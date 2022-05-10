from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase,tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE

from ..form_validators import MaternalArvDuringPregFormValidator
from .models import ArvsPrePregnancy, SubjectConsent, FlourishConsentVersion
from .models import MaternalVisit, Appointment
from .test_model_mixin import TestModeMixin

@tag('mdp')
class TestMaternalArvDuringPregForm(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(MaternalArvDuringPregFormValidator, *args, **kwargs)

    def setUp(self):

        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_identifier = '11111111'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(),)

        self.appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000M')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=self.appointment,
            subject_identifier=self.subject_consent.subject_identifier)

        self.arvs_pre_preg = ArvsPrePregnancy.objects.create(
            maternal_visit=self.maternal_visit,
            preg_on_art=YES)

    def test_medication_interrupted_invalid(self):
        '''Assert raises if arvs was interrupted but
        no reasons were given.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_interrupt': YES,
            'interrupt': 'reason',
        }
        form_validator = MaternalArvDuringPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_medication_interrupted_invalid_yes(self):
        '''Assert raises if arvs was interrupted but
        no reason was given.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_interrupt': YES,
            'interrupt': NOT_APPLICABLE,
        }
        form_validator = MaternalArvDuringPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('interrupt', form_validator._errors)

    def test_medication_interrupted_valid(self):
        '''True if arvs was not interrupted and no
        interrupt reason was provided.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_interrupt': NO,
            'interrupt': NOT_APPLICABLE,
            'report_datetime': get_utcnow()
        }
        form_validator = MaternalArvDuringPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised. Got {e}')

    def test_medication_interrupted_invalid_none(self):
        '''Assert raises if no interruptions but
        reason is given.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_interrupt': NO,
            'interrupt': 'reason',
        }
        form_validator = MaternalArvDuringPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('interrupt', form_validator._errors)

    def test_took_arv_preg_on_art_invalid(self):
        '''Assert raises if preg on art but took arv is `NO`.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_interrupt': NO,
            'interrupt': NOT_APPLICABLE,
            'took_arv': NO
        }
        form_validator = MaternalArvDuringPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('took_arv', form_validator._errors)

    def test_took_arv_preg_on_art_valid(self):
        '''True if preg on art and took arv.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_interrupt': NO,
            'interrupt': NOT_APPLICABLE,
            'took_arv': YES
        }
        form_validator = MaternalArvDuringPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised. Got {e}')
       
          
    def test_pre_preg_not_valid(self):
        '''Assert pre preg is not filled when updating arv during pregnancy.
        '''

        ArvsPrePregnancy.objects.all().delete()
        
        appt = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2000D')
        
        visit = MaternalVisit.objects.create(
            appointment=appt,
            subject_identifier=self.subject_consent.subject_identifier)
       
        cleaned_data = {
            'maternal_visit': visit,
            'is_interrupt': NO,
            'interrupt': NOT_APPLICABLE,
            'took_arv': YES
        }
        
        form_validator = MaternalArvDuringPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        
            
    def test_pre_preg_valid(self):
        '''Raise error when pre preg is valid when updating arv during pregnancy.
        '''
        
        appt = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2000D')
        
        visit = MaternalVisit.objects.create(
            appointment=appt,
            subject_identifier=self.subject_consent.subject_identifier)
       
        cleaned_data = {
            'maternal_visit': visit,
            'is_interrupt': NO,
            'interrupt': NOT_APPLICABLE,
            'took_arv': YES
        }
        
        form_validator = MaternalArvDuringPregFormValidator(
            cleaned_data=cleaned_data)
        
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised. Got {e}')
