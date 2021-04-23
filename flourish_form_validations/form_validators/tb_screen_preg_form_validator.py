from edc_constants.constants import YES
from edc_form_validators import FormValidator


class TbScreenPregFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='tb_screened',
            field_required='where_screened')

        self.validate_other_specify(field='where_screened')
