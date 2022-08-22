from edc_form_validators import FormValidator
from edc_constants.constants import OTHER, YES, POS, NEG, NO
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class RelationshipFatherInvolmentFormValidator(FormValidatorMixin,FormValidator):
    
    
    def clean(self):
        super().clean()
        
        self.validate_why_partner_upsent_required()
        self.validate_not_living_with_partner_required()
        self.validate_discussion_with_partner_required()
        self.validate_disclose_status_required()
        self.validate_times_separated_required()
        self.validate_separation_consideration_required()
        self.validate_partner_upsent_fields_not_required()
        self.validate_is_partner_the_father_required()
    
        
        
    # On yes    
        
    def validate_is_partner_the_father_required(self):
        self.required_if(YES,
                         field='partner_present',
                         field_required='is_partner_the_father')
        
    def validate_why_not_living_with_partner_required(self):
        self.required_if(YES,
                         field='living_with_partner',
                         field_required='why_not_living_with_partner') 
        
    def validate_discussion_with_partner_required(self):
        self.required_if(YES,
                         field='disclosure_to_partner',
                         field_required='discussion_with_partner')      
        
    def validate_separation_consideration_required(self):
        self.required_if(YES,
                         field='ever_separated',
                         field_required='separation_consideration')      
               
        
        
    #If “No” to Q1, provide short answer stem question “Why not?”
    def validate_why_partner_upsent_required(self):
        required_fields = ['why_partner_upsent', 'father_child_contact']
        for field in required_fields:
            self.required_if(NO,
                            field='partner_present',
                            field_required=field)
        
    def validate_not_living_with_partner_required(self):
        self.required_if(NO,
                         field='living_with_partner',
                         field_required='why_not_living_with_partner') 
           
    # If “Yes” on Q6 go to Q7  If “No” skip to Q8    
    def validate_disclose_status_required(self):
        self.required_if(NO,
                         field='disclosure_to_partner',
                         field_required='disclose_status')  
        
    # If “Yes” to Q10, continue to Q11. Otherwise skip to Q12 
    
    def validate_times_separated_required(self):
        self.required_if(NO,
                         field='ever_separated',
                         field_required='times_separated')  
        
        
    # validate on Q1 no
    def validate_partner_upsent_fields_not_required(self):
        not_required_fields = ['is_partner_the_father',
                               'duration_with_partner_months',
                               'duration_with_partner_years',
                               'partner_age_in_years',
                               'living_with_partner',
                               'why_not_living_with_partner',
                               'disclosure_to_partner',
                               'discussion_with_partner',
                               'disclose_status',
                               'partners_support',
                               'ever_separated',
                               'times_separated',
                               'separation_consideration',
                               'after_fight',
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

        for not_required in not_required_fields:
            self.not_required_if(
                NO,
                field='partner_present',
                field_required=not_required,
                )
        
        
        
        