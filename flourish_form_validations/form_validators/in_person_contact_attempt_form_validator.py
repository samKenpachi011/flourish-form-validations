from django.core.exceptions import ValidationError

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

        phy_addr_unsuc = self.cleaned_data.get('phy_addr_unsuc')
        workplace_unsuc = self.cleaned_data.get('workplace_unsuc')
        contact_person_unsuc = self.cleaned_data.get('contact_person_unsuc')

        if contact_location != successful_location:

            required_fields = [phy_addr_unsuc, workplace_unsuc, contact_person_unsuc]

            for field in required_fields:
                if field == '':
                    message = {'phy_addr_unsuc':
                               'This field is required'}
                    self._errors.update(message)
                    raise ValidationError(message)
