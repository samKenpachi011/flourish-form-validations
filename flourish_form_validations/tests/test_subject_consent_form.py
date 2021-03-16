from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES, OTHER, NOT_APPLICABLE

from ..form_validators import SubjectConsentFormValidator
from .models import SubjectConsent, MaternalDataset, ChildDataset


@tag('consent')
class TestSubjectConsentForm(TestCase):

    def setUp(self):
        subject_consent_model = 'flourish_form_validations.subjectconsent'
        SubjectConsentFormValidator.subject_consent_model = subject_consent_model

        maternal_dataset_model = 'flourish_form_validations.maternaldataset'
        SubjectConsentFormValidator.maternal_dataset_model = maternal_dataset_model

        child_dataset_model = 'flourish_form_validations.childdataset'
        SubjectConsentFormValidator.child_dataset_model = child_dataset_model

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
            'citizen': YES,
            'child_dob': (get_utcnow() - relativedelta(years=2)).date()}

    def test_consent_dob_mismatch_consent_dob_years(self):
        SubjectConsent.objects.create(
            subject_identifier='11111111',
            screening_identifier=self.screening_identifier,
            consent_datetime=get_utcnow() - relativedelta(years=2),
            dob=get_utcnow() - relativedelta(years=20),
            version='1',
            child_dob=(get_utcnow() - relativedelta(years=2)).date()
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
            child_dob=(get_utcnow() - relativedelta(years=2)).date()
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

    def test_child_dob_mismatch_dataset(self):
        MaternalDataset.objects.create(
            screening_identifier=self.screening_identifier,
            study_child_identifier=self.study_child_identifier,
            delivdt=(get_utcnow() - relativedelta(years=1)).date())
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('child_dob', form_validator._errors)

    def test_child_dob_match_dataset(self):
        MaternalDataset.objects.create(
            screening_identifier=self.screening_identifier,
            study_child_identifier=self.study_child_identifier,
            delivdt=(get_utcnow() - relativedelta(years=2)).date())
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_consent_for_child_applicable(self):
        MaternalDataset.objects.create(
            screening_identifier=self.screening_identifier,
            study_child_identifier=self.study_child_identifier,
            delivdt=(get_utcnow() - relativedelta(years=2)).date())
        self.consent_options.update(
            {'child_test': NOT_APPLICABLE,
             'child_remain_in_study': NOT_APPLICABLE})
        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('child_test', form_validator._errors)

    def test_child_preg_test_na_if_male(self):
        MaternalDataset.objects.create(
            screening_identifier=self.screening_identifier,
            study_child_identifier=self.study_child_identifier,
            delivdt=(get_utcnow() - relativedelta(years=2)).date())

        ChildDataset.objects.create(
            study_child_identifier=self.study_child_identifier,
            infant_sex='Male',)

        self.consent_options.update(
            {'child_test': YES,
             'child_remain_in_study': YES,
             'child_preg_test': NOT_APPLICABLE})

        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_child_preg_test_na_if_female_fails(self):
        MaternalDataset.objects.create(
            screening_identifier=self.screening_identifier,
            study_child_identifier=self.study_child_identifier,
            delivdt=(get_utcnow() - relativedelta(years=2)).date())

        ChildDataset.objects.create(
            study_child_identifier=self.study_child_identifier,
            infant_sex='Female',)

        self.consent_options.update(
            {'child_test': YES,
             'child_remain_in_study': YES,
             'child_preg_test': NOT_APPLICABLE})

        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('child_preg_test', form_validator._errors)

    def test_child_knows_status_na_if_less_than_16years(self):
        MaternalDataset.objects.create(
            screening_identifier=self.screening_identifier,
            study_child_identifier=self.study_child_identifier,
            delivdt=(get_utcnow() - relativedelta(years=2)).date())

        ChildDataset.objects.create(
            study_child_identifier=self.study_child_identifier,
            infant_sex='Female',)

        self.consent_options.update(
            {'child_test': YES,
             'child_remain_in_study': YES,
             'child_preg_test': YES,
             'child_knows_status': NOT_APPLICABLE})

        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_child_knows_status_na_if_more_than_16years_fails(self):
        MaternalDataset.objects.create(
            screening_identifier=self.screening_identifier,
            study_child_identifier=self.study_child_identifier,
            delivdt=(get_utcnow() - relativedelta(years=17)).date())

        ChildDataset.objects.create(
            study_child_identifier=self.study_child_identifier,
            infant_sex='Female',)

        self.consent_options.update(
            {'child_dob': (get_utcnow() - relativedelta(years=17)).date(),
             'child_test': YES,
             'child_remain_in_study': YES,
             'child_preg_test': YES,
             'child_knows_status': NOT_APPLICABLE})

        form_validator = SubjectConsentFormValidator(
            cleaned_data=self.consent_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('child_knows_status', form_validator._errors)

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
