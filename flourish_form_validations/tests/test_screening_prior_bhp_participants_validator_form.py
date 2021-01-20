from django.core.exceptions import ValidationError
from django.test import TestCase

from edc_constants.constants import NO, UNKNOWN, YES
from  edc_form_validators import FormValidator

from ..form_validators import ScreeningPriorBhpParticipantsFormValidator


class TestScreeningPriorBhpParticipantsForm(TestCase):

    def setUp(self):

        self.options = {
            'study_child_identifier': '12345',
            'child_alive': YES,
            'mother_alive': YES,
            'flourish_interest': None,
            'age_assurance': None,
            'flourish_participation': 'interested',
        }

    def test_form_valid(self):
        """
        Checks form saves successfully with all necessary field
        values completed.
        """
        form_validator = ScreeningPriorBhpParticipantsFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_interested_caregiver_to_participate(self):
        """
        Test if interested caregiver is eligible to part in the
        Flourish study
        """
        self.options['mother_alive'] = NO
        self.options['flourish_interest'] = YES
        self.options['age_assurance'] = YES
        form_validator = ScreeningPriorBhpParticipantsFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
