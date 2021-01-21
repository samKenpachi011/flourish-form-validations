from edc_constants.constants import YES
from edc_form_validators import FormValidator


class TbHistoryPregFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='history_of_tbt',
            field_required='tbt_completed')

        self.required_if(
            YES,
            field='prior_tb_history',
            field_required='tb_diagnosis_type')

        fields_required = ['tb_drugs_freq', 'iv_meds_used', 'tb_treatmnt_completed']

        for field in fields_required:
            self.required_if(
                YES,
                field='prior_treatmnt_history',
                field_required=field)
