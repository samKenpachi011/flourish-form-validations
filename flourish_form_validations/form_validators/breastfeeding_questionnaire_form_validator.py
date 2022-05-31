from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin
from edc_constants.constants import OTHER, YES, NO, DWTA 

class BreastFeedingQuestionnaireFormValidator(FormValidatorMixin, FormValidator):
    
    
    def clean(self):
        
        self.validate_during_preg_influencers()
        self.validate_after_delivery_influencers()
        self.validate_infant_feeding_reasons()
        self.validate_hiv_status_known_by_required()
        self.validate_hiv_status_during_preg_required()
        self.validate_influenced_during_preg_required()
        self.validate_feeding_hiv_status()

    def validate_during_preg_influencers(self):
        self.m2m_other_specify(OTHER,
                               m2m_field='during_preg_influencers',
                               field_other='during_preg_influencers_other')
        
    def validate_after_delivery_influencers(self):
        self.m2m_other_specify(OTHER,
                               m2m_field='after_delivery_influencers',
                               field_other='after_delivery_influencers_other')
        
    def validate_infant_feeding_reasons(self):
        self.m2m_other_specify(OTHER,
                               m2m_field='infant_feeding_reasons',
                               field_other='infant_feeding_other')
        
    def validate_hiv_status_known_by_required(self):
        self.required_if(YES,
                         field='hiv_status_during_preg',
                         field_required='hiv_status_known_by')    
        
    def validate_hiv_status_during_preg_required(self):
        self.required_if(YES,
                         field='feeding_hiv_status',
                         field_required='hiv_status_during_preg')   
        
    def validate_influenced_during_preg_required(self):
        self.required_if(NO,
                         field='hiv_status_during_preg',
                         field_required='influenced_during_preg')       
                
    def validate_feeding_hiv_status(self):
        
        status = self.cleaned_data.get('feeding_hiv_status')
        required_fields = ['hiv_status_aware','on_hiv_status_aware']
        for field in required_fields:
            self.required_if_true(status in ['No','Rather not answer'],
                                  field='feeding_hiv_status',
                                  field_required=field)
        
        
        
        
    
        
        
        



