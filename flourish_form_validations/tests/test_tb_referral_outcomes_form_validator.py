from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import YES, NO, OTHER

from ..form_validators import TbReferralOutcomesFormValidator
from .models import ListModel
from .test_model_mixin import TestModeMixin


@tag('tbrof')
class TestTbReferralOutcomesFormValidator(TestModeMixin, TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(TbReferralOutcomesFormValidator, *args, **kwargs)

    def test_referral_clinic_appt_required_valid(self):
        """
        Raise error if referral_clinic_appt is Yes and fields further_tb_eval , tb_diagnostic_perf,
         'tb_treat_start', 'tb_prev_therapy_start' are null
        """
        ListModel.objects.create(short_name="sputum")
        cleaned_data = {
            'referral_clinic_appt': YES,
            'further_tb_eval': YES,
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

    def test_referral_clinic_appt_required_invalid(self):
        """
        Raise error if referral_clinic_appt is No and fields further_tb_eval , tb_diagnostic_perf,
         'tb_treat_start', 'tb_prev_therapy_start' are not null
        """
        ListModel.objects.create(short_name="sputum")
        cleaned_data = {
            'referral_clinic_appt': NO,
            'further_tb_eval': None,
            'tb_diagnostic_perf': YES,
            'tb_treat_start': NO,
            'tb_prev_therapy_start': YES,
            'tb_diagnose_pos': YES,
            'tb_test_results': "thiiis ",
            'tb_diagnostics': ListModel.objects.all()
        }

        form_validator = TbReferralOutcomesFormValidator(
            cleaned_data=cleaned_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('tb_diagnostic_perf', form_validator._errors)

    def test_tb_diagnostics_other_specify(self):
        """
         Raise error if tb_diagnostics is Other and tb_diagnostics_other is null
         """
        ListModel.objects.create(short_name=OTHER)
        cleaned_data = {
            'referral_clinic_appt': YES,
            'further_tb_eval': YES,
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
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('tb_diagnostics_other', form_validator._errors)

    def test_referral_tb_diagnostic_perf_not_required(self):
        """
        Raise error if tb_diagnostic_perf is NO and tb_diagnose_pos is provided
        """

        cleaned_data = {
            'referral_clinic_appt': YES,
            'further_tb_eval': YES,
            'tb_diagnostic_perf': NO,
            'tb_treat_start': NO,
            'tb_prev_therapy_start': YES,
            'tb_diagnose_pos': YES,
            'tb_test_results': "thiiis ",
            'tb_diagnostics': ListModel.objects.all(),
            'tb_diagnostics_other': None,
        }

        form_validator = TbReferralOutcomesFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('tb_diagnose_pos', form_validator._errors)

    def test_referral_tb_diagnostic_perf_required(self):
        """
        Raise error if tb_diagnostic_perf is Yes and tb_diagnose_pos is provided
        """
        ListModel.objects.create(short_name="sputum")
        cleaned_data = {
            'referral_clinic_appt': YES,
            'further_tb_eval': YES,
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

    def test_referral_tb_diagnose_pos_required(self):
        """
        Raise error if tb_diagnose_pos is No and tb_test_results is provided
        """
        ListModel.objects.create(short_name="sputum")
        cleaned_data = {
            'referral_clinic_appt': YES,
            'further_tb_eval': YES,
            'tb_diagnostic_perf': YES,
            'tb_treat_start': NO,
            'tb_prev_therapy_start': YES,
            'tb_diagnose_pos': NO,
            'tb_test_results': "thiiis ",
            'tb_diagnostics': ListModel.objects.all(),
            'tb_diagnostics_other': None,
        }

        form_validator = TbReferralOutcomesFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('tb_test_results', form_validator._errors)
