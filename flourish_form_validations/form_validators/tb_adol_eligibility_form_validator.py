from edc_constants.constants import NO
from edc_form_validators import FormValidatorMixin, FormValidator


class TbAdolEligibilityFormValidator(FormValidator, FormValidatorMixin):

    def clean(self):
        super().clean()

        self.required_if(NO,
                         field_required='tb_adol_participation',
                         field='reasons_unwilling_part')

        self.validate_other_specify(field='reasons_unwilling_part',
                                    other_specify_field='reasons_unwilling_part_other')
