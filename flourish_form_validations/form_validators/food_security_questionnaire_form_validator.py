from edc_constants.constants import YES
from edc_form_validators import FormValidator


class FoodSecurityQuestionnaireFormValidator(FormValidator):

    def clean(self):
        super().clean()
        self.required_if(
            YES,
            field='cut_meals',
            field_required='how_often')
