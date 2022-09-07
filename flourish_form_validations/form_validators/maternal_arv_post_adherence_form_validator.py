from edc_form_validators import FormValidator
from edc_constants.constants import OTHER, YES, POS, NEG
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class MaternalArvPostAdherenceFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        
        missed_arv_doses = self.cleaned_data.get('missed_arv_doses')
        self.applicable_if_true(missed_arv_doses>=1,
                                field_applicable='missed_arv_doses_reason',
                              )
        
        self.validate_other_specify(field='missed_arv_doses_reason',
                            other_specify_field='missed_arv_doses_reason_other')
