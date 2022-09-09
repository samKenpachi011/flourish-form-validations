from edc_form_validators import FormValidator
from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class TBCaregiverAdolescentScreeningFormValidator(FormValidatorMixin,FormValidator):
    
    
    def clean(self):
        super().clean()
        

        self.validate_other_specify(field='reason_for_not_participating',
                                    other_specify_field='reason_for_not_participating_other')
        
        
        self.applicable_if(NO,
                         field='tb_caregiver_participation',
                         field_applicable='reason_for_not_participating')
        
        self.not_required_if(YES,
                         field='tb_caregiver_participation',
                         field_required='reason_for_not_participating_other')

        
        
        
        
        
        