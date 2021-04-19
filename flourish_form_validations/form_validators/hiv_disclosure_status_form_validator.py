from edc_constants.choices import YES
from edc_form_validators import FormValidator


class HIVDisclosureStatusFormValidator(FormValidator):

    def clean(self):
        super().clean()

        not_required_fields = ['plan_to_disclose', 'reason_not_disclosed',
                               'reason_not_disclosed_other']
        for field in not_required_fields:
            self.not_required_if(YES,
                                 field='disclosed_status',
                                 field_required=field)

        self.validate_other_specify(field='reason_not_disclosed')
