from edc_constants.constants import NO, YES
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin
from django.forms import ValidationError
from django.apps import apps as django_apps


class InterviewFocusGroupInterestFormValidator(FormValidatorMixin, FormValidator):
    maternal_delivery_model = 'flourish_caregiver.maternaldelivery'
    caregiver_child_consent_model = 'flourish_caregiver.caregiverchildconsent'

    def onschedule_model_cls(self, onschedule_model):
        return django_apps.get_model(onschedule_model)

    @property
    def maternal_delivery_model_cls(self):
        return django_apps.get_model(self.maternal_delivery_model)

    @property
    def caregiver_child_consent_cls(self):
        return django_apps.get_model(self.caregiver_child_consent_model)

    def clean(self):
        self.required_if(
            *['group', 'either'],
            field='discussion_pref',
            field_required='hiv_group_pref'
        )

        self.required_if_true(
            self.is_preg_enrol,
            field_required='infant_feeding_group_interest',
            required_msg='Infant feeding group interest is required if enrolled pregnant(pregnant or postpartum).'
        )

        fields = ['same_status_comfort', 'diff_status_comfort']

        for field in fields:
            self.required_if_true(
                self.is_preg_enrol and self.cleaned_data['discussion_pref'] in ['group', 'either'],
                field_required=field
            )

    def is_preg_enrol(self, child_subject_identifier):
        consents = self.caregiver_child_consent_cls.objects.filter(
            subject_identifier=child_subject_identifier)
        try:
            consent = consents.latest('consent_datetime')
        except self.caregiver_child_consent_cls.DoesNotExist:
            raise ValidationError('Caregiver consent on behalf of child does not exist.')
        else:
            return consent.preg_enroll
