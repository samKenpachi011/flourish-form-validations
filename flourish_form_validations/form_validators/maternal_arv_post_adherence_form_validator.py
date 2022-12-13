from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin


class MaternalArvPostAdherenceFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        super().clean()

        self.validate_interruption_reason_against_missed_arv(self.cleaned_data)
        self.validate_other_specify(
            field='interruption_reason',
            other_specify_field='interruption_reason_other'
        )

    def validate_interruption_reason_against_missed_arv(self, cleaned_data):
        if cleaned_data.get('missed_arv') is not None:
            self.applicable_if_true(
                cleaned_data.get('missed_arv') >= 1,
                field_applicable='interruption_reason',
                applicable_msg='Can\'t choose this option when participant has more than one misses',
                not_applicable_msg='Can\'t choose this option when participant has no missed arvs'
            )
