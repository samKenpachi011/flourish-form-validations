from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import NO, OTHER, YES

from ..form_validators import TbStudyEligibilityFormValidator


class TestTbStudyEligibilityFormValidator(TestCase):

    def test_reasons_not_participating_required(self):
        """
        Test if  reasons for not participating are needed if the participant
        does not want to take part in the study
        """
        cleaned_data = {
            'tb_participation': YES,
            'reasons_not_participating': 'blah blah',
        }

        form_validator = TbStudyEligibilityFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reasons_not_participating', form_validator._errors)

    def test_reasons_not_participating_required_other(self):
        """
        checks if the field for other reasons for not participating ton the study is
        required of the participant selects their reason as `Other`
        """
        cleaned_data = {
            'reasons_not_participating': 'Still thinking',
            'tb_participation': NO,
            'reasons_not_participating_other': 'None'
        }

        form_validator = TbStudyEligibilityFormValidator(
            cleaned_data=cleaned_data
        )

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reasons_not_participating_other', form_validator._errors)
