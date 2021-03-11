from edc_form_validators import FormValidator
from edc_constants.choices import YES


class HivViralLoadCd4FormValidator(FormValidator):

    def clean(self):

        required_fields = ['cd4_count', 'cd4_count_date']
        for field in required_fields:
            self.required_if(
                YES,
                field='last_cd4_count_known',
                field_required=field)

        self.required_if(
            YES,
            field='last_vl_known',
            field_required='vl_detectable')
