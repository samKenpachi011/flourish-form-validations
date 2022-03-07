from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow

from ..form_validators import TbRoutineHealthScreenFormValidator
from .models import FlourishConsentVersion, SubjectConsent
from .test_model_mixin import TestModeMixin


@tag('screen_location')
class TestTbRoutineHealthScreening(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(TbRoutineHealthScreenFormValidator, *args, **kwargs)

    def setUp(self):

        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_identifier = '11111111'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='1')

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
