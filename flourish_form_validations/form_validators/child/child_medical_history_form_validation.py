from edc_constants.constants import YES, OTHER
from edc_form_validators import FormValidator


class ChildMedicalHistoryFormValidator(FormValidator):

    def clean(self):

        self.required_if(
            YES,
            field='chronic_since',
            field_required='caregiver_chronic',)

        self.required_if(
            OTHER,
            field='caregiver_chronic',
            field_required='caregiver_chronic_other',)
