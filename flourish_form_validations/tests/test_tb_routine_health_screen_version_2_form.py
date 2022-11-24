from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import TbRoutineHealthScreenVersionTwoFormValidator
from .models import FlourishConsentVersion, SubjectConsent
from .test_model_mixin import TestModeMixin


@tag('tbhe')
class TestTbRoutineHealthScreening(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(TbRoutineHealthScreenVersionTwoFormValidator, *args, **kwargs)

    def setUp(self):

        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_identifier = '11111111'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='1')

    def test_tb_health_visits(self):
        """
        Raise an error if tb_health_visits has a response of 1 or greater
        and other fields are required
        """

        cleaned_data = {
            'tb_health_visits': '1',
            'tb_screened': YES,
            'screen_location': None,
            'screen_location_other': 'some place',
            'diagnostic_referral': YES
        }

        form_validator = TbRoutineHealthScreenVersionTwoFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_screen_location(self):
        """
        Raise an error if the screen location other specify field is null
        when screen location is set to other specify
        """

        cleaned_data = {
            'screen_location': None,
            'screen_location_other': 'some place'
        }

        form_validator = TbRoutineHealthScreenVersionTwoFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

