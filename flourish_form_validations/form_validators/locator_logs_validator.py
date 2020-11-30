from edc_form_validators import FormValidator


class LocatorLogEntryFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.required_if(
            'not_found',
            field='log_status',
            field_required='comment',
            required_msg='Please provide a short brief reason')
