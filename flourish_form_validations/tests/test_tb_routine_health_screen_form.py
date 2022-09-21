from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import TbRoutineHealthScreenFormValidator
from .models import FlourishConsentVersion, SubjectConsent
from .test_model_mixin import TestModeMixin


@tag('tbhe')
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

    def test_referral_reason_valid(self):
        """
        Assert form does not raise an error if the referral reason is not None
         if diagnostic referral is Yes
        """

        cleaned_data = {
            'tb_screened': YES,
            'screen_location': 'blah',
            'pos_screen': 'blah',
            'diagnostic_referral': YES,
            'referral_reason': 'blah blah blah'
        }

        form_validator = TbRoutineHealthScreenFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_referral_reason_invalid(self):
        """
        Assert form raises an error if the referral reason is None
         if diagnostic referral is Yes
        """

        cleaned_data = {
            'tb_screened': YES,
            'screen_location': 'blah',
            'pos_screen': 'blah',
            'diagnostic_referral': YES,
            'referral_reason': None
        }

        form_validator = TbRoutineHealthScreenFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_reason', form_validator._errors)

    def test_referral_reason_valid2(self):
        """
        Assert form does not raise an error if the referral reason is None
         and diagnostic referral is No
        """

        cleaned_data = {
            'tb_screened': YES,
            'screen_location': 'blah',
            'pos_screen': 'blah',
            'diagnostic_referral': NO,
            'referral_reason': None
        }

        form_validator = TbRoutineHealthScreenFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_referral_reason_invalid2(self):
        """
        Assert form does not raise an error if the referral reason is None
         and diagnostic referral is No
        """

        cleaned_data = {
            'tb_screened': YES,
            'screen_location': 'blah',
            'pos_screen': 'blah',
            'diagnostic_referral': NO,
            'referral_reason': 'blah blah blah'
        }

        form_validator = TbRoutineHealthScreenFormValidator(
            cleaned_data=cleaned_data
        )

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('referral_reason', form_validator._errors)
