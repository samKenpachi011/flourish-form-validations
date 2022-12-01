from django.forms import ValidationError
from edc_constants.constants import NO, YES, OTHER
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class CaregiverReferralFUFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        pnta_fields = ['emo_support_type', 'emo_health_improved',
                       'percieve_counselor', 'satisfied_counselor',
                       'additional_counseling']

        for p_field in pnta_fields:
            self.not_required_if('PNTA',
                                 field='emo_support_provider',
                                 field_required=p_field,
                                 inverse=False)

        qs = self.cleaned_data.get('emo_health_improved')
        if self.cleaned_data.get('emo_support_provider') == 'PNTA' and qs:
            message = {
                'emo_health_improved': 'This field is not required.'}
            self._errors.update(message)
            raise ValidationError(message)

        other_fields = ['referred_to', 'support_ref_decline_reason',
                        'no_support_reason', 'emo_support_type', 'percieve_counselor']

        for other_field in other_fields:
            self.validate_other_specify(field=other_field)

        self.required_if(NO,
                         field='satisfied_counselor',
                         field_required='additional_counseling')

        if (self.cleaned_data.get('emo_support_provider')
                and self.cleaned_data.get('emo_support_provider') != 'PNTA'):

            self.required_if(NO,
                             field='attended_referral',
                             field_required='support_ref_decline_reason')

            self.required_if(YES,
                             field='attended_referral',
                             field_required='emo_support')

            self.required_if(NO,
                             field='emo_support',
                             field_required='no_support_reason')

            self.m2m_required_if(YES,
                                 field='emo_support',
                                 m2m_field='emo_support_type')

            self.m2m_other_specify(OTHER,
                                   m2m_field='emo_support_type',
                                   field_other='emo_support_type_other')

            self.m2m_other_specify(OTHER,
                                   m2m_field='emo_health_improved',
                                   field_other='emo_health_improved_other')

            emo_fields = ['percieve_counselor',
                          'satisfied_counselor']

            for emo in emo_fields:
                self.required_if(YES,
                                 field='emo_support',
                                 field_required=emo)

            self.m2m_required_if(YES,
                                 field='emo_support',
                                 m2m_field='emo_health_improved')
