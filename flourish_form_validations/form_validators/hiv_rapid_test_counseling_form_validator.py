from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .crf_form_validator import CRFFormValidator


class HIVRapidTestCounselingFormValidator(CRFFormValidator, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.required_if(
            YES,
            field='rapid_test_done',
            field_required='result_date',
            required_msg=('If a rapid test was processed, what is '
                          f'the result date of the rapid test?'),
            not_required_msg=('If a rapid test was not processed, '
                              f'please do not provide the result date.'),
            inverse=True)

        self.required_if(
            YES,
            field='rapid_test_done',
            field_required='result',
            required_msg=('If a rapid test was processed, what is '
                          f'the result of the rapid test?'),
            not_required_msg=('If a rapid test was not processed, '
                              f'please do not provide the result.'),
            inverse=True)

        self.validate_test_date(self.cleaned_data.get('result_date'))

    def validate_test_date(self, test_date=None):

        if test_date and relativedelta(get_utcnow().date(), test_date).months >= 3:
            message = {'result_date': 'The date provided is more than 3 months old.'}
            self._errors.update(message)
            raise ValidationError(message)
