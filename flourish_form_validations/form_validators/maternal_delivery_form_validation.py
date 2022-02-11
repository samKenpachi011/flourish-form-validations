from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import OTHER, NONE
from edc_form_validators import FormValidator

from .crf_form_validator import CRFFormValidator
from .form_validator_mixin import FlourishFormValidatorMixin


class MaternalDeliveryFormValidator(CRFFormValidator, FlourishFormValidatorMixin,
                                    FormValidator):
    maternal_arv_model = 'flourish_caregiver.maternalarv'
    maternal_visit_model = 'flourish_caregiver.maternalvisit'
    ultrasound_model = 'flourish_caregiver.ultrasound'
    arvs_pre_pregnancy = 'flourish_caregiver.arvsprepregnancy'

    @property
    def ultrasound_cls(self):
        return django_apps.get_model(self.ultrasound_model)

    @property
    def maternal_visit_cls(self):
        return django_apps.get_model(self.maternal_visit_model)

    @property
    def maternal_arv_cls(self):
        return django_apps.get_model(self.maternal_arv_model)

    @property
    def arvs_pre_pregnancy_cls(self):
        return django_apps.get_model(self.arvs_pre_pregnancy)

    def clean(self):
        self.subject_identifier = self.cleaned_data.get('subject_identifier')
        #         if self.instance and not self.instance.id:
        #             self.validate_offstudy_model()

        id = None
        if self.instance:
            id = self.instance.id

        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'),
            id=id)

        condition = self.cleaned_data.get(
            'mode_delivery') and 'c-section' in self.cleaned_data.get('mode_delivery')
        self.required_if_true(
            condition,
            field_required='csection_reason'
        )

        self.validate_against_maternal_delivery()
        self.validate_ultrasound(cleaned_data=self.cleaned_data)
        self.validate_initiation_date(cleaned_data=self.cleaned_data)
        self.validate_valid_regime_hiv_pos_only(cleaned_data=self.cleaned_data)
        self.validate_live_births_still_birth(cleaned_data=self.cleaned_data)
        self.validate_other()

    def validate_ultrasound(self, cleaned_data=None):
        ultrasound = self.ultrasound_cls.objects.filter(
            maternal_visit__appointment__subject_identifier=cleaned_data.get(
                'subject_identifier'))
        if not ultrasound:
            message = 'Please complete ultrasound form first'
            raise ValidationError(message)

    def validate_initiation_date(self, cleaned_data=None):
        subject_identifier = cleaned_data.get('subject_identifier')
        maternal_arv = self.maternal_arv_cls.objects.filter(
            maternal_arv_durg_preg__maternal_visit__appointment__subject_identifier=subject_identifier,
            arv_code='Tenoforvir',
            stop_date__isnull=True).order_by('-start_date').first()
        if maternal_arv:
            initiation_date = cleaned_data.get('arv_initiation_date')
            if initiation_date != maternal_arv.start_date:
                message = {'arv_initiation_date':
                               'ARV\'s initiation date must match start date '
                               'in pregnancy form, pregnancy form start date is '
                               f'{maternal_arv.start_date}, got {initiation_date}.'}
                self._errors.update(message)
                raise ValidationError(message)

    def validate_live_births_still_birth(self, cleaned_data=None):
        still_births = cleaned_data.get('still_births')
        live_births = cleaned_data.get('live_infants_to_register')
        if still_births == 0 and live_births != 1:
            message = {'live_infants_to_register':
                           'If still birth is 0 then live birth should be 1.'}
            self._errors.update(message)
            raise ValidationError(message)
        elif still_births == 1 and live_births != 0:
            message = {'still_births':
                           'If live births is 1 then still birth should be 0.'}
            self._errors.update(message)
            raise ValidationError(message)

    def validate_other(self):
        fields = {'delivery_hospital': 'delivery_hospital_other',
                  'mode_delivery': 'mode_delivery_other',
                  'csection_reason': 'csection_reason_other'}
        for field, other in fields.items():
            self.validate_other_specify(
                field=field,
                other_specify_field=other
            )
        selections = [OTHER, NONE]
        self.m2m_single_selection_if(
            *selections,
            m2m_field='delivery_complications')
        self.m2m_other_specify(
            'Other',
            m2m_field='delivery_complications',
            field_other='delivery_complications_other')

    def validate_against_maternal_delivery(self):

        subject_identifier = self.cleaned_data.get('subject_identifier')

        try:
            pre_pregnancy = self.arvs_pre_pregnancy_cls.objects.get(
                maternal_visit__appointment__subject_identifier=subject_identifier)
        except self.arvs_pre_pregnancy_cls.DoesNotExist:
            pass
        else:
            if pre_pregnancy.art_start_date != self.cleaned_data.get(
                    'arv_initiation_date'):
                raise ValidationError({
                    'arv_initiation_date': 'The date does not corrospond with the date from Arv Pregnancy CRF, '
                                           f'the date should be {pre_pregnancy.art_start_date} '})
