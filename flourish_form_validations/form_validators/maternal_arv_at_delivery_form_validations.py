from edc_constants.constants import OTHER, YES
from edc_form_validators import FormValidator

from flourish_form_validations.form_validators import FormValidatorMixin


class MaternalArvAtDeliveryFormValidations(FormValidatorMixin, FormValidator):

    def clean(self):
        self.required_if(OTHER,
                         field='change_reason',
                         field_required='change_reason_other')

        self.required_if(YES, field_required='change_reason', field='last_visit_change')

        self.applicable_if_true(
            self.is_arv_treatment(),
            field_applicable='resume_treat'
        )

    def is_arv_treatment(self):
        reasons_changed = self.cleaned_data.get('change_reason')
        return reasons_changed == 'NO_REFILL' or reasons_changed == 'DEFAULT'
