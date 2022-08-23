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
            visit_code='1000')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow())

                
        """ Validations
        
        -If ‘Yes’ to Q1, continue to Q2, 
        -If “No” to Q1, provide short answer stem question “Why not?” (allow free text) otherwise skip to Q23
        -If “No” to Q5, provide short answer stem question “Why not?” (allow free text) otherwise skip to Q6
        -If “Yes” on Q6 go to Q7
            If “No” skip to Q8
        -If “Yes” to Q10, continue to Q11. Otherwise skip to Q12


        -test validate_why_partner_upsent_required on YES and NO --done
        -test validate_why_not_living_with_partner --done
        -test validate_is_partner_the_father_required --done
        -test validate_not_living_with_partner_required --done
        -test validate_discussion_with_partner_required --done
        -test validate_disclose_status_required  --done
        -test validate_times_separated_required --done
        -test validate_separation_consideration_required --done
        -test partner_cell  --done


        """  
              
    def test_father_involvement_form_valid(self):
        
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'is_partner_the_father': YES,
            'duration_with_partner_months': '1',
            'duration_with_partner_years': '1',
            'partner_age_in_years':'30',
            'living_with_partner': YES,
            'disclosure_to_partner': YES,
            'discussion_with_partner': 'easy',
            'partners_support':'supportive',
            'ever_separated': YES,
            'times_separated': '4',
            'after_fight':'occasionally',
            'relationship_progression':'occasionally',
            'confide_in_partner':'occasionally',
            'relationship_regret':'occasionally',
            'quarrel_frequency':'occasionally',
            'bothering_partner':'occasionally',
            'kissing_partner':'occasionally',
            'engage_in_interests':'occasionally',
            'happiness_in_relationship':'happy',
            'future_relationship':'happy',
            'fathers_financial_support':'supportive',
            'child_left_alone':3,
            'read_books':'mother',
            'told_stories':'mother',
            'sang_songs':'mother',
            'took_child_outside':'mother',
            'played_with_child':'mother',
            'named_with_child':'mother',
            'interview_participation':YES,
            'contact_info': YES,
            'partner_cell': '1212344'
            
        } 
            
        form_validator = RelationshipFatherInvolmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}') 
        

    def test_father_involvement_partner_upresent_form_valid(self):
        
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present':NO,
            'why_partner_upsent':'test',
            'father_child_contact':'test',
            'fathers_financial_support':'supportive',
            'child_left_alone':3,
            'read_books':'mother',
            'told_stories':'mother',
            'sang_songs':'mother',
            'took_child_outside':'mother',
            'played_with_child':'mother',
            'named_with_child':'mother',

        } 
            
        form_validator = RelationshipFatherInvolmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}') 
           
    def test_is_partner_the_father_invalid(self):
        
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'is_partner_the_father': None
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('is_partner_the_father', form_validator._errors)
       
    def test_is_partner_the_father_valid(self):
        
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'is_partner_the_father': YES
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}') 
         
        
    def test_why_not_living_with_partner_invalid(self):
        
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'living_with_partner': NO,
            'is_partner_the_father':YES,
            'why_not_living_with_partner': None
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('why_not_living_with_partner', form_validator._errors)
    
    def test_why_not_living_with_partner_valid(self):
        
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'living_with_partner': NO,
            'is_partner_the_father':YES,
            'why_not_living_with_partner': 'test',
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}') 
    

    def test_discussion_with_partner_invalid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'living_with_partner': YES,
            'is_partner_the_father':YES,
            'disclosure_to_partner': YES,
            'discussion_with_partner': None,   
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('discussion_with_partner', form_validator._errors)
        
        

    def test_disclose_status_invalid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'living_with_partner': YES,
            'is_partner_the_father':YES,
            'disclosure_to_partner': NO,
            'disclose_status': None,     
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('disclose_status', form_validator._errors)
    
         
    def test_discussion_with_partner_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'living_with_partner': YES,
            'is_partner_the_father':YES,
            'disclosure_to_partner': YES,
            'discussion_with_partner': 'easy',   
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}') 
       
       
    def test_disclose_status_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'living_with_partner': YES,
            'is_partner_the_father':YES,
            'disclosure_to_partner': NO,
            'disclose_status': YES, 
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}') 
    
                
    def test_times_separated_invalid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'living_with_partner': YES,
            'is_partner_the_father':YES,
            'ever_separated': YES,
            'times_separated': None,  
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('times_separated', form_validator._errors)  
                   
    def test_separation_consideration_invalid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'living_with_partner': YES,
            'is_partner_the_father':YES,
            'ever_separated': NO,
            'separation_consideration': None,
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('separation_consideration', form_validator._errors)        
    
           
    def test_times_separated_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'living_with_partner': YES,
            'is_partner_the_father':YES,
            'ever_separated': YES,
            'times_separated': '4',       
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}') 
    
               
    def test_separation_consideration_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'living_with_partner': YES,
            'is_partner_the_father':YES,
            'ever_separated': NO,
            'separation_consideration': 'never',
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Go{e}')           
    
    
    def test_partner_cell_invalid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'living_with_partner': YES,
            'is_partner_the_father':YES,
            'contact_info': YES,
            'partner_cell': None,
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('partner_cell', form_validator._errors)   
        
    def test_partner_cell_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'living_with_partner': YES,
            'is_partner_the_father':YES,
            'contact_info': YES,
            'partner_cell': '12345',
        }
        
        form_validator = RelationshipFatherInvolmentFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Go{e}')               
            