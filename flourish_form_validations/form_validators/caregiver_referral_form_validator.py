from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin


class CaregiverReferralFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.validate_other_specify(field='referred_to')
