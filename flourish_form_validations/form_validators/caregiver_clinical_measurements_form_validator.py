from django.core.exceptions import ValidationError
from edc_constants.constants import YES
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

        self.required_if_true(
            (cleaned_data.get('is_preg') != YES
                and cleaned_data.get('maternal_visit').visit_code != '2000D'),
            field_required='waist_circ')

        self.required_if_true(
            (cleaned_data.get('is_preg') != YES
                and cleaned_data.get('maternal_visit').visit_code != '2000D'),
            field_required='hip_circ')
        
        self.validate_systolic_bp(cleaned_data=cleaned_data)
        self.validate_diastolic_bp(cleaned_data=cleaned_data)

    def validate_systolic_bp(self,cleaned_data=None):
        systolic_bp_upper = 130
        systolic_bp_lower = 100
        systolic_bp = cleaned_data.get('systolic_bp')

        if systolic_bp:
            self.required_if_true((systolic_bp < systolic_bp_lower) or (systolic_bp > systolic_bp_upper),
                                  field_required='confirm_values')
            
    def validate_diastolic_bp(self,cleaned_data=None):
        
        diastolic_bp_upper = 80
        diastolic_bp_lower = 60
        diastolic_bp = cleaned_data.get('diastolic_bp')
        
        if diastolic_bp:
            self.required_if_true((diastolic_bp < diastolic_bp_lower) or (diastolic_bp > diastolic_bp_upper),
                                  field_required='confirm_values')
            
        
            