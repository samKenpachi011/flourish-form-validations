from django.core.exceptions import ValidationError
from django.test import TestCase

from edc_constants.constants import OTHER

from ..form_validators import InPersonContactAttemptFormValidator


class TestInPersonContactAttemptForm(TestCase):

    def setUp(self):

        self.options ={
            'contact_location': 'physical_address',
            'successful_location': 'physical_address',
            'study_maternal_identifier': '12345',
            'phy_addr_unsuc': 'no_one_was_home',
            'phy_addr_unsuc_other': '',
            'workplace_unsuc': 'no_one_was_home',
            'workplace_unsuc_other': '',
            'contact_person_unsuc': 'no_one_was_home',
            'contact_person_unsuc_other': ''
        }

    def test_form_valid(self):
        """
        Checks form saves successfully with all necessary field
        values completed.
        """
        form_validator = InPersonContactAttemptFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
