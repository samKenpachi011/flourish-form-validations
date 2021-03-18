import re
from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.utils import relativedelta
from edc_constants.constants import FEMALE, MALE, NO
from edc_form_validators import FormValidator


class SubjectConsentFormValidator(FormValidator):

    prior_screening_model = 'flourish_caregiver.screeningpriorbhpparticipants'

    subject_consent_model = 'flourish_caregiver.subjectconsent'

    maternal_dataset_model = 'flourish_caregiver.maternaldataset'

    child_dataset_model = 'flourish_child.childdataset'

    @property
    def bhp_prior_screening_cls(self):
        return django_apps.get_model(self.prior_screening_model)

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def maternal_dataset_cls(self):
        return django_apps.get_model(self.maternal_dataset_model)

    @property
    def child_dataset_cls(self):
        return django_apps.get_model(self.child_dataset_model)

    def clean(self):
        cleaned_data = self.cleaned_data
        self.subject_identifier = cleaned_data.get('subject_identifier')
        self.screening_identifier = cleaned_data.get('screening_identifier')
        super().clean()

        self.clean_full_name_syntax()
        self.clean_initials_with_full_name()
        self.validate_recruit_source()
        self.validate_recruitment_clinic()
        self.validate_is_literate()
        self.validate_dob(cleaned_data=self.cleaned_data)
        self.validate_citizenship()
        self.validate_identity_number(cleaned_data=self.cleaned_data)
        self.validate_child_dob(cleaned_data=self.cleaned_data)
        self.validate_consent_for_child(cleaned_data=self.cleaned_data)
        self.validate_reconsent()

    def validate_reconsent(self):
        try:
            consent_obj = self.subject_consent_cls.objects.get(
                subject_identifier=self.cleaned_data.get('subject_identifier'),
                version=self.cleaned_data.get('version'))
        except self.subject_consent_cls.DoesNotExist:
            pass
        else:
            consent_dict = consent_obj.__dict__
            consent_fields = [
                'first_name', 'last_name', 'dob', 'recruit_source',
                'recruit_source_other', 'recruitment_clinic',
                'recruitment_clinic_other', 'is_literate', 'identity',
                'identity_type']
            for field in consent_fields:
                if self.cleaned_data.get(field) != consent_dict[field]:
                    message = {field:
                               f'{field} was previously reported as, '
                               f'{consent_dict[field]}, please correct.'}
                    self._errors.update(message)
                    raise ValidationError(message)

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
        if cleaned_data.get('identity') != cleaned_data.get('confirm_identity'):
            msg = {'identity':
                   '\'Identity\' must match \'confirm identity\'.'}
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

    def validate_dob(self, cleaned_data=None):
        consent_datetime = cleaned_data.get('consent_datetime')
        consent_age = relativedelta(
            consent_datetime.date(), cleaned_data.get('dob')).years
        age_in_years = None

        try:
            consent_obj = self.subject_consent_cls.objects.get(
                screening_identifier=self.cleaned_data.get('screening_identifier'),
                version=self.cleaned_data.get('version'))
        except self.subject_consent_cls.DoesNotExist:
            if consent_age < 18:
                message = {'dob':
                           'Participant is less than 18 years, age derived '
                           f'from the DOB is {consent_age}.'}
                self._errors.update(message)
                raise ValidationError(message)
        else:
            age_in_years = relativedelta(
                consent_datetime.date(), consent_obj.dob).years
            if consent_age != age_in_years:
                message = {'dob':
                           'In previous consent the derived age of the '
                           f'participant is {age_in_years}, but age derived '
                           f'from the DOB is {consent_age}.'}
                self._errors.update(message)
                raise ValidationError(message)

    def validate_child_dob(self, cleaned_data=None):
        child_dob = cleaned_data.get('child_dob')
        if child_dob and self.maternal_dataset:
            if child_dob != self.maternal_dataset.delivdt:
                msg = {'child_dob':
                       'Child date of birth does not match with dob '
                       f'({self.maternal_dataset.delivdt}) from the dataset.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_consent_for_child(self, cleaned_data=None):
        consent_datetime = cleaned_data.get('consent_datetime')
        fields = ['child_test', 'child_remain_in_study', ]
        for field in fields:
            self.applicable_if_true(
                self.maternal_dataset is not None,
                field_applicable=field)
        if self.maternal_dataset:
            child_dataset = self.child_dataset(
                study_maternal_identifier=self.maternal_dataset.study_maternal_identifier)
            if child_dataset:
                self.applicable_if_true(
                    child_dataset.infant_sex[:1] == FEMALE,
                    field_applicable='child_preg_test',
                    applicable_msg=('Child\'s gender is female from the dataset '
                                    'This field is applicable.'))
            child_age_in_years = relativedelta(
                consent_datetime.date(), self.maternal_dataset.delivdt).years
            self.applicable_if_true(
                child_age_in_years >= 16,
                field_applicable='child_knows_status',
                applicable_msg=(f'Age derived from the child DOB is {child_age_in_years} '
                                'This field is applicable.'))

    def validate_recruit_source(self):
        self.validate_other_specify(
            field='recruit_source',
            other_specify_field='recruit_source_other',
            required_msg=('You indicated that mother first learnt about the '
                          'study from a source other than those in the list '
                          'provided. Please specify source.'),
        )

    def validate_recruitment_clinic(self):
        clinic = self.cleaned_data.get('recruitment_clinic')
        self.validate_other_specify(
            field='recruitment_clinic',
            other_specify_field='recruitment_clinic_other',
            required_msg=('You MUST specify other facility that mother was '
                          f'recruited from as you already indicated {clinic}')
        )

    def validate_is_literate(self):
        self.required_if(
            NO,
            field='is_literate',
            field_required='witness_name',
            required_msg='Participant is illiterate please provide witness\'s name(s).')

    def validate_citizenship(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('citizen') == NO:
            msg = {'citizen':
                   'Participant MUST be a botswana citizen.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    @property
    def maternal_dataset(self):
        try:
            maternal_dataset = self.maternal_dataset_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except self.maternal_dataset_cls.DoesNotExist:
            return None
        else:
            return maternal_dataset

    def child_dataset(self, study_maternal_identifier=None):
        try:
            child_dataset = self.child_dataset_cls.objects.get(
                study_maternal_identifier=study_maternal_identifier)
        except self.child_dataset_cls.DoesNotExist:
            return None
        else:
            return child_dataset
