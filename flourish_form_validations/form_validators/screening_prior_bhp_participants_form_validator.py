from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from edc_constants.constants import NO, UNKNOWN, NOT_APPLICABLE, YES


class ScreeningPriorBhpParticipantsFormValidator(FormValidator):

    def clean(self):
        self.validate_child_alive()
        self.applicable_only(
            YES,
            field='flourish_interest',
            field_applicable='flourish_participation')
        self.validate_participation()

    def validate_participation(self):
        cleaned_data = self.cleaned_data
        mother_alive = cleaned_data.get('mother_alive')
        flourish_interest = cleaned_data.get('flourish_interest')
        flourish_participation = cleaned_data.get('flourish_participation')
        if mother_alive:
            self.applicable_only(
                *[NO, UNKNOWN],
                field='mother_alive',
                field_applicable='flourish_interest')

            if mother_alive in [NO, UNKNOWN] and flourish_interest == NO:
                if flourish_participation != NOT_APPLICABLE:
                    message = {'flourish_participation':
                               'This field is not applicable'}
                    self._errors.update(message)
                    raise ValidationError(message)
            if mother_alive in [NO, UNKNOWN] and flourish_interest == YES:
                if flourish_participation == 'interested':
                    message = {'flourish_participation':
                               'The mother from the previous study is not alive, '
                               'Please correct interest for `another caregiver`. '}
                    self._errors.update(message)
                    raise ValidationError(message)
            if mother_alive == YES:
                if flourish_participation == NOT_APPLICABLE:
                    message = {'flourish_participation':
                               'This field is applicable'}
                    self._errors.update(message)
                    raise ValidationError(message)
                if (flourish_interest in [NO, NOT_APPLICABLE]) and (
                     flourish_participation == 'another_caregiver_interested'):
                    message = {'flourish_participation':
                               'The mother from the previous study is alive, '
                               'Please correct interest. '}
                    self._errors.update(message)
                    raise ValidationError(message)
                if flourish_interest == YES and flourish_participation == 'interested':
                    message = {'flourish_participation':
                               'The caregiver is interested in participating in the '
                               'FLOURISH study. Please correct interest. '}
                    self._errors.update(message)
                    raise ValidationError(message)

    def validate_child_alive(self):
        self.not_applicable_if(
            NO,
            field='child_alive',
            field_applicable='mother_alive')

        fields = ['flourish_interest', 'flourish_participation']

        for field in fields:
            self.not_applicable_only(
                NO,
                field='child_alive',
                field_applicable=field)

    def not_applicable_only(self, *responses, field=None, field_applicable=None):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get(field) in responses
                and cleaned_data.get(field_applicable) != NOT_APPLICABLE):
                message = {field_applicable: 'This field is not applicable'}
                self._errors.update(message)
                raise ValidationError(message)

    def applicable_only(self, *responses, field=None, field_applicable=None):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get(field) in responses
                and cleaned_data.get(field_applicable) == NOT_APPLICABLE):
                message = {field_applicable: 'This field is applicable'}
                self._errors.update(message)
                raise ValidationError(message)
