import re
from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError

from edc_constants.choices import NO
from edc_constants.constants import MALE, FEMALE
from edc_form_validators import FormValidator


class CaregiverChildConsentFormValidator(FormValidator):

    subject_consent_model = 'flourish_caregiver.subjectconsent'

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    def clean(self):

        self.subject_identifier = self.cleaned_data.get('subject_identifier')
        super().clean()

        self.required_if(
            NO,
            field='is_literate',
            field_required='witness_name')

        self.clean_full_name_syntax()
        self.clean_initials_with_full_name()
        self.validate_identity_number(cleaned_data=self.cleaned_data)
        self.validate_personal_fields()

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

    def clean_initials_with_full_name(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        initials = cleaned_data.get("initials")
        try:
            middle_name = None
            is_first_name = False
            new_first_name = None
            if len(first_name.split(' ')) > 1:
                new_first_name = first_name.split(' ')[0]
                middle_name = first_name.split(' ')[1]

            if (middle_name and
                (initials[:1] != new_first_name[:1] or
                 initials[1:2] != middle_name[:1])):
                is_first_name = True

            elif not middle_name and initials[:1] != first_name[:1]:
                is_first_name = True

            if is_first_name or initials[-1:] != last_name[:1]:
                raise forms.ValidationError(
                    {'initials': 'Initials do not match full name.'},
                    params={
                        'initials': initials,
                        'first_name': first_name,
                        'last_name': last_name},
                    code='invalid')
        except (IndexError, TypeError):
            raise forms.ValidationError('Initials do not match fullname.')

    def validate_identity_number(self, cleaned_data=None):
        if cleaned_data.get('identity_type') == 'country_id':

            identity = cleaned_data.get('identity')
            confirm_identity = cleaned_data.get('confirm_identity')

            if len(identity) != 9:
                msg = {'identity':
                       'Country identity provided should contain 9 values. '
                       'Please correct.'}
                self._errors.update(msg)
                raise ValidationError(msg)

            if identity[4] != '2' and identity[4] != '1':
                msg = {'identity':
                       'This is not a Botswana Identity number'}
                self._errors.update(msg)
                raise ValidationError(msg)

            if identity != confirm_identity:
                msg = {'identity':
                       'Identity number and confirm identity number '
                       'should be the same'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_personal_fields(self, clinician_call_value=None, field=None):

        field_value = self.cleaned_data.get(field)

        if clinician_call_value != field_value:
            message = {field:
                       f'The {field} provided does not match the {field} '
                       f'provided in the Clinician Call Enrollment '
                       f' form. Expected \'{clinician_call_value}\' '
                       f'got \'{field_value}\''}
            self._errors.update(message)
            raise ValidationError(message)
