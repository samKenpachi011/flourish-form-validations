from edc_constants.constants import OTHER
from edc_form_validators import FormValidator


class InPersonContactAttemptFormValidator(FormValidator):

    def clean(self):

        self.required_if(
            OTHER,
            field='phy_addr_unsuc',
            field_required='phy_addr_unsuc_other')

        self.required_if(
            OTHER,
            field='workplace_unsuc',
            field_required='workplace_unsuc_other')

        self.required_if(
            OTHER,
            field='contact_person_unsuc',
            field_required='contact_person_unsuc_other')

        contact_location = self.cleaned_data.get('contact_location')
        successful_location = self.cleaned_data.get('successful_location')

        if (contact_location == 'physical_address' and
                successful_location != 'physical_address'):

            self.required_if(
                'physical_address',
                field='contact_location',
                field_required='phy_addr_unsuc')
