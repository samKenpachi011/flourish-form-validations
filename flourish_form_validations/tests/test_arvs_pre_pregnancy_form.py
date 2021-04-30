from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import (
    RESTARTED, NO, YES, CONTINUOUS, STOPPED, NEG, POS, NOT_APPLICABLE)

from ..form_validators import ArvsPrePregnancyFormValidator
from .models import AntenatalEnrollment
from .models import SubjectConsent, Appointment, MaternalVisit


class TestArvsPrePregnancyForm(TestCase):

    def setUp(self):
        ArvsPrePregnancyFormValidator.caregiver_consent_model = \
            'flourish_form_validations.subjectconsent'

        ArvsPrePregnancyFormValidator.antenatal_enrollment_model = \
            'flourish_form_validations.antenatalenrollment'

        ArvsPrePregnancyFormValidator.subject_screening_model = \
            'flourish_form_validations.subjectscreening'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(),
            version='1')

        self.antenatal_enrollment = AntenatalEnrollment.objects.create(
            subject_identifier='11111111',
            enrollment_hiv_status=NEG, week32_result=POS,
            rapid_test_result=POS, rapid_test_date=get_utcnow().date(),
            week32_test_date=get_utcnow().date())

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,)

    def test_preg_on_art_no_preg_prior_invalid(self):
        '''Asserts raises exception if subject was not on triple
        antiretrovirals at the time she became pregnant but prior to
        pregnancy value is restarted.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'preg_on_art': NO,
            'prior_preg': RESTARTED, }
        form_validator = ArvsPrePregnancyFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prior_preg', form_validator._errors)

    def test_preg_on_art_no_preg_prior_invalid2(self):
        '''Asserts raises exception if subject was not on triple
        antiretrovirals at the time she became pregnant but prior to
        pregnancy value is continuous.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'preg_on_art': NO,
            'prior_preg': CONTINUOUS}
        form_validator = ArvsPrePregnancyFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prior_preg', form_validator._errors)

    def test_preg_on_art_yes_preg_prior_invalid(self):
        '''Asserts raises exception if subject was still on triple
        antiretrovirals at the time she became pregnant but prior to
        pregnancy value is stopped.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'preg_on_art': YES,
            'prior_preg': STOPPED,
            'art_start_date': get_utcnow().date(),
            'is_date_estimated': 'yes',
            'report_datetime': get_utcnow() + relativedelta(days=30)}
        form_validator = ArvsPrePregnancyFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prior_preg', form_validator._errors)

    def test_antenatal_enrollment_hiv_test_date_provided(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_preg_art': YES,
            'art_start_date': get_utcnow().date() - relativedelta(days=30),
            'is_date_estimated': 'no',
            'report_datetime': get_utcnow() + relativedelta(days=30)}

        self.antenatal_enrollment.week32_test_date = get_utcnow().date()
        form_validator = ArvsPrePregnancyFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_prev_preg_art_yes_start_date_provided(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_preg_art': YES,
            'art_start_date': get_utcnow().date(),
            'is_date_estimated': 'no',
            'report_datetime': get_utcnow()}
        form_validator = ArvsPrePregnancyFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_art_start_date_valid_date_est_provided(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'art_start_date': get_utcnow().date(),
            'is_date_estimated': 'yes',
            'report_datetime': get_utcnow() + relativedelta(days=30)}
        form_validator = ArvsPrePregnancyFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_art_start_date_invalid_date_est_valid(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'art_start_date': None,
            'is_date_estimated': NOT_APPLICABLE}
        form_validator = ArvsPrePregnancyFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_consent_date_less_than_report_date_valid(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        self.subject_consent.consent_datetime = \
            get_utcnow() - relativedelta(days=30)
        self.subject_consent.save()

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'art_start_date': get_utcnow().date(),
            'is_date_estimated': NO,
            'report_datetime': get_utcnow()}
        form_validator = ArvsPrePregnancyFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_consent_date_more_than_report_date_invalid(self):
        '''Asserts raises exception if subject received antiretrovirals during
        a prior pregnancy and date first started given but does not state if
        the date is estimated or not.'''

        self.maternal_visit.report_datetime = get_utcnow() - relativedelta(days=30)
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'art_start_date': get_utcnow().date(),
            'is_date_estimated': NO,
            'report_datetime': get_utcnow() - relativedelta(days=30)}
        form_validator = ArvsPrePregnancyFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('report_datetime', form_validator._errors)

    def test_art_start_less_than_dob_invalid(self):
        '''Asserts raises exception if antiretrovirals date first started given
        is less than subject's date of birth.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'art_start_date': get_utcnow().date() - relativedelta(years=30),
            'is_date_estimated': NO,
            'report_datetime': get_utcnow()}
        form_validator = ArvsPrePregnancyFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('art_start_date', form_validator._errors)

    def test_art_start_more_than_dob_valid(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'art_start_date': get_utcnow().date(),
            'is_date_estimated': NO,
            'report_datetime': get_utcnow()}
        form_validator = ArvsPrePregnancyFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
