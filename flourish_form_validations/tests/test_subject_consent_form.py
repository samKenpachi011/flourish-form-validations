from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES, OTHER

from ..form_validators import SubjectConsentFormValidator
from .models import SubjectConsent, SubjectScreening
from .test_model_mixin import TestModeMixin


@tag('sc')
class TestSubjectConsentForm(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(SubjectConsentFormValidator, *args, **kwargs)

    def setUp(self):

        self.screening_identifier = 'ABC12345'
        self.study_child_identifier = '1234DCD'

        self.consent_options = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'version': 1,
            'dob': (get_utcnow() - relativedelta(years=25)).date(),
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'identity': '123425678',
            'confirm_identity': '123425678',
            'citizen': YES}

    def test_consent_dob_mismatch_consent_dob_years(self):
        SubjectConsent.objects.create(
            subject_identifier='11111111',
            screening_identifier=self.screening_identifier,
            consent_datetime=get_utcnow() - relativedelta(years=2),
            dob=get_utcnow() - relativedelta(years=20),
            version='1',
        )
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('dob', form_validator._errors)

    def test_consent_dob_match_consent_dob_years(self):
        SubjectConsent.objects.create(
            subject_identifier='11111111',
            screening_identifier=self.screening_identifier,
            consent_datetime=get_utcnow() - relativedelta(years=2),
            dob=get_utcnow() - relativedelta(years=25),
            version='1',
        )
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_consent_dob_less_than_18years(self):
        self.consent_options.update({'dob': (get_utcnow() - relativedelta(years=16)).date()})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('dob', form_validator._errors)

    @tag('sc1')
    def test_recruit_source_prior_preg_not_required(self):
        SubjectScreening.objects.create(
            screening_identifier=self.screening_identifier)

        self.consent_options.update(
            {'recruitment_clinic': 'Prior'})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recruitment_clinic', form_validator._errors)

    def test_recruit_source_OTHER_source_other_required(self):
        self.consent_options.update(
            {'recruit_source': OTHER,
             'recruit_source_other': None})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recruit_source_other', form_validator._errors)

    def test_recruit_source_OTHER_source_other_provided(self):
        self.consent_options.update(
            {'recruit_source': OTHER,
             'recruit_source_other': 'None'})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_recruit_source_not_OTHER_source_other_invalid(self):
        self.consent_options.update(
            {'recruit_source': 'ANC clinic staff',
             'recruit_source_other': 'family friend'})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recruit_source_other', form_validator._errors)

    def test_recruit_source_not_OTHER_source_other_valid(self):
        self.consent_options.update(
            {'recruit_source': 'ANC clinic staff',
             'recruit_source_other': None})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_recruitment_clinic_OTHER_recruitment_clinic_other_required(self):
        self.consent_options.update(
            {'recruitment_clinic': OTHER,
             'recruitment_clinic_other': None})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recruitment_clinic_other', form_validator._errors)

    def test_recruitment_clinic_OTHER_recruitment_clinic_other_provided(self):
        self.consent_options.update(
            {'recruitment_clinic': OTHER,
             'recruitment_clinic_other': 'None'})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_recruitment_clinic_not_OTHER_recruitment_clinic_other_invalid(self):
        self.consent_options.update(
            {'recruitment_clinic': 'PMH',
             'recruitment_clinic_other': 'G.West Clinic'})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recruitment_clinic_other', form_validator._errors)

    def test_recruitment_clinic_not_OTHER_recruitment_clinic_other_valid(self):
        self.consent_options.update(
            {'recruitment_clinic': 'G.West Clinic',
             'recruitment_clinic_other': None})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_first_name_last_name_valid(self):
        self.consent_options.update(
            {'first_name': 'TEST BONE',
             'last_name': 'TEST',
             'initials': 'TOT'})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('initials', form_validator._errors)

    def test_first_name_last_name_invalid(self):
        self.consent_options.update(
            {'first_name': 'TEST ONE',
             'last_name': 'TEST',
             'initials': 'TOT'})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_first_name_invalid(self):
        self.consent_options.update(
            {'first_name': 'TEST ONE BEST',
             'last_name': 'TEST',
             'initials': 'TOT'})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('first_name', form_validator._errors)
