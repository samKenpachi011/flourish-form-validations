from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, YES

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

    def test_cough(self):
        """
        Raise an error if cough duration is captured when the subject did not answer yes
        to have a cough question
        """

        cleaned_data = {
            'have_cough': YES,
            'cough_intersects_preg': YES,
            'cough_illness': YES,
            'cough_duration_preg': 'month',
            'seek_med_help': 'month',
            'cough_num': 'month',
            'cough_illness_times': 'month',
            'cough_illness_preg': 'month',
            'cough_illness_med_help': 'month',
            'cough_duration': 'month',
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
            'fever_during_preg': YES,
            'fever_illness_postpartum': YES,
            'fever_illness_times': "None",
            'fever_illness_preg': "None",
            'fever_illness_postpartum_times': "None",
            'fever_illness_postpartum_preg': "None",
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
            'night_sweats_during_preg': YES,
            'night_sweats_postpartum': YES,
            'night_sweats_during_preg_times': "None",
            'night_sweats_during_preg_clinic': "None",
            'night_sweats_postpartum_times': "None",
            'night_sweats_postpartum_clinic': "None",
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
            'weight_loss_during_preg': YES,
            'weight_loss_postpartum': YES,
            'weight_loss_during_preg_times': "None",
            'weight_loss_during_preg_clinic': "None",
            'weight_loss_postpartum_times': "None",
            'weight_loss_postpartum_clinic': "None",
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
            'cough_blood_during_preg': YES,
            'cough_blood_postpartum': YES,
            'cough_blood_during_preg_times': "None",
            'cough_blood_during_preg_clinic': "None",
            'cough_blood_postpartum_times': "None",
            'cough_blood_postpartum_clinic': "None",
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
            'enlarged_lymph_nodes_during_preg': YES,
            'enlarged_lymph_nodes_postpartum': YES,
            'enlarged_lymph_nodes_postpartum_times': "None",
            'enlarged_lymph_nodes_postpartum_clinic': "None",
            'enlarged_lymph_nodes_during_preg_times': "None",
            'enlarged_lymph_nodes_during_preg_clinic': "None",
        }

        form_validator = TbVisitScreeningWomenFormValidator(
            cleaned_data=cleaned_data
        )

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
