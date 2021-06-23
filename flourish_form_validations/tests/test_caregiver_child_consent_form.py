from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES, FEMALE, NOT_APPLICABLE, MALE
from ..form_validators import CaregiverChildConsentFormValidator
from .test_model_mixin import TestModeMixin
from .models import ChildDataset


@tag('ccc')
class TestCaregiverChildConsentForm(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(CaregiverChildConsentFormValidator, *args, **kwargs)

    def setUp(self):

        self.screening_identifier = 'ABC12345'
        self.study_child_identifier = '1234DCD'

        self.consent_options = {
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

