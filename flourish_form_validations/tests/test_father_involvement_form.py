from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS, NEG
from ..form_validators import RelationshipFatherInvolmentFormValidator
from flourish_form_validations.tests.test_model_mixin import TestModeMixin
from .models import (FlourishConsentVersion, SubjectConsent,
                     Appointment, MaternalVisit, ListModel)
from dateutil.relativedelta import relativedelta
from edc_constants.constants import OTHER



@tag('rfi')
class TestRelationshipFatherInvolment(TestModeMixin,TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(RelationshipFatherInvolmentFormValidator, *args, **kwargs)
        
    def setUp(self):
        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111',
            screening_identifier='ABC12345',
            gender='F',
            dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(),
            version='1')

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2001M')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow())

        self.options = {
            'maternal_visit': self.maternal_visit,
        }
        
        """Test criteria's
        -form valid
        -Q1
        -Q5
        -Q6
        -Q10
        -Q25
        """
    def test_father_involvement_form_valid(self):
        
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'all_measurements': NO,
            
        }    
            
        form_validator = RelationshipFatherInvolmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}') 
    
        
        
        
        
        