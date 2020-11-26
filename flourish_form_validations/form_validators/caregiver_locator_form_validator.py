from edc_constants.constants import YES
from edc_form_validators.form_validator import FormValidator


class CaregiverLocatorFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='may_visit_home',
            field_required='physical_address')

        self.required_if(
            YES,
            field='may_call',
            field_required='subject_cell')

        fields_required = ['subject_work_place', 'subject_work_phone']
        for field in fields_required:
            self.required_if(
                YES,
                field='may_call_work',
                field_required=field)

        fields = ['indirect_contact_name', 'indirect_contact_relation',
                  'indirect_contact_physical_address', 'indirect_contact_cell']
        for field in fields:
            self.required_if(
                YES,
                field='may_contact_indirectly',
                field_required=field)

        required_fields = ['caretaker_name', 'caretaker_cell']

        for field in required_fields:
            self.required_if(
                YES,
                field='has_caretaker',
                field_required=field)
