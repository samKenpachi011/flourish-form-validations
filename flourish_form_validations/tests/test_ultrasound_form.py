from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow

from .models import SubjectConsent, MaternalVisit, Appointment, FlourishConsentVersion
from .test_model_mixin import TestModeMixin
from ..form_validators import UltrasoundFormValidator, AntenatalEnrollmentFormValidator


@tag('bpd')
class TestUltrasoundForm(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(UltrasoundFormValidator, *args, **kwargs)
        AntenatalEnrollmentFormValidator.antenatal_enrollment_model = \
            'flourish_form_validator.antenatalenrollment'

    def setUp(self):

        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow())

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow())

        self.cleaned_data = {'report_datetime': get_utcnow(),
                             'bpd': 4.2,
                             'hc': 3.1,
                             'ac': 2.1,
                             'fl': 3.2,
                             'amniotic_fluid_volume': '0',
                             'ga_by_lmp': 0,
                             'ga_by_ultrasound_wks': 0,
                             'ga_by_ultrasound_days': 0,
                             'est_fetal_weight': 0,
                             'ga_confirmed': 0,
                             'est_edd_ultrasound': get_utcnow().date(), }

    def test_est_ultrasound_less_than(self):
        self.cleaned_data.update({
            'maternal_visit': self.maternal_visit,
            'est_edd_ultrasound': get_utcnow().date() + relativedelta(days=50),
            'report_datetime': get_utcnow()
        })
        form_validator = UltrasoundFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_est_ultrasound_greater_than(self):
        self.cleaned_data.update({
            'maternal_visit': self.maternal_visit,
            'est_edd_ultrasound': get_utcnow().date() + relativedelta(weeks=60),
            'report_datetime': get_utcnow(),
        })
        form_validator = UltrasoundFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('est_edd_ultrasound', form_validator._errors)

    def test_est_ultrasound_less_than_invalid(self):
        self.cleaned_data.update({
            'maternal_visit': self.maternal_visit,
            'est_edd_ultrasound': get_utcnow().date(),
            'report_datetime': get_utcnow()
        })
        form_validator = UltrasoundFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ga_ultrasound_wks_valid(self):
        self.cleaned_data.update({
            'maternal_visit': self.maternal_visit,
            'ga_by_ultrasound_wks': 35,
            'report_datetime': get_utcnow(),
            'est_edd_ultrasound': get_utcnow().date() + relativedelta(weeks=5),
        })
        form_validator = UltrasoundFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ga_ultrasound_wks_invalid(self):
        self.cleaned_data.update({
            'maternal_visit': self.maternal_visit,
            'ga_by_ultrasound_wks': 50,
            'report_datetime': get_utcnow(),
        })
        form_validator = UltrasoundFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('ga_by_ultrasound_wks', form_validator._errors)

    def test_ga_by_ultrasound_days_valid(self):
        self.cleaned_data.update({
            'maternal_visit': self.maternal_visit,
            'ga_by_ultrasound_days': 6,
            'report_datetime': get_utcnow(),
        })
        form_validator = UltrasoundFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ga_by_ultrasound_against_est_edd_ultrasound_valid(self):
        self.cleaned_data.update({
            'maternal_visit': self.maternal_visit,
            'est_edd_ultrasound': get_utcnow().date() + relativedelta(weeks=5),
            'ga_by_ultrasound_wks': 35,
            'report_datetime': get_utcnow()
        })
        form_validator = UltrasoundFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_bpd(self):
        """
        check if bpd value allows for values below 5
        """
        self.cleaned_data.update({
            'maternal_visit': self.maternal_visit,
            'bpd': 2,
        })

        form_validator = UltrasoundFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_no_gestations_other_fields_not_required(self):
        """
        check if number_of_gestation's is 0, other fields are not required
        """
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'number_of_gestations': 0,
            'ga_by_lmp': 2,
        }

        form_validator = UltrasoundFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('ga_by_lmp', form_validator._errors)

    def test_no_gestations_other_fields_not_required_(self):
        """
        check if number_of_gestation's is 0, other fields are not required
        """
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'number_of_gestations': 0,
            'est_edd_ultrasound': 2,
        }

        form_validator = UltrasoundFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('est_edd_ultrasound', form_validator._errors)
