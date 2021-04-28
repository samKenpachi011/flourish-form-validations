from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES, OTHER

from ..form_validators import SubjectConsentFormValidator
from .models import SubjectConsent


@tag('sc')
class TestSubjectConsentForm(TestCase):

    def setUp(self):
        subject_consent_model = 'flourish_form_validations.subjectconsent'
        SubjectConsentFormValidator.subject_consent_model = subject_consent_model

        maternal_dataset_model = 'flourish_form_validations.maternaldataset'
        SubjectConsentFormValidator.maternal_dataset_model = maternal_dataset_model

        child_dataset_model = 'flourish_form_validations.childdataset'
        SubjectConsentFormValidator.child_dataset_model = child_dataset_model

        prior_screening_model = 'flourish_form_validations.subjectscreening'
        SubjectConsentFormValidator.prior_screening_model = prior_screening_model

        caregiver_locator_model = 'flourish_form_validations.subjectconsent'
        SubjectConsentFormValidator.prior_screening_model = caregiver_locator_model

        preg_women_screening_model = 'flourish_form_validations.subjectscreening'
        SubjectConsentFormValidator.preg_women_screening_model = preg_women_screening_model

        delivery_model = 'flourish_form_validations.maternaldelivery'
        SubjectConsentFormValidator.delivery_model = delivery_model

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
