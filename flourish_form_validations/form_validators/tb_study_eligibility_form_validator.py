from edc_constants.constants import YES
from edc_form_validators import FormValidatorMixin, FormValidator


class TbStudyEligibilityFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        super().clean()

        self.required_if(YES,
                         field_required='reasons_not_participating',
                         field='tb_participation')

        self.validate_other_specify(field='reasons_not_participating',
                                    other_specify_field='tb_participation')
