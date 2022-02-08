from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError


class FlourishFormValidatorMixin:

    antenatal_enrollment_model = 'flourish_caregiver.antenatalenrollment'
    caregiver_consent_model = 'flourish_caregiver.subjectconsent'
    screening_preg_women_model = 'flourish_caregiver.screeningpregwomen'

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    @property
    def screening_preg_women_cls(self):
        return django_apps.get_model(self.screening_preg_women_model)

    @property
    def caregiver_consent_cls(self):
        return django_apps.get_model(self.caregiver_consent_model)

    def validate_against_consent_datetime(self, report_datetime, id=None):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""

        consent = self.validate_against_consent()

        if report_datetime and report_datetime < consent.consent_datetime:
            raise forms.ValidationError(
                "Report datetime cannot be before consent datetime")

    def validate_against_consent(self):
        """Returns an instance of the current maternal consent version form or
        raises an exception if not found."""
        try:
            consent = self.caregiver_consent_cls.objects.get(
                subject_identifier=self.subject_identifier,
                version=self.consent_version)
        except self.caregiver_consent_cls.DoesNotExist:
                raise ValidationError(
                    'Please complete Caregiver Consent form '
                    f'before proceeding.')
        else:
            return consent

    @property
    def consent_version_cls(self):
        return django_apps.get_model('flourish_caregiver.flourishconsentversion')

    @property
    def consent_version(self):
        version = None
        try:
            consent_version_obj = self.consent_version_cls.objects.get(
                screening_identifier=self.screening_obj.screening_identifier)
        except self.consent_version_cls.DoesNotExist:
            version = '1'
        else:
            version = consent_version_obj.version
        return version

    @property
    def screening_obj(self):
        screening_obj = self.caregiver_consent_cls.objects.filter(
                 subject_identifier=self.subject_identifier)
        if screening_obj.count() > 0:
            return screening_obj[0]
        return None

