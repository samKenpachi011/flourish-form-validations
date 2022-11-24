from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin


class TbRoutineHealthScreenV2FormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        super().clean()

        fields_required = ['tb_screened', 'diagnostic_referral']

        for field in fields_required:
            self.not_required_if(
                '0',
                field='tb_health_visits',
                field_required=field
            )

        self.validate_other_specify(
            field='screen_location',
            other_specify_field='screen_location_other'
        )
