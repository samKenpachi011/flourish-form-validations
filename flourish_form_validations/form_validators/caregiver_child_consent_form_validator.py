import re
import datetime
from django.core.exceptions import ValidationError

from edc_constants.choices import FEMALE, MALE, YES, NO, NOT_APPLICABLE
from edc_base.utils import age, get_utcnow
from edc_form_validators import FormValidator


class CaregiverChildConsentFormValidator(FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get('subject_identifier')
        super().clean()

        self.clean_full_name_syntax()
        self.validate_child_knows_status(cleaned_data=self.cleaned_data)
        self.validate_child_preg_test(cleaned_data=self.cleaned_data)
        self.validate_child_years_more_tha_12yrs_at_jun_2025(
            cleaned_data=self.cleaned_data)
        self.validate_identity_number(cleaned_data=self.cleaned_data)

    def clean_full_name_syntax(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name:
            if not re.match(r'^[A-Z]+$|^([A-Z]+[ ][A-Z]+)$', first_name):
                message = {'first_name': 'Ensure first name is letters (A-Z) in '
                           'upper case, no special characters, except spaces.'}
                self._errors.update(message)
                raise ValidationError(message)

        if last_name:
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
        identity = cleaned_data.get('identity')
        if not re.match('[0-9]+$', identity):
            message = {'identity': 'Identity number must be digits.'}
            self._errors.update(message)
            raise ValidationError(message)
        if cleaned_data.get('identity') != cleaned_data.get('confirm_identity'):
            msg = {'identity':
                   '\'Identity\' must match \'confirm identity\'.'}
            self._errors.update(msg)
            raise ValidationError(msg)
        if cleaned_data.get('identity_type') in ['country_id',
                                                 'birth_cert']:
            if len(cleaned_data.get('identity')) != 9:
                msg = {'identity':
                       'Country identity provided should contain 9 values. '
                       'Please correct.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            gender = cleaned_data.get('gender')
            if gender == FEMALE and cleaned_data.get('identity')[4] != '2':
                msg = {'identity':
                       'Participant gender is Female. Please correct identity'
                       ' number.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            elif gender == MALE and cleaned_data.get('identity')[4] != '1':
                msg = {'identity':
                       'Participant is Male. Please correct identity number.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_child_preg_test(self, cleaned_data=None):
        if cleaned_data.get('gender') == 'M' and cleaned_data.get(
                'child_preg_test') in [YES, NO]:
            msg = {'child_preg_test':
                   'Can only be answered as Not applicable since child is Male'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_child_knows_status(self, cleaned_data):

        child_dob = cleaned_data.get('child_dob')

        if not child_dob:
            message = {'child_dob':
                       'Please Enter a valid Date. '
                       f'{child_dob} is not a valid date'}
            self._errors.update(message)
            raise ValidationError(message)
        else:
            child_age = age(child_dob, get_utcnow()).years
            if child_age < 16 and cleaned_data.get(
                    'child_knows_status') in [YES, NO]:
                msg = {'child_knows_status':
                       'Child is less than 16 years'}
                self._errors.update(msg)
                raise ValidationError(msg)
            elif child_age >= 16 and cleaned_data.get(
                    'child_knows_status') == NOT_APPLICABLE:
                msg = {'child_knows_status':
                       'This field is applicable'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_child_years_more_tha_12yrs_at_jun_2025(self, cleaned_data):
        child_dob = cleaned_data.get('child_dob')
        date_jun_2025 = datetime.datetime.strptime("2025-01-30", "%Y-%m-%d").date()
        child_age_at_2025 = age(child_dob, date_jun_2025).years
        if cleaned_data.get('gender') == 'F':
            if (child_age_at_2025 < 12
                    and cleaned_data.get('child_preg_test') != NOT_APPLICABLE):
                msg = {'child_preg_test':
                       'Child will not be 12 years old by 2025, This field is'
                       'not applicable'}
                self._errors.update(msg)
                raise ValidationError(msg)
            elif (child_age_at_2025 >= 12
                    and cleaned_data.get('child_preg_test') == NOT_APPLICABLE):
                msg = {'child_preg_test':
                       'Child is Female. This field is applicable'}
                self._errors.update(msg)
                raise ValidationError(msg)
