from edc_constants.constants import NO, YES, OTHER
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin


class TbReferralOutcomesFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        required_fields = ['further_tb_eval', 'tb_diagnostic_perf',
                           'tb_treat_start', 'tb_prev_therapy_start']
        for field in required_fields:
            self.required_if(
                YES,
                field='referral_clinic_appt',
                field_required=field,
            )

        self.m2m_required_if(
            YES,
            field='tb_diagnostic_perf',
            m2m_field='tb_diagnostics')

        self.m2m_other_specify(
            OTHER,
            m2m_field='tb_diagnostics',
            field_other='tb_diagnostics_other')

        self.required_if(
            YES,
            field='tb_diagnostic_perf',
            field_required='tb_diagnose_pos')

        self.required_if(
            YES,
            field='tb_diagnose_pos',
            field_required='tb_test_results')
