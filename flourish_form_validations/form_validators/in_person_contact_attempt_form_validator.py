from edc_form_validators import FormValidator


class InPersonContactAttemptFormValidator(FormValidator):

    def clean(self):

        self.validate_other_specify(
            field='phy_addr_unsuc')

        self.validate_other_specify(
            field='workplace_unsuc')

        self.validate_other_specify(
            field='contact_person_unsuc')
