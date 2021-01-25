from edc_constants.constants import OTHER
from edc_form_validators import FormValidator


class InPersonContactAttemptFormValidator(FormValidator):

    def clean(self):

        self.validate_other_specify(
            field='phy_addr_unsuc')

        self.validate_other_specify(
            field='workplace_unsuc')

        self.validate_other_specify(
            field='contact_person_unsuc')

        contact_location = self.cleaned_data.get('contact_location')
        successful_location = self.cleaned_data.get('successful_location')

        if (contact_location == 'physical_address' and
                successful_location != 'physical_address'):

            self.required_if(
                'physical_address',
                field='contact_location',
                field_required='phy_addr_unsuc')
