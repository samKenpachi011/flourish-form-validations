from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_form_validators.form_validator import FormValidator


class CaregiverLocatorFormValidator(FormValidator):

    maternal_dataset_model = 'flourish_caregiver.maternaldataset'

    @property
    def maternal_dataset_model_cls(self):
        return django_apps.get_model(self.maternal_dataset_model)

    @property
    def caregiver_child_consent_model_cls(self):
        return django_apps.get_model(self.caregiver_child_consent_model)

    def clean(self):
        #self.validate_names_against_dataset()
        self.required_if(
            YES,
            field='may_visit_home',
            field_required='physical_address')

        not_required_fields = ['subject_cell', 'subject_cell_alt',
                               'subject_phone', 'subject_phone_alt']

        for not_required in not_required_fields:
            self.not_required_if(
                *[NO, NOT_APPLICABLE],
                field='may_call',
                field_required=not_required,
                inverse=False)

        may_call = self.cleaned_data.get('may_call')
        subject_cell = self.cleaned_data.get('subject_cell')
        subject_tel = self.cleaned_data.get('subject_phone')
        if may_call == YES and (not subject_cell and not subject_tel):
            msg = {'may_call':
                   'Please provide either the participant\'s cell number or telephone'}
            self._errors.update(msg)
            raise ValidationError(msg)

        may_call_work = self.cleaned_data.get('may_call_work')
        workplace = self.cleaned_data.get('subject_work_place')
        work_phone = self.cleaned_data.get('subject_work_phone')
        if may_call_work == YES and (not workplace and not work_phone):
            msg = {'may_call_work':
                   'Please provide either the participant\'s name and location of work place'
                   ' or work contact number.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        fields = ['subject_work_place', 'subject_work_phone']
        for field in fields:
            self.not_required_if(
                *[NO, 'Doesnt_work'],
                field='may_call_work',
                field_required=field,
                inverse=False)

        contact_indirectly = self.cleaned_data.get('may_contact_indirectly')
        indirect_contact_cell = self.cleaned_data.get('indirect_contact_cell')
        indirect_contact_phone = self.cleaned_data.get('indirect_contact_phone')
        indirect_contact_physical = self.cleaned_data.get('indirect_contact_physical_address')
        if contact_indirectly == YES and (not indirect_contact_physical and\
                                          not indirect_contact_cell and not indirect_contact_phone):
            msg = {'may_contact_indirectly':
                   'Please provide the physical address or either cell number or '
                   'telephone of the contact.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        not_required_fields = ['indirect_contact_physical_address',
                               'indirect_contact_cell', 'indirect_contact_phone',
                               'indirect_contact_name', 'indirect_contact_relation']
        for not_required in not_required_fields:
            self.not_required_if(
                NO,
                field='may_contact_indirectly',
                field_required=not_required,
                inverse=False)

        self.required_if(
            YES,
            field='has_caretaker',
            field_required='caretaker_name')

        not_required_fields = ['caretaker_cell', 'caretaker_tel']
        for not_required in not_required_fields:
            self.not_required_if(
                NO,
                field='has_caretaker',
                field_required=not_required,
                inverse=False)

    def validate_names_against_dataset(self):
        cleaned_data = self.cleaned_data
        dataset = self.maternal_dataset_obj
        if dataset:
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            if dataset.first_name and first_name != dataset.first_name:
                message = {'first_name':
                           f'First name does not match {dataset.first_name} from dataset.'}
                self._errors.update(message)
                raise ValidationError(message)
            if dataset.last_name and last_name != dataset.last_name:
                message = {'last_name':
                           f'Last name does not match {dataset.last_name} from dataset.'}
                self._errors.update(message)
                raise ValidationError(message)

    @property
    def maternal_dataset_obj(self):
        try:
            maternal_dataset = self.maternal_dataset_model_cls.objects.get(
                screening_identifier=self.cleaned_data.get('screening_identifier'))
        except self.maternal_dataset_model_cls.DoesNotExist:
            return None
        else:
            return maternal_dataset
