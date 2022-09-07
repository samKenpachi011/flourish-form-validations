from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from .models import MaternalVisit, Appointment
from edc_base.utils import get_utcnow
from django.test import TestCase, tag
from edc_constants.constants import OTHER, YES, NOT_APPLICABLE, OTHER

from ..form_validators import MaternalArvPostAdherenceFormValidator
from .models import SubjectConsent, FlourishConsentVersion
from .test_model_mixin import TestModeMixin

@tag('mapa')
class TestMaternalArvPostAdherenceFormValidator(TestModeMixin, TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(MaternalArvPostAdherenceFormValidator, *args, **kwargs)
        
    def setUp(self):
        
        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_identifier = '11111111'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='F', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='3')
        
        
        # Enrollement
        self.appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000M')
        

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=self.appointment,
            subject_identifier=self.subject_consent.subject_identifier)
        
        self.options = {
            'report_datetime': get_utcnow(),
            'missed_arv_doses': 0,
            'missed_arv_doses_reason': NOT_APPLICABLE,
            'missed_arv_doses_reason_other': None,
            'comment':'test'   
        }
        
        """Validations
        
        -test form validate
        -test form invalid
        -test missed_arv_doses >1 (2 days) to make missed_arv_doses_reason required (form_invalid)
        -test missed_arv_doses = 0 to make missed_arv_doses_reason not applicable
        -test missed_arv_doses_reason_other = other to make other_specify required
        """
        
    def test_post_adherence_form_valid(self):
        
        appt = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2000D')
        
        visit = MaternalVisit.objects.create(
            appointment=appt,
            subject_identifier=self.subject_consent.subject_identifier)
        
        self.options.update({'maternal_visit':visit})
        
        form_validator = MaternalArvPostAdherenceFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raise. Got {e}')    
        
    def test_missed_arv_doses_reason_invalid(self):
        # provide missed_arv_doses_reason without missed_arv_doses being > 1
        
        self.options.update({'missed_arv_doses': 2})
        
        form_validator = MaternalArvPostAdherenceFormValidator(
            cleaned_data=self.options
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('missed_arv_doses_reason', form_validator._errors)
        
    def test_missed_arv_doses_reason_valid(self):
        self.options.update({'missed_arv_doses': 2,
                             'missed_arv_doses_reason':'test'
                             })
        form_validator = MaternalArvPostAdherenceFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raise. Got {e}')  
            
    def test_missed_arv_doses_reason_other_required(self):
        
        self.options.update({'missed_arv_doses': 2,
                             'missed_arv_doses_reason': OTHER
                             })
        
        form_validator = MaternalArvPostAdherenceFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('missed_arv_doses_reason_other', form_validator._errors)
        
        
    def test_missed_arv_doses_reason_other_valid(self):
        
        self.options.update({'missed_arv_doses': 2,
                             'missed_arv_doses_reason': OTHER,
                             'missed_arv_doses_reason_other':'test',
                             })
        
        form_validator = MaternalArvPostAdherenceFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raise. Got {e}')      
        
        
                
            
            
        
           
        
        
        
         
        
        
        
        
        
        
            
    
    
    