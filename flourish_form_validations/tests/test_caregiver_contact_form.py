from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, OTHER

from ..form_validators import CaregiverContactFormValidator
from .models import CaregiverLocator, SubjectConsent, FlourishConsentVersion
from .test_model_mixin import TestModeMixin


@tag('contact')
class TestCaregiverContactForm(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(CaregiverContactFormValidator, *args, **kwargs)

    def setUp(self):
        CaregiverContactFormValidator.caregiver_consent_model = \
            'flourish_form_validations.subjectconsent'
        CaregiverContactFormValidator.caregiver_locator_model = \
            'flourish_form_validations.caregiverlocator'

        self.subject_identifier = '12345678'
        self.screening_identifier = 'ABC12345'

        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier=self.subject_identifier,
            screening_identifier=self.screening_identifier,
            gender='F', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='1')

        self.caregiver_locator = CaregiverLocator.objects.create(
            subject_identifier=self.subject_identifier,
            screening_identifier=self.screening_identifier,
            may_call=YES,
            may_visit_home=YES)

    def test_contact_form_call_invalid(self):
        """ Assert raises if contact type is phone call but call permission on
            locator was not given.
        """
        self.caregiver_locator.may_call = NO
        self.caregiver_locator.save()
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'contact_type': 'phone_call'
        }
        form_validator = CaregiverContactFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contact_type', form_validator._errors)

    def test_contact_form_visit_invalid(self):
        """ Assert raises if contact type is in person visit but home visit
            permission on locator was not given.
        """
        self.caregiver_locator.may_visit_home = NO
        self.caregiver_locator.save()
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'contact_type': 'in_person'
        }
        form_validator = CaregiverContactFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contact_type', form_validator._errors)

    def test_call_reason_other_specify(self):
        """ Assert raises if call reason is 'Other, specify' but call reason
            other not provided.
        """
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'contact_type': 'in_person',
            'call_reason': OTHER,
            'call_reason_other': None
        }
        form_validator = CaregiverContactFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('call_reason_other', form_validator._errors)

    def test_contact_success_valid(self):
        '''Assert form saves without error.
        '''
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'contact_type': 'phone_call',
            'contact_success': YES,
            'contact_comment': 'blahblah'

        }
        form_validator = CaregiverContactFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
