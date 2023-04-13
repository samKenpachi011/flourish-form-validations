from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin
from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE
from django.core.exceptions import ValidationError


class MaternalArvAdherenceFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        super().clean()

        missed_arv = self.cleaned_data.get('missed_arv', 0)
        condition = missed_arv > 0
        self.m2m_applicable_if_true(
            condition,
            m2m_field='interruption_reason')

        art_defaulted = self.cleaned_data.get('art_defaulted')
        if missed_arv == 7 and art_defaulted == NO:
            raise ValidationError({'art_defaulted':
                                   'Response to Q3 is 7days, response must be Yes'})

        self.required_if(
            YES,
            field='art_defaulted',
            field_required='days_defaulted')

        check = art_defaulted == YES
        self.m2m_applicable_if_true(
            check,
            m2m_field='reason_defaulted')

        m2m_fields = ['interruption_reason', 'reason_defaulted']
        for field in m2m_fields:
            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field=field)

            self.m2m_other_specify(
                    *[OTHER],
                    m2m_field=field,
                    field_other=f'{field}_other')
