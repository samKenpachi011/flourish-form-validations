from django.apps import apps as django_apps
from django.forms import ValidationError
from django.conf import settings
from edc_form_validators import FormValidator
from edc_constants.constants import OTHER, YES, POS, NEG, NO, NOT_APPLICABLE
from edc_form_validators import FormValidator
from flourish_caregiver.helper_classes import MaternalStatusHelper
from .crf_form_validator import FormValidatorMixin


class RelationshipFatherInvolvementFormValidator(FormValidatorMixin,FormValidator):
        
    
    def clean(self):
        
        
        self.validate_required_fields()
        
        self.required_if(NO,
                        field='partner_present',
                        field_required='why_partner_absent')
        
        self.required_if(NO,
                         field='living_with_partner',
                         field_required='why_not_living_with_partner') 
        
        self.required_if(YES,
                         field='disclosure_to_partner',
                         field_required='discussion_with_partner')    


        self.required_if(YES,
                        field='partner_present',
                        field_required='is_partner_the_father')
        
  
        
        self.required_if(YES,
                         field='ever_separated',
                         field_required='times_separated')     

        self.required_if(YES,
                    field='contact_info',
                    field_required='partner_cell')   
               

        

        
        self.not_required_if(YES,
                         field='partner_present',
                         field_required='why_partner_absent') 
  

    
        self.required_if(NO,
                         field='ever_separated',
                         field_required='separation_consideration')
        
        self.validate_positive_mother()
        
        
        self.validate_father_involvement()  
        
        
        super().clean()
        
    def validate_required_fields(self):
        required_fields = [
                'is_partner_the_father',
                'duration_with_partner',
                'partner_age_in_years',
                'living_with_partner',
                'partners_support',
                'ever_separated',
                'separation_consideration',
                'leave_after_fight',
                'relationship_progression',
                'confide_in_partner',
                'relationship_regret',
                'quarrel_frequency',
                'bothering_partner',
                'kissing_partner',
                'engage_in_interests',
                'happiness_in_relationship',
                'future_relationship',
        ]
        
        for field in required_fields:
            self.required_if(YES, field='partner_present', field_required=field)
            
    def validate_father_involvement(self):
        
        
        required_fields = [

            'father_child_contact',
            'fathers_financial_support',
            'child_left_alone',
            'read_books',
            'told_stories',
            'sang_songs',
            'took_child_outside',
            'played_with_child',
            'named_with_child'
        ]
        
        # check if a field is available in the current context
        # incase if some fields are stem questions
        available_required_fields = [f for f in required_fields if f in self.cleaned_data.keys()]
        
        for field in available_required_fields:
            self.required_if(YES, field='biological_father_alive', field_required=field)
        
    def validate_positive_mother(self):
        # Checker when running tests so it does require addition modules
        if settings.APP_NAME != 'flourish_form_validations':

            partner_present = self.cleaned_data.get('partner_present', None)
            maternal_visit = self.cleaned_data.get('maternal_visit')
            helper = MaternalStatusHelper(maternal_visit, maternal_visit.subject_identifier)

            
            fields = ['disclosure_to_partner', 'discussion_with_partner', 'disclose_status']
            
            
            if helper.hiv_status == POS and partner_present == YES:

                for field in fields:
                    self.required_if_true(True, field_required=field)
                    
        
                
        else:
            pass
            