from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import NO

from ..form_validators import TbVisitScreeningWomenFormValidator
from .models import SubjectConsent, FlourishConsentVersion
from .test_model_mixin import TestModeMixin


@tag('tb_visit')
class TestTbVisitScreeningWomen(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(TbVisitScreeningWomenFormValidator, *args, **kwargs)

    def setUp(self):

        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_identifier = '11111111'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='1')

    def test_have_cough(self):
        """
        Raise an error if cough duration is captured when the subject did not answer yes
        to have a cough question
        """

        cleaned_data = {
            'have_cough': NO,
            'cough_duration': None
        }

        form_validator = TbVisitScreeningWomenFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_cough_intersects_preg(self):
        """
        Raise an error if cough duration is captured when the subject did not answer yes
        to have a cough question
        """

        cleaned_data = {
            'cough_intersects_preg': NO,
            'cough_timing': 'month'
        }

        form_validator = TbVisitScreeningWomenFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_fever(self):
        """
        Raise an error if fever timing is captured when the subject did not answer yes
        to have a a fever during preg
        """

        cleaned_data = {
            'fever_during_preg': NO,
            'fever_timing': None
        }

        form_validator = TbVisitScreeningWomenFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_night_sweats(self):
        """
        Raise an error if night sweat timing is captured when the subject did not answer
        yes to have a night sweat postpartum
        """

        cleaned_data = {
            'night_sweats_postpartum': NO,
            'night_sweats_timing': None
        }

        form_validator = TbVisitScreeningWomenFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_weight_loss(self):
        """
        Raise an error if weight loss timing is captured when the subject did not answer
        yes to have a weight loss postpartum
        """

        cleaned_data = {
            'weight_loss_postpartum': NO,
            'weight_loss_timing': None
        }

        form_validator = TbVisitScreeningWomenFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_cough_blood(self):
        """
        Raise an error if cough blood timing is captured when the subject did not answer
        yes to have a cough blood postpartum
        """

        cleaned_data = {
            'cough_blood_postpartum': NO,
            'cough_blood_timing': None
        }

        form_validator = TbVisitScreeningWomenFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_enlarged_lymph_nodes(self):
        """
        Raise an error if enlarged lymph nodes timing is captured when the subject did not answer
        yes to have a _enlarged lymph nodes postpartum
        """

        cleaned_data = {
            'enlarged_lymph_nodes_postpartum': NO,
            'lymph_nodes_timing': None
        }

        form_validator = TbVisitScreeningWomenFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
