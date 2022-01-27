from edc_constants.constants import YES
from edc_form_validators import FormValidator


class TbRoutineHealthScreenFormValidator(FormValidator):

    def clean(self):
        fields_required = ['screen_location', 'pos_screen', 'diagnostic_referral']
        for field in fields_required:
            self.required_if(
                YES,
                field='tb_screened',
                field_required=field)

        self.validate_other_specify(
            field='screen_location',
            other_specify_field='screen_location_other',
        )
