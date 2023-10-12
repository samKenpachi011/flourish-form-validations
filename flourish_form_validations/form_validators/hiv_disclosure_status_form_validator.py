from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.utils import age, get_utcnow
from edc_constants.choices import YES
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class HIVDisclosureStatusFormValidator(FormValidatorMixin, FormValidator):
    child_assent_model = 'flourish_child.childassent'
    caregiver_child_consent_model = 'flourish_caregiver.caregiverchildconsent'
    maternal_delivery_model = 'flourish_caregiver.maternaldelivery'

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        not_required_fields = ['plan_to_disclose', 'reason_not_disclosed', ]
        for field in not_required_fields:
            self.not_required_if(YES,
                                 field='disclosed_status',
                                 field_required=field)

        required_fields = ['disclosure_age', 'who_disclosed',
                           'disclosure_difficulty', 'child_reaction']

        for field in required_fields:
            self.required_if(YES,
                             field='disclosed_status',
                             field_required=field)
        self.validate_other_specify(field='reason_not_disclosed')
        self.validate_other_specify(field='who_disclosed')
        self.validate_other_specify(field='child_reaction')

        self.validate_child_age()

    def validate_child_age(self):
        disclosure_age = self.cleaned_data.get('disclosure_age')
        if not any(child_age > disclosure_age for child_age in self.child_ages):
            raise ValidationError(
                {'disclosure_age': 'Caregiver does not have a child older the age you '
                                   f'provided for disclosure age. The oldest child is '
                                   f'{max(self.child_ages)} years old.'})

    @property
    def child_ages(self):
        child_ages = []
        if self.child_assent_objs:
            for child in self.child_assent_objs:
                birth_date = child.dob
                years = age(birth_date, get_utcnow()).years + age(
                    birth_date, get_utcnow()).months / 12
                child_ages.append(years)
        if self.child_caregiver_consent_objs:
            for child in self.child_caregiver_consent_objs:
                birth_date = child.child_dob
                years = age(birth_date, get_utcnow()).years + age(
                    birth_date, get_utcnow()).months / 12
                child_ages.append(years)
        if self.maternal_delivery_objs:
            for child in self.maternal_delivery_objs:
                birth_date = child.delivery_datetime.date()
                years = age(birth_date, get_utcnow()).months / 12
                child_ages.append(years)
        return child_ages

    @property
    def child_caregiver_consent_objs(self):
        child_caregiver_consent_model_cls = django_apps.get_model(
            self.caregiver_child_consent_model)
        return child_caregiver_consent_model_cls.objects.filter(
            subject_identifier__startswith=self.subject_identifier)

    @property
    def maternal_delivery_objs(self):
        maternal_delivery_model_cls = django_apps.get_model(
            self.maternal_delivery_model)
        return maternal_delivery_model_cls.objects.filter(
            subject_identifier=self.subject_identifier)

    @property
    def child_assent_objs(self):
        child_assent_model_cls = django_apps.get_model(self.child_assent_model)
        return child_assent_model_cls.objects.filter(
            subject_identifier=self.subject_identifier)
