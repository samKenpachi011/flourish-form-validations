from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from edc_constants.constants import NO, YES, UNKNOWN


class ScreeningPriorBhpParticipantsFormValidator(FormValidator):

    def clean(self):

        self.validate_mother_alive()
        self.validate_age_assurance()

    def validate_mother_alive(self):
        mother_alive_options = [NO, UNKNOWN]
        mother_alive = self.cleaned_data.get('mother_alive')

        if mother_alive in mother_alive_options:

            self.required_if(
                NO,
                field='mother_alive',
                field_required='flourish_interest',
                inverse=False)

            self.required_if(
                UNKNOWN,
                field='mother_alive',
                field_required='flourish_interest',
                inverse=False)
        else:
            self.not_required_if(
                YES,
                field='mother_alive',
                field_required='flourish_interest',
                inverse=False)
            self.not_required_if(
                YES,
                field='mother_alive',
                field_required='age_assurance',
                inverse=False)

    def validate_age_assurance(self):

        age_assurance = self.cleaned_data.get('age_assurance')

        if age_assurance == NO:
            message = {'flourish_interest':
                       'Interested Caregiver Is Under-Age'}
            self._errors.update(message)
            raise ValidationError(message)

        self.required_if(
            YES,
            field='flourish_interest',
            field_required='age_assurance',
            inverse=False)
