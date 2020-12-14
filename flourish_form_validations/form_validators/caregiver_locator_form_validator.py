from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO
from edc_form_validators.form_validator import FormValidator


class CaregiverLocatorFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='may_visit_home',
            field_required='physical_address')

        not_required_fields = ['subject_cell', 'subject_cell_alt',
                               'subject_phone', 'subject_phone_alt']

        for not_required in not_required_fields:
            self.not_required_if(
                NO,
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

        fields = ['indirect_contact_name', 'indirect_contact_relation',
                  'indirect_contact_physical_address']
        for field in fields:
            self.required_if(
                YES,
                field='may_contact_indirectly',
                field_required=field)

        contact_indirectly = self.cleaned_data.get('may_contact_indirectly')
        indirect_contact_cell = self.cleaned_data.get('indirect_contact_cell')
        indirect_contact_phone = self.cleaned_data.get('indirect_contact_phone')
        if contact_indirectly == YES and (not indirect_contact_cell and not indirect_contact_phone):
            msg = {'may_contact_indirectly':
                   'Please provide either the cell number or telephone of the contact.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        not_required_fields = ['indirect_contact_cell', 'indirect_contact_phone']
        for not_required in not_required_fields:
            self.not_required_if(
                NO,
                field='may_contact_indirectly',
                field_required=not_required,
                inverse=False)

        required_fields = ['caretaker_name']

        for field in required_fields:
            self.required_if(
                YES,
                field='has_caretaker',
                field_required=field)

        has_caretaker = self.cleaned_data.get('has_caretaker')
        caretaker_cell = self.cleaned_data.get('caretaker_cell')
        caretaker_tel = self.cleaned_data.get('caretaker_tel')
        if has_caretaker == YES and (not caretaker_cell and not caretaker_tel):
            msg = {'has_caretaker':
                   'Please provide either the caretaker\'s cell number or telephone.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        not_required_fields = ['caretaker_cell', 'caretaker_tel']
        for not_required in not_required_fields:
            self.not_required_if(
                NO,
                field='has_caretaker',
                field_required=not_required,
                inverse=False)
