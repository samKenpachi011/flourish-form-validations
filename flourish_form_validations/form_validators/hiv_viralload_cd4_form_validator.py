from edc_form_validators import FormValidator
from edc_constants.choices import YES


class HivViralLoadCd4FormValidator(FormValidator):

    def clean(self):

        self.required_if(
            YES,
            field='last_cd4_count_known',
            field_required='cd4_count')

        self.required_if(
            YES,
            field='last_vl_known',
            field_required='vl_detectable')
