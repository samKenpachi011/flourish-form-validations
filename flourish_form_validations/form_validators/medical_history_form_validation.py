from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO, NOT_APPLICABLE, NEG, POS, OTHER, NONE
from edc_form_validators import FormValidator
# from flourish_caregiver.helper_classes import MaternalStatusHelper

from .crf_form_validator import CRFFormValidator


class MedicalHistoryFormValidator(CRFFormValidator, FormValidator):

    antenatal_enrollment_model = 'flourish_caregiver.antenatalenrollment'

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    @property
    def maternal_visit_cls(self):
        return django_apps.get_model(self.maternal_visit_model)

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        med_history_changed = self.cleaned_data.get('med_history_changed')
        self.validate_med_history_changed(med_history_changed)
        if not med_history_changed or med_history_changed == YES:
            self.applicable_if_true(
                self.subject_status == POS,
                field_applicable='know_hiv_status',)

            self.validate_caregiver_chronic_multiple_selection(
                cleaned_data=self.cleaned_data)
            self.validate_chronic_since_who_diagnosis_neg(
                cleaned_data=self.cleaned_data)
            self.validate_who_diagnosis_who_chronic_list(
                cleaned_data=self.cleaned_data)
            self.validate_other_caregiver()
            self.validate_caregiver_medications_multiple_selections()
            self.validate_other_caregiver_medications()

    def validate_med_history_changed(self, med_history_changed):
        if med_history_changed:
            if med_history_changed == NOT_APPLICABLE:
                msg = {'med_history_changed': 'This field is applicable.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            fields = ['chronic_since', 'who_diagnosis', 'know_hiv_status']
            for field in fields:
                self.not_applicable_if(
                    NO,
                    field='med_history_changed',
                    field_applicable=field)
            self.not_required_if(
                NO,
                field='med_history_changed',
                field_required='caregiver_chronic_other',
                inverse=False)
            if med_history_changed == NO:
                m2m_fields = ['caregiver_chronic', 'who', 'caregiver_medications']
                for field in m2m_fields:
                    self.validate_m2m_na(field)

    def validate_chronic_since_who_diagnosis_neg(self, cleaned_data=None):

        if self.subject_status == NEG and cleaned_data.get('chronic_since') == YES:
            msg = {'chronic_since':
                   'The caregiver is HIV negative. Chronic_since should be NO'}
            self._errors.update(msg)
            raise ValidationError(msg)

        self.applicable_if_true(
            self.subject_status == POS,
            field_applicable='who_diagnosis',
            not_applicable_msg=('The caregiver is HIV negative. Who Diagnosis '
                                'should be Not Applicable')
        )

        if self.subject_status == POS and cleaned_data.get('chronic_since') == NO:
            if cleaned_data.get('who_diagnosis') != NO:
                msg = {'who_diagnosis':
                       'The caregiver is HIV positive, because chronic since is '
                       'NO and Who Diagnosis should also be NO'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_who_diagnosis_who_chronic_list(self, cleaned_data=None):

        # subject_status = self.maternal_status_helper.hiv_status

        if self.subject_status == POS and cleaned_data.get('who_diagnosis') == YES:
            qs = self.cleaned_data.get('who')
            if qs and qs.count() > 0:
                selected = {obj.short_name: obj.name for obj in qs}
                if NOT_APPLICABLE in selected:
                    msg = {'who':
                           'Participant indicated that they had WHO stage III '
                           'and IV, list of diagnosis cannot be N/A'}
                    self._errors.update(msg)
                    raise ValidationError(msg)
        elif cleaned_data.get('who_diagnosis') != YES:
            m2m = 'who'
            message = ('Participant did not indicate that they have WHO stage'
                       ' III and IV, list of diagnosis must be N/A')
            self.validate_m2m_na(m2m, message)

    def validate_caregiver_chronic_multiple_selection(self, cleaned_data=None):
        selected = {}
        qs = self.cleaned_data.get('caregiver_chronic')
        if qs and qs.count() > 0:
            selected = {obj.short_name: obj.name for obj in qs}
        if cleaned_data.get('chronic_since') == YES:
            if NOT_APPLICABLE in selected:
                msg = {'caregiver_chronic':
                       'Participant indicated that they had chronic'
                       ' conditions list of diagnosis cannot be N/A'}
                self._errors.update(msg)
                raise ValidationError(msg)
        elif cleaned_data.get('chronic_since') == NO:
            if NOT_APPLICABLE not in selected:
                msg = {'caregiver_chronic':
                       'Participant indicated that they had no chronic '
                       'conditions list of diagnosis should be N/A'}
                self._errors.update(msg)
                raise ValidationError(msg)
        self.m2m_single_selection_if(
            NOT_APPLICABLE,
            m2m_field='caregiver_chronic')

    def validate_other_caregiver(self):
        self.m2m_other_specify(
            OTHER,
            m2m_field='caregiver_chronic',
            field_other='caregiver_chronic_other')

    def validate_caregiver_medications_multiple_selections(self):
        selections = [NOT_APPLICABLE, NONE]
        self.m2m_single_selection_if(
            *selections,
            m2m_field='caregiver_medications')

    def validate_other_caregiver_medications(self):

        self.m2m_other_specify(
            OTHER,
            m2m_field='caregiver_medications',
            field_other='caregiver_medications_other')

    def validate_m2m_na(self, m2m_field, message=None):
        qs = self.cleaned_data.get(m2m_field)
        message = message or 'This field is not applicable.'
        if qs and qs.count() > 0:
            selected = {obj.short_name: obj.name for obj in qs}
            if NOT_APPLICABLE not in selected:
                msg = {m2m_field: message}
                self._errors.update(msg)
                raise ValidationError(msg)

            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field=m2m_field)
