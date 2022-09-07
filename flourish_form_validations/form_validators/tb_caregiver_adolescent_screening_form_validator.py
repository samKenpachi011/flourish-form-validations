from edc_form_validators import FormValidator
from edc_constants.constants import OTHER, YES, POS, NEG, NO
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class TBCaregiverAdolescentScreeningFormValidator(FormValidatorMixin,FormValidator):
    
    
    def clean(self):
        super().clean()
        
        self.required_if(NO,
                         field='tb_caregiver_participation',
                         field_required='reason_for_not_participating')

        self.validate_other_specify(field='reason_for_not_participating',
                                    other_specify_field='reason_for_not_participating_other')
        
        
        self.required_if(NO,
                         field='tb_caregiver_participation',
                         field_required='reason_for_not_participating')

        
        
        
        
        
        