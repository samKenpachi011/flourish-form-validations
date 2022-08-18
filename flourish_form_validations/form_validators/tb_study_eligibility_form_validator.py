from edc_constants.constants import NO
from edc_form_validators import FormValidatorMixin, FormValidator


class TbStudyEligibilityFormValidator(FormValidator, FormValidatorMixin):

    def clean(self):
        super().clean()

        self.required_if(NO,
                         field_required='reasons_not_participating',
                         field='tb_participation')

        self.validate_other_specify(field='reasons_not_participating',
                                    other_specify_field='reasons_not_participating_other')
