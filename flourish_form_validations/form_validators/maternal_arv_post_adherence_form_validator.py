from edc_constants.constants import NOT_APPLICABLE, YES, OTHER
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class MaternalArvPostAdherenceFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        super().clean()

        self.validate_interruption_reason_against_missed_arv(self.cleaned_data)

        self.m2m_other_specify(
            OTHER,
            m2m_field='interruption_reason',
            field_other='interruption_reason_other')

        self.required_if(
            YES,
            field='stopped_art_past_yr',
            field_required='stopped_art_freq')

        stopped_art = self.cleaned_data.get('stopped_art_past_yr', None)
        self.m2m_applicable_if_true(
            stopped_art == YES,
            m2m_field='stopped_art_reasons')

        self.m2m_other_specify(
            OTHER,
            m2m_field='stopped_art_reasons',
            field_other='stopped_reasons_other')

        selections = [NOT_APPLICABLE]
        self.m2m_single_selection_if(
            *selections,
            m2m_field='stopped_art_reasons')


    def validate_interruption_reason_against_missed_arv(self, cleaned_data):
        if cleaned_data.get('missed_arv', None) is not None:
            self.m2m_applicable_if_true(
                cleaned_data.get('missed_arv') >= 1,
                m2m_field='interruption_reason')

        selections = [NOT_APPLICABLE]
        self.m2m_single_selection_if(
            *selections,
            m2m_field='interruption_reason')
