from datetime import timedelta
from edc_base.utils import get_utcnow

from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin
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
            field_required='hiv_group_pref',
        )

        self.required_if_true(
            self.is_preg_enroll(),
            field_required='infant_feeding_group_interest',
            required_msg='Infant feeding group interest is required if enrolled'
                         ' pregnant(pregnant or postpartum).',
        )

        fields = ['same_status_comfort', 'diff_status_comfort']
        condition = (
                self.is_preg_enroll
                and self.cleaned_data['discussion_pref'] in ['group', 'either']
                and self.is_within_first_year_postpartum()
        )

        for field in fields:
            self.required_if_true(
                condition,
                field_required=field,
            )

    def is_preg_enroll(self):
        subject_identifier = self.cleaned_data.get('maternal_visit').subject_identifier
        consents = self.caregiver_child_consent_cls.objects.filter(
            subject_identifier=subject_identifier)

        if consents.exists():
            consent = consents.latest('consent_datetime')
            return consent.preg_enroll
        else:
            raise ValidationError('Caregiver consent on behalf of child does not exist.')

    def is_within_first_year_postpartum(self):
        """Returns True if subject is currently in first year postpartum."""

        maternal_visit = self.cleaned_data.get('maternal_visit')
        subject_identifier = maternal_visit.subject_identifier
        maternal_delivery_objs = self.maternal_delivery_model_cls.objects.filter(
            subject_identifier=subject_identifier
        )
        if maternal_delivery_objs.exists():
            maternal_delivery_obj = maternal_delivery_objs.first()
            if maternal_delivery_obj.delivery_datetime:
                today = get_utcnow().date()
                delivery_date = maternal_delivery_obj.delivery_datetime.date()
                return (today - delivery_date) < timedelta(days=365)
        else:
            return False
