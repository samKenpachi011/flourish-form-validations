from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import NOT_APPLICABLE
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class SocioDemographicDataFormValidator(FormValidatorMixin, FormValidator):
    antenatal_enrollment_model = 'flourish_caregiver.antenatalenrollment'

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    def clean(self):
        super().clean()

        other_specify_fields = ['marital_status', 'ethnicity',
                                'current_occupation', 'provides_money',
                                'money_earned', 'toilet_facility']
        for field in other_specify_fields:
            self.validate_other_specify(field=field)

        subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier

        is_woman_preg = self.antenatal_enrollment_cls.objects.filter(subject_identifier=subject_identifier)

        if is_woman_preg:
            stay_with_child = self.cleaned_data['stay_with_child']
            if not stay_with_child == NOT_APPLICABLE:
                raise ValidationError({
                    'stay_with_child': 'The participant is currently pregnant'
                })

            if not self.cleaned_data['number_of_household_members']:
                raise ValidationError({
                    'number_of_household_members': 'The participant is pregnant, hence this question needs to be '
                                                   'answered '
                })

        else:
            if self.cleaned_data['number_of_household_members']:
                raise ValidationError({
                    'number_of_household_members': 'The participant is not pregnant, hence should be left blank'
                })
