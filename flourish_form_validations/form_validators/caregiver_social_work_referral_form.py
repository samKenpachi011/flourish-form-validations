from django import forms
from edc_constants.constants import OTHER
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin


class CaregiverSocialWorkReferralFormValidator(FormValidatorMixin,FormValidator):
    
    def clean(self):
        
        self.validate_referral_reason()

    def validate_referral_reason(self):
        self.m2m_other_specify(OTHER,
                               m2m_field='referral_reason',
                               field_other='reason_other')
        
        