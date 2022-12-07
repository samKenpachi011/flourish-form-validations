from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, OTHER

from ..form_validators import TbReferralOutcomesFormValidator
from .models import FlourishConsentVersion, SubjectConsent, ListModel
from .test_model_mixin import TestModeMixin


@tag('tbrof')
class TestTbReferralOutcomesFormValidator(TestModeMixin, TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(TbReferralOutcomesFormValidator, *args, **kwargs)

    def setUp(self):
        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_identifier = '11111111'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='1')

    def test_referral_clinic_appt_required(self):
        """
        Raise error if referral_clinic_appt is YES and fields 'tb_diagnostic_perf',
         'tb_treat_start', 'tb_prev_therapy_start' are null
        """

        cleaned_data = {
            'referral_clinic_appt': YES,
        }

        form_validator = TbReferralOutcomesFormValidator(
            cleaned_data=cleaned_data)

        try:
            form_validator.validate()
        except ValidationError as e:
            self.assertRaises(ValidationError)

    def test_referral_clinic_appt_not_required(self):
        """
        Raise error if referral_clinic_appt is NO and other fields are provided
        """

        cleaned_data = {
            'referral_clinic_appt': NO,
        }

        form_validator = TbReferralOutcomesFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_tb_diagnostics_valid(self):
        ListModel.objects.create(short_name="septum")
        cleaned_data = {
            'referral_clinic_appt': YES,
            'tb_diagnostic_perf': YES,
            'tb_treat_start': NO,
            'tb_prev_therapy_start': YES,
            'tb_diagnose_pos': YES,
            'tb_test_results': "thiiis ",
            'tb_diagnostics': ListModel.objects.all()
        }

        form_validator = TbReferralOutcomesFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_tb_diagnostics_other_specify_valid(self):
        ListModel.objects.create(short_name=OTHER)

        cleaned_data = {
            'referral_clinic_appt': YES,
            'tb_diagnostic_perf': YES,
            'tb_treat_start': NO,
            'tb_prev_therapy_start': YES,
            'tb_diagnose_pos': YES,
            'tb_test_results': "thiiis ",
            'tb_diagnostics': ListModel.objects.all(),
            'tb_diagnostics_other': None,
        }
        form_validator = TbReferralOutcomesFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_tb_diagnostics_other_specify_invalid(self):
        ListModel.objects.create(short_name=OTHER)

        cleaned_data = {
            'referral_clinic_appt': YES,
            'tb_diagnostic_perf': YES,
            'tb_treat_start': NO,
            'tb_prev_therapy_start': YES,
            'tb_diagnose_pos': YES,
            'tb_test_results': "thiiis ",
            'tb_diagnostics': ListModel.objects.all(),
            'tb_diagnostics_other': "thiiis",
        }
        form_validator = TbReferralOutcomesFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
