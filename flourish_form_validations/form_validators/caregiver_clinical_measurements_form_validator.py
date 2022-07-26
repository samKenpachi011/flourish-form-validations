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
    
        visit_code = cleaned_data.get('maternal_visit').visit_code
        
        obtained_all_measurements = self.cleaned_data.get('all_measurements')
        is_preg = self.cleaned_data.get('is_preg') 

        required_fields_not_pregnant = ['waist_circ','hip_circ']
        for r_field in required_fields_not_pregnant:
            self.required_if_true(obtained_all_measurements==YES and is_preg==NO and visit_code !='2000D',
                                  field='is_preg',field_required=r_field) 
        
        if obtained_all_measurements == YES:
            
            required_fields_all_measurements = ['systolic_bp','diastolic_bp']
            for r_field in required_fields_all_measurements:
                self.required_if(YES,field='all_measurements',field_required=r_field, inverse=True)

            self.required_if(YES,
                            field='weight_available', field_required='weight_kg')

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
 
            
        
            