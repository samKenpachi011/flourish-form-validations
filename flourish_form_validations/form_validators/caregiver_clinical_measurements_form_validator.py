from django.core.exceptions import ValidationError
from edc_constants.constants import YES,NO
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class CaregiverClinicalMeasurementsFormValidator(FormValidatorMixin,
                                                 FormValidator):

    def clean(self):

        cleaned_data = self.cleaned_data
        self.subject_identifier = cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        if (cleaned_data.get('systolic_bp') and
                cleaned_data.get('diastolic_bp')):
            if cleaned_data.get('systolic_bp') < \
                    cleaned_data.get('diastolic_bp'):
                msg = {'diastolic_bp':
                       'Systolic blood pressure cannot be lower than the '
                       'diastolic blood pressure. Please correct.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            
            
        confirm_values = self.cleaned_data.get('confirm_values')
        if confirm_values == NO:
            message = {'confirm_values':
                        'Please ensure that you agree with the given values'}
            self._errors.update(message)
            raise ValidationError(message)  

        self.required_if_true(
            (cleaned_data.get('is_preg') != YES
                and cleaned_data.get('maternal_visit').visit_code != '2000D'),
            field_required='waist_circ')

        self.required_if_true(
            (cleaned_data.get('is_preg') != YES
                and cleaned_data.get('maternal_visit').visit_code != '2000D'),
            field_required='hip_circ')
        
  
            
        
            