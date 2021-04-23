from edc_constants.constants import YES
from edc_form_validators.form_validator import FormValidator


class SubstanceUseDuringPregFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='smoked_during_preg',
            field_required='smoking_during_preg_freq')

        self.required_if(
            YES,
            field='alcohol_during_pregnancy',
            field_required='alcohol_during_preg_freq')

        self.required_if(
            YES,
            field='marijuana_during_preg',
            field_required='marijuana_during_preg_freq')

        self.required_if(
            YES,
            field='khat_during_preg',
            field_required='khat_during_preg_freq')
