from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from edc_constants.constants import NO, UNKNOWN, NOT_APPLICABLE


class ScreeningPriorBhpParticipantsFormValidator(FormValidator):

    def clean(self):
        self.validate_mother_alive()
        self.validate_participation()

    def validate_mother_alive(self):

        self.required_if(
            *[NO, UNKNOWN],
            field='mother_alive',
            field_required='flourish_interest')

    def validate_participation(self):
        cleaned_data = self.cleaned_data
        mother_alive = cleaned_data.get('mother_alive')
        flourish_interest = cleaned_data.get('flourish_interest')
        if mother_alive == NO and flourish_interest == NO:
            if cleaned_data.get('flourish_participation') != NOT_APPLICABLE:
                message = {'flourish_participation':
                           'This field is not applicable'}
                self._errors.update(message)
                raise ValidationError(message)
        else:
            if cleaned_data.get('flourish_participation') == NOT_APPLICABLE:
                message = {'flourish_participation':
                           'This field is applicable'}
                self._errors.update(message)
                raise ValidationError(message)
