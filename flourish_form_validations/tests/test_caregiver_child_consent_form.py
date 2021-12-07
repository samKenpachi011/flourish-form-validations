from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES, FEMALE, NOT_APPLICABLE, MALE

from ..form_validators import CaregiverChildConsentFormValidator
from .models import ChildDataset, SubjectConsent, SubjectScreening
from .test_model_mixin import TestModeMixin


@tag('ccc')
class TestCaregiverChildConsentForm(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(CaregiverChildConsentFormValidator, *args, **kwargs)

    def setUp(self):

        self.screening_identifier = 'ABC12345'
        self.study_child_identifier = '1234DCD'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111',
            screening_identifier=self.screening_identifier,
            gender='F', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='1')

        self.consent_options = {
            'subject_consent': self.subject_consent,
            'consent_datetime': get_utcnow(),
            'version': 1,
            'child_dob': (get_utcnow() - relativedelta(years=5)).date(),
            'first_name': 'TEST ONE',
            'gender': FEMALE,
            'child_preg_test': NOT_APPLICABLE,
            'last_name': 'TEST',
            'initials': 'TOT',
            'identity': '123425678',
            'confirm_identity': '123425678',
            'citizen': YES}

        ChildDataset.objects.create(
            study_child_identifier='1112-9876',
            infant_sex='Female',
            dob=(get_utcnow() - relativedelta(years=5)).date())

    def test_form_valid(self):
        form_validator = CaregiverChildConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_child_dataset_valid(self):
        self.consent_options['study_child_identifier'] = '1112-9876'

        form_validator = CaregiverChildConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_child_dataset_gender_invalid(self):
        self.consent_options['study_child_identifier'] = '1112-9876'
        self.consent_options['gender'] = MALE

        form_validator = CaregiverChildConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('study_child_identifier', form_validator._errors)

    def test_child_dataset_dob_invalid(self):
        self.consent_options['study_child_identifier'] = '1112-9876'
        self.consent_options['child_dob'] = (get_utcnow() - relativedelta(years=6)).date()

        form_validator = CaregiverChildConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('study_child_identifier', form_validator._errors)

    def test_child_dataset_invalid2(self):
        self.consent_options['study_child_identifier'] = '1112-9879'
        self.consent_options['gender'] = FEMALE

        form_validator = CaregiverChildConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('study_child_identifier', form_validator._errors)

    @tag('tt1')
    def test_pregnant_not_required(self):
        SubjectScreening.objects.create(
            screening_identifier=self.screening_identifier)

        self.consent_options['last_name'] = None
        self.consent_options['first_name'] = None
        self.consent_options['gender'] = None

        form_validator = CaregiverChildConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_gender_required_invalid(self):
        self.consent_options['study_child_identifier'] = '1112-9876'
        self.consent_options['gender'] = None

        form_validator = CaregiverChildConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('gender', form_validator._errors)

    def test_last_name_required_invalid(self):
        self.consent_options['study_child_identifier'] = '1112-9876'
        self.consent_options['last_name'] = None

        form_validator = CaregiverChildConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('last_name', form_validator._errors)

    def test_first_name_required_invalid(self):
        self.consent_options['study_child_identifier'] = '1112-9876'
        self.consent_options['first_name'] = None

        form_validator = CaregiverChildConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('first_name', form_validator._errors)
