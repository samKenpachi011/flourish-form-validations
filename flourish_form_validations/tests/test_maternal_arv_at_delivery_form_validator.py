from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import OTHER, YES

from flourish_form_validations.form_validators.maternal_arv_at_delivery_form_validations import \
    MaternalArvAtDeliveryFormValidations


@tag('arv_delivery')
class TestMaternalArvAtDeliveryFormValidator(TestCase):

    def test_maternal_arv_at_delivery_form_validator(self):
        cleaned_data = {
            'change_reason': OTHER,
            'change_reason_other': 'blah blah',
            'last_visit_change': YES,
        }

        form_validator = MaternalArvAtDeliveryFormValidations(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_resume_treatment(self):
        cleaned_data = {
            'last_visit_change': YES,
            'change_reason': 'NO_REFILL',
            'resume_treat': 'NO_REFILL',
        }

        form_validator = MaternalArvAtDeliveryFormValidations(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
