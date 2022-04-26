from edc_constants.choices import YES
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin


class HIVDisclosureStatusFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        not_required_fields = ['plan_to_disclose', 'reason_not_disclosed']
        for field in not_required_fields:
            self.not_required_if(YES,
                                 field='disclosed_status',
                                 field_required=field)

        self.validate_other_specify(field='reason_not_disclosed')
