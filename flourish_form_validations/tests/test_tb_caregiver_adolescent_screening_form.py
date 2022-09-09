from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS, NEG
from ..form_validators import TBCaregiverAdolescentScreeningFormValidator
from flourish_form_validations.tests.test_model_mixin import TestModeMixin
from .models import (FlourishConsentVersion, SubjectConsent,
                     Appointment, MaternalVisit, ListModel)
from dateutil.relativedelta import relativedelta
from edc_constants.constants import OTHER



@tag('tbcs') 
class TestTBCaregiverAdolescentScreeningForm(TestModeMixin,TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(TBCaregiverAdolescentScreeningFormValidator, *args, **kwargs)
        
    def setUp(self):

        """Validations
        -test form valid
        -test form invalid (q1 = YES and other is provided
        -test if q1 =NO the the reason is required q2 is required
        -test if q1 =YES then q2 is not applicable 

        """
        
        self.options = {
            'tb_caregiver_participation': YES,
            'reason_for_not_participating': NOT_APPLICABLE,
            'reason_for_not_participating_other': None
            
        }
    @tag('rbcss')    
    def test_caregiver_adolescent_screening_form_on_yes_valid(self):        
        form_validator = TBCaregiverAdolescentScreeningFormValidator(
            cleaned_data=self.options
        ) 
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}') 
            
    def test_caregiver_adolescent_screening_form_on_no_valid(self):  
        
        self.options.update({'tb_caregiver_participation':NO,
                            'reason_for_not_participating':'test'})      
        form_validator = TBCaregiverAdolescentScreeningFormValidator(
            cleaned_data=self.options
        ) 
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}') 
            
    def test_reason_for_not_participating_required(self):
        """
        Tests if reason for not participating is needed if the participant
        does not want to take part in the study
        """
        cleaned_data = {
            'tb_caregiver_participation': NO,
            'reason_for_not_participating': NOT_APPLICABLE,
        }

        form_validator = TBCaregiverAdolescentScreeningFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reason_for_not_participating', form_validator._errors)

    def test_reason_for_not_participating_other_required(self):
        """
        checks if the field for other reasons is provided
        """
        cleaned_data = {
            'tb_caregiver_participation': NO,
            'reason_for_not_participating': OTHER,
            'reason_for_not_participating_other': None
        }

        form_validator = TBCaregiverAdolescentScreeningFormValidator(
            cleaned_data=cleaned_data
        )

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reason_for_not_participating_other', form_validator._errors)
        
    def test_reason_for_not_participating_other_not_required(self):
        """
        checks if the field for other reasons is not required
        """
        cleaned_data = {
            'tb_caregiver_participation': NO,
            'reason_for_not_participating': NOT_APPLICABLE,
            'reason_for_not_participating_other': 'test'
        }

        form_validator = TBCaregiverAdolescentScreeningFormValidator(
            cleaned_data=cleaned_data
        )

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reason_for_not_participating_other', form_validator._errors)
