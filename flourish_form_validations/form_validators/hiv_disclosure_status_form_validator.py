from edc_form_validators import FormValidator


class HIVDisclosureStatusFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.validate_other_specify(field='reason_not_disclosed')
