from edc_constants.constants import YES, OTHER
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin


class TbRoutineHealthScreenV2FormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        super().clean()

        self.m2m_other_specify(
            OTHER,
            m2m_field='screen_location',
            field_other='screen_location_other')
        self.required_if(
            YES,
            field='tb_screened',
            field_required='pos_screen'
        )
        self.required_if(
            YES,
            field='pos_screen',
            field_required='diagnostic_referral'
        )