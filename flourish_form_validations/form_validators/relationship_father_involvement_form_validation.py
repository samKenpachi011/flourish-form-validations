from edc_form_validators import FormValidator
from edc_constants.constants import OTHER, YES, POS, NEG, NO
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class RelationshipFatherInvolmentFormValidator(FormValidatorMixin,FormValidator):
    
    
    def clean(self):
        super().clean()
        
        self.validate_partner_absent_fields_not_required()
    
        self.required_if(YES,
                         field='partner_present',
                         field_required='is_partner_the_father')
        
        self.required_if(YES,
                         field='disclosure_to_partner',
                         field_required='discussion_with_partner')      
        
        self.required_if(YES,
                         field='ever_separated',
                         field_required='times_separated')     

        self.required_if(YES,
                    field='contact_info',
                    field_required='partner_cell')   
               
        required_fields = ['why_partner_absent', 'father_child_contact']
        for field in required_fields:
            self.required_if(NO,
                            field='partner_present',
                            field_required=field)
        
        self.required_if(NO,
                         field='living_with_partner',
                         field_required='why_not_living_with_partner') 
  
        self.required_if(NO,
                         field='disclosure_to_partner',
                         field_required='disclose_status')  
    
        self.required_if(NO,
                         field='ever_separated',
                         field_required='separation_consideration')  

    def validate_partner_absent_fields_not_required(self):
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
                                'interview_participation',
                                'contact_info',
                                'partner_cell'
                               ]

        for not_required in not_required_fields:
            self.not_required_if(
                NO,
                field='partner_present',
                field_required=not_required,
            )
               