from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO, OTHER
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class PostHIVRapidTestCounselingFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        for field in ['result_date', 'result']:

            self.required_if(
                YES,
                field='rapid_test_done',
                field_required=field,)

        self.validate_test_date(self.cleaned_data.get('result_date'),)

        self.not_required_if(
            YES,
            field='rapid_test_done',
            field_required='reason_not_tested',)

        self.required_if(
            OTHER,
            field='reason_not_tested',
            field_required='reason_not_tested_other')

    def validate_test_date(self, test_date=None):

        maternal_visit = self.cleaned_data.get('maternal_visit')

        if test_date and relativedelta(
                maternal_visit.report_datetime.date(), test_date).months >= 3:
            message = {
                'result_date': 'The date provided is more than 3 months old.'}
            self._errors.update(message)
            raise ValidationError(message)
