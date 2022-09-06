from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from .models import MaternalVisit, Appointment
from edc_base.utils import get_utcnow
from django.test import TestCase, tag
from edc_constants.constants import OTHER, YES

from ..form_validators import MaternalArvPostAdherenceFormValidator
from .models import SubjectConsent, FlourishConsentVersion

@tag('mapa')
class TestMaternalArvPostAdherenceFormValidator(TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(MaternalArvPostAdherenceFormValidator, *args, **kwargs)
        
    def setUp(self):
        
        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_identifier = '11111111'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='3')
        
        self.appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000M')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=self.appointment,
            subject_identifier=self.subject_consent.subject_identifier)
        
        
        
        
        
            
    
    
    