from edc_constants.constants import YES
from edc_form_validators import FormValidator

from flourish_form_validations.form_validators import FormValidatorMixin


class HITSScreeningFormValidator(FormValidatorMixin, FormValidator):
    def clean(self):
        fields = ['physical_hurt', 'insults', 'threaten', 'screem_curse']

        for field in fields:
            self.required_if(
                YES,
                field=field,
                field_required='in_relationship')
