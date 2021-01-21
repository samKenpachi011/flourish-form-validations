from edc_constants.constants import YES
from edc_form_validators import FormValidator


class TbScreenPregFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='have_cough',
            field_required='cough_lasted_2wks')

        self.required_if(
            YES,
            field='have_fever',
            field_required='fever_lasted_2wks')

        self.required_if(
            YES,
            field='have_night_sweats',
            field_required='sweats_lasted_2wks')
