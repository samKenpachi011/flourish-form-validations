from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import NO, YES, OTHER

from ..form_validators.tb_study_eligibility_form_validator import \
    TbStudyEligibilityFormValidator


class TestTbStudyEligibilityFormValidator(TestCase):


    def test_reasons_not_participating_required(self):
        cleaned_data = {
            'reasons_not_participating': 'YES',
            'tb_participation': NO
        }

        form_validator = TbStudyEligibilityFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_reasons_not_participating_required_other(self):
        cleaned_data = {
            'reasons_not_participating': OTHER,
            'tb_participation': YES,
            'reasons_not_participating_other': 'None'
        }

        form_validator = TbStudyEligibilityFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
