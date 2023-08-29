from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import YES, OTHER

from ..form_validators import TbRoutineHealthScreenV2FormValidator
from .models import ListModel
from .test_model_mixin import TestModeMixin


@tag('tbrhsv2')
class TestTbRoutineHealthScreeningV2(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(TbRoutineHealthScreenV2FormValidator, *args, **kwargs)

    def test_screen_location_valid(self):
        """
        Raise an error if screen_location is not selected
        """
        ListModel.objects.create(short_name="sputum")
        cleaned_data = {
            'tb_screened': YES,
            'screen_location': ListModel.objects.all(),
            'screen_location_other': None,
            'pos_screen': YES,
            'diagnostic_referral': YES
        }

        form_validator = TbRoutineHealthScreenV2FormValidator(
            cleaned_data=cleaned_data
        )
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_screen_location_other(self):
        """
        Raise an error if the screen location other specify field is null
        when screen location is set to None
        """
        ListModel.objects.create(short_name=OTHER)
        cleaned_data = {
            'tb_screened': YES,
            'screen_location': ListModel.objects.all(),
            'screen_location_other': 'some place',
            'pos_screen': YES,
            'diagnostic_referral': YES
        }

        form_validator = TbRoutineHealthScreenV2FormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
