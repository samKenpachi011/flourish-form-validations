from edc_constants.constants import YES
from edc_form_validators.form_validator import FormValidator


class SubstanceUsePriorFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='smoked_prior_to_preg',
            field_required='smoking_prior_preg_freq')

        self.required_if(
            YES,
            field='alcohol_prior_pregnancy',
            field_required='alcohol_prior_preg_freq')

        self.required_if(
            YES,
            field='marijuana_prior_preg',
            field_required='marijuana_prior_preg_freq')

        self.required_if(
            YES,
            field='khat_prior_preg',
            field_required='khat_prior_preg_freq')
