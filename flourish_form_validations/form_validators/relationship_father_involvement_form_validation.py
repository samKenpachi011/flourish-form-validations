from edc_form_validators import FormValidator
from edc_constants.constants import OTHER, YES, POS, NEG
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class RelationshipFatherInvolmentFormValidator(FormValidatorMixin,FormValidator):
    
    def clean(self):
        
        pass