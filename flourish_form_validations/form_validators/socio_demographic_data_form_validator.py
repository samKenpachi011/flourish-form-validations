from django.core.exceptions import ValidationError

from edc_constants.constants import YES, NOT_APPLICABLE, NO
from edc_form_validators import FormValidator

from .crf_form_validator import CRFFormValidator


class SocioDemographicDataFormValidator(CRFFormValidator, FormValidator):

    def clean(self):
        super().clean()

        socio_demographic_changed = self.cleaned_data.get(
            'socio_demographic_changed')
        self.validate_socio_demographic_changed(
            socio_demographic_changed=socio_demographic_changed)
        other_specify_fields = ['marital_status', 'ethnicity',
                                'current_occupation', 'provides_money',
                                'money_earned']
        for field in other_specify_fields:
            self.validate_other_specify(field=field)

    def validate_socio_demographic_changed(self, socio_demographic_changed):
        if socio_demographic_changed:
            if socio_demographic_changed == NOT_APPLICABLE:
                msg = {'socio_demographic_changed': 'This field is applicable.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            fields = ['marital_status', 'ethnicity', 'highest_education',
                      'current_occupation', 'provides_money', 'money_earned',
                      'stay_with_child']
            for field in fields:
                self.not_applicable_if(
                    NO,
                    field='socio_demographic_changed',
                    field_applicable=field)
            not_required_fields = ['marital_status_other', 'ethnicity_other',
                                   'current_occupation_other',
                                   'provides_money_other', 'money_earned_other']
            for field in not_required_fields:
                self.not_required_if(
                    NO,
                    field='socio_demographic_changed',
                    field_required=field,
                    inverse=False)
