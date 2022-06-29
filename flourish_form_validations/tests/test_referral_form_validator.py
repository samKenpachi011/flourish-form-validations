from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import OTHER

from flourish_form_validations.form_validators.tb_referral_form_validator import \
    TbReferralFormValidator


@tag('xxx')
class TestTbReferralFormValidator(TestCase):

    def test_referral_clinic_other_specify(self):
        cleaned_data = {
            'referral_clinic': OTHER,
            'referral_clinic_other': "blah blah"
        }

        form_validator = TbReferralFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
