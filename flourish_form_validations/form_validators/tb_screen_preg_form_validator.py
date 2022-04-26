from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin


class TbScreenPregFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.required_if(
            YES,
            field='tb_screened',
            field_required='where_screened')

        self.validate_other_specify(field='where_screened')
