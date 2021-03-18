import re
from django.core.exceptions import ValidationError

from edc_constants.choices import FEMALE, MALE, NO
from edc_form_validators import FormValidator


class CaregiverChildConsentFormValidator(FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get('subject_identifier')
        super().clean()

        self.required_if(
            NO,
            field='is_literate',
            field_required='witness_name')

        self.clean_full_name_syntax()
        self.validate_identity_number(cleaned_data=self.cleaned_data)

    def clean_full_name_syntax(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if not re.match(r'^[A-Z]+$|^([A-Z]+[ ][A-Z]+)$', first_name):
            message = {'first_name': 'Ensure first name is letters (A-Z) in '
                       'upper case, no special characters, except spaces.'}
            self._errors.update(message)
            raise ValidationError(message)

        if not re.match(r'^[A-Z-]+$', last_name):
            message = {'last_name': 'Ensure last name is letters (A-Z) in '
                       'upper case, no special characters, except hyphens.'}
            self._errors.update(message)
            raise ValidationError(message)

        if first_name and last_name:
            if first_name != first_name.upper():
                message = {'first_name': 'First name must be in CAPS.'}
                self._errors.update(message)
                raise ValidationError(message)
            elif last_name != last_name.upper():
                message = {'last_name': 'Last name must be in CAPS.'}
                self._errors.update(message)
                raise ValidationError(message)

    def validate_identity_number(self, cleaned_data=None):
        if cleaned_data.get('identity') != cleaned_data.get(
                'confirm_identity'):
            msg = {'identity': '\'Identity\' must match \'confirm identity\'.'}
            self._errors.update(msg)
            raise ValidationError(msg)
        if cleaned_data.get('identity_type') == 'country_id':
            if len(cleaned_data.get('identity')) != 9:
                msg = {'identity':
                       'Country identity provided should contain 9 values. '
                       'Please correct.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            gender = cleaned_data.get('gender')
            if gender == FEMALE and cleaned_data.get('identity')[4] != '2':
                msg = {'identity':
                       'Participant gender is Female. Please correct identity number.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            elif gender == MALE and cleaned_data.get('identity')[4] != '1':
                msg = {'identity':
                       'Participant is Male. Please correct identity number.'}
                self._errors.update(msg)
                raise ValidationError(msg)
