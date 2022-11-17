from django.core.exceptions import ValidationError
from edc_constants.constants import NOT_APPLICABLE,OTHER
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin


class MaternalArvPostAdherenceFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        super().clean()

        self.validate_other_specify(
            field='screen_location',
            other_specify_field='screen_location_other'
        )
        self.validate_interruption_reason_against_missed_arv()

    def validate_interruption_reason_against_missed_arv(self):

        reason = ['TOXICITY_HEALTHCARE_PROVIDER', 'NO_DRUGS', 'NO_REFILL', 'FORGOT', 'TRAVELING', 'DEFAULT', OTHER]

        if (self.cleaned_data.get('missed_arv') == 0 and
                self.cleaned_data.get('interruption_reason') in reason):
            message = {'interruption_reason': 'can\'t choose this option when participant has no missed arvs'}
            self._errors.update(message)
            raise ValidationError(message)

        elif (self.cleaned_data.get('missed_arv') >= 1 and
              self.cleaned_data.get('interruption_reason') in [NOT_APPLICABLE, 'TOXICITY_SELF']):
            message = {'interruption_reason': 'can\'t choose this option'
                                              ' when participant has more than one misses'}
            self._errors.update(message)
            raise ValidationError(message)

