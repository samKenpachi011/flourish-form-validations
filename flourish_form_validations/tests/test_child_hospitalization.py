from unittest import TestCase

from django.core.exceptions import ValidationError
from edc_constants.constants import NO

from flourish_form_validations.form_validators import \
    ChildHospitalizationFormValidations
from flourish_form_validations.tests.test_model_mixin import TestModeMixin


class TestChildHospitalization(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(ChildHospitalizationFormValidations, *args, **kwargs)

    def test_hospitalization_number(self):
        """
        Raise an error if the hospitalisation number is entered when
        the participant was not hospitalized
        """

        cleaned_data = {
            'hospitalized': NO,
            'number_hospitalised': 2
        }

        form_validator = ChildHospitalizationFormValidations(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
