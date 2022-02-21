from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow

from .models import SubjectConsent, Appointment, MaternalVisit
from .models import UltraSound
from .test_model_mixin import TestModeMixin
from ..form_validators import ObstericalHistoryFormValidator


@tag('xxx')
class TestObstericalHistoryForm(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(ObstericalHistoryFormValidator, *args, **kwargs)

    def setUp(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow())
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')
        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment)
        self.ultrasound = UltraSound.objects.create(
            maternal_visit=self.maternal_visit, ga_confirmed=20)
        self.ultrasound_model = 'flourish_form_validations.ultrasound'
        ObstericalHistoryFormValidator.ultrasound_model = self.ultrasound_model

    @tag('obx')
    def test_ultrasound_prev_preg_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_pregnancies': 1,
            'pregs_24wks_or_more': 1,
            'lost_before_24wks': 0,
            'lost_after_24wks': 0,
            'live_children': 1,
            'children_died_b4_5yrs': 0,
            'children_deliv_before_37wks': 0,
            'children_deliv_aftr_37wks': 1}
        form_validator = ObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    @tag('obx')
    def test_prev_preg_one_pregs_24wks_or_more_not_one_lost(self):
        '''Asserts raises exception if previous pregnancies is 1
        and and the value of pregnancies 24 weeks or more is not 0.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_pregnancies': 3,
            'pregs_24wks_or_more': 3,
            'lost_before_24wks': 0,
            'lost_after_24wks': 1,
            'live_children': 2}
        form_validator = ObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_lost_after_24wks_valid(self):
        '''Asserts raises exception if previous pregnancies is 1
        and and the value of pregnancies 24 weeks or more is not 0.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_pregnancies': 3,
            'pregs_24wks_or_more': 3,
            'lost_before_24wks': 0,
            'lost_after_24wks': 1,
            'live_children': 2}
        form_validator = ObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_prev_preg_one_lost_after_24wks_not_zero(self):
        '''Asserts raises exception if previous pregnancies is 1
        and and the value of pregnancies lost after 24 weeks is not 0.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_pregnancies': 1,
            'lost_after_24wks': 2}
        form_validator = ObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('__all__', form_validator._errors)

    def test_prev_preg_one(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_pregnancies': 1,
            'lost_after_24wks': 0,
            'lost_before_24wks': 0,
            'pregs_24wks_or_more': 1
        }
        form_validator = ObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        form_validator.validate()

    def test_sum_pregs_lost_before_and_current_preg_sum_not_equal(self):
        '''Asserts raises exception if the sum of pregnancies 24 weeks or more
        and pregnancies lost before 24 weeks is not equals to the value of
        previous pregnancies.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_pregnancies': 2,
            'pregs_24wks_or_more': 1,
            'lost_before_24wks': 2,
            'lost_after_24wks': 1}
        form_validator = ObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_sum_pregs_lost_before_and_current_preg_sum_equal(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_pregnancies': 3,
            'pregs_24wks_or_more': 1,
            'lost_before_24wks': 2,
            'lost_after_24wks': 1}
        form_validator = ObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pregs_24wks_less_than_lost_after(self):
        '''Asserts raises exception if pregnancies 24 weeks or more
        is less than pregnancies lost before 24 weeks.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_pregnancies': 4,
            'pregs_24wks_or_more': 2,
            'lost_before_24wks': 2,
            'lost_after_24wks': 2}
        form_validator = ObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_sum_pregs_24wks_not_less_than_lost_after(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_pregnancies': 23,
            'pregs_24wks_or_more': 21,
            'lost_before_24wks': 2,
            'lost_after_24wks': 2}
        form_validator = ObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_sum_deliv_37wks_invalid(self):
        '''Asserts raises exception if the sum of Q8 and Q9 is not equal to'
        '(Q2 -1) - (Q4 + Q5)'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'children_deliv_before_37wks': 7,
            'children_deliv_aftr_37wks': 5,
            'lost_before_24wks': 1,
            'lost_after_24wks': 2,
            'pregs_24wks_or_more': 4,
            'prev_pregnancies': 15}
        form_validator = ObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_sum_deliv_37wks_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'children_deliv_before_37wks': 3,
            'children_deliv_aftr_37wks': 2,
            'lost_before_24wks': 1,
            'lost_after_24wks': 3,
            'prev_pregnancies': 9,
            'live_children': 5,
            'pregs_24wks_or_more': 8, }
        form_validator = ObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_sum_deliv_37wks_valid_1(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_pregnancies': 2,
            'pregs_24wks_or_more': 2,
            'lost_before_24wks': 0,
            'lost_after_24wks': 1,
            'live_children': 1,
            'children_died_b4_5yrs': 0,
            'children_deliv_before_37wks': 1,
            'children_deliv_aftr_37wks': 0}
        form_validator = ObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
