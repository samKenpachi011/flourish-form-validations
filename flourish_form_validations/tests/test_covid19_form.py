from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NEG, OTHER

from ..form_validators.covid19_form_validation import Covid19FormValidator
from .models import ListModel, FlourishConsentVersion, SubjectConsent, Appointment, MaternalVisit


@tag('test_covid')
class Covid19Tests(TestCase):

    def setUp(self):
        self.form_data = {
            'test_for_covid': YES,
            'date_of_test': '2021-01-01',
            'is_test_estimated': YES,
            'reason_for_testing': 'routine_testing',
            'result_of_test': NEG,
            'has_tested_positive': NO,
            'close_contact': ListModel.objects.all(),
            'symptoms_for_past_14days': ListModel.objects.all(),
            'full_vaccinated': YES,
        }

        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_identifier = '11111111'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='1')

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2000M')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow())
        self.form_data['maternal_visit'] = self.maternal_visit

    def test_other_reason_for_testing_required(self):
        self.form_data['reason_for_testing'] = OTHER
        form = Covid19FormValidator(cleaned_data=self.form_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('other_reason_for_testing', form._errors)

    def test_has_tested_positive_date_required(self):
        self.form_data['has_tested_positive'] = YES
        self.form_data['date_of_test_member'] = None

        form = Covid19FormValidator(cleaned_data=self.form_data)

        self.assertRaises(ValidationError, form.validate)
        self.assertIn('date_of_test_member', form._errors)

    def test_received_booster(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'received_booster': YES,
            'booster_vac_type': 'blah blah',
            'booster_vac_date': 'blah blah',
        }
        form_validator = Covid19FormValidator(
            cleaned_data=cleaned_data or self.form_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_other_booster_vac_type(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'booster_vac_type': OTHER,
            'other_booster_vac_type': 'blah blah',
        }
        form_validator = Covid19FormValidator(
            cleaned_data=cleaned_data or self.form_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
