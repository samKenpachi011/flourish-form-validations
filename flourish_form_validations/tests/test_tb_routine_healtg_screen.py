from django.test import TestCase, tag

from django.core.exceptions import ValidationError

from .test_model_mixin import TestModeMixin
from ..form_validators import TbRoutineHealthScreenFormValidator


@tag('screen_location')
class TestTbRoutineHealthScreening(TestModeMixin, TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(TbRoutineHealthScreenFormValidator, *args, **kwargs)

    def test_screen_location(self):
        """
        Raise an error if the screen location other specify field is null
        when screen location is set to other specify
        """

        cleaned_data = {
            'screen_location': 'Other, specify',
            'screen_location_other': None
        }

        form_validator = TbRoutineHealthScreenFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
