from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class CaregiverClinicalMeasurementsFormValidator(FormValidatorMixin,
                                                 FormValidator):

    def clean(self):

        cleaned_data = self.cleaned_data
        self.subject_identifier = cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.check_bp()
        # self.check_all_cm_valid()
        self.check_all_cm_tb_valid()
        self.check_all_cm_valid_1000M()
        self.check_all_cm_valid_2000M()
        self.check_all_cm_valid_2000D()
        
        if (cleaned_data.get('systolic_bp') and
            cleaned_data.get('diastolic_bp')):
            if cleaned_data.get('systolic_bp') < \
                    cleaned_data.get('diastolic_bp'):
                        msg = {'diastolic_bp':
                            'Systolic blood pressure cannot be lower than the'
                            'diastolic blood pressure. Please correct.'}
                        self._errors.update(msg)
                        raise ValidationError(msg)
                    
        if cleaned_data.get('systolic_bp') is not None or cleaned_data.get('diastolic_bp') is not None :
            
            if cleaned_data.get('diastolic_bp') is None or cleaned_data.get('systolic_bp') is None:
                msg = {'systolic_bp':
                    'Systolic blood pressure cannot be lower than the'
                    'diastolic blood pressure. Please correct.'}
                self._errors.update(msg)
                raise ValidationError(msg)       

    def check_bp(self):
        if self.cleaned_data.get('all_measurements') == YES and self.check_bp_measurements == False:
            message = {'systolic_bp':
                        'Please provide all the blood pressure values'}
            self._errors.update(message)
            raise ValidationError(message)

    @property
    def check_bp_measurements(self):
        systolic_bp = self.cleaned_data.get('systolic_bp')
        diastolic_bp = self.cleaned_data.get('diastolic_bp')
        bp_list = [systolic_bp, diastolic_bp]
        
        return not any(item is None for item in bp_list)

    @property
    def check_all_cm(self):
        height = self.cleaned_data.get('height')
        weight_kg = self.cleaned_data.get('weight_kg')
        systolic_bp = self.cleaned_data.get('systolic_bp')
        diastolic_bp = self.cleaned_data.get('diastolic_bp')
        hip_circ = self.cleaned_data.get('hip_circ')
        waist_circ = self.cleaned_data.get('waist_circ')
        cm_all = [height, weight_kg, systolic_bp, diastolic_bp, hip_circ, waist_circ]

        return not any(item is None for item in cm_all)
    
    @property
    def check_all_cm_1000(self):
        height = self.cleaned_data.get('height')
        weight_kg = self.cleaned_data.get('weight_kg')
        systolic_bp = self.cleaned_data.get('systolic_bp')
        diastolic_bp = self.cleaned_data.get('diastolic_bp')

        cm_all = [height, weight_kg, systolic_bp, diastolic_bp,]

        return not any(item is None for item in cm_all)
    
    @property
    def check_all_cm_2000D(self):
        weight_kg = self.cleaned_data.get('weight_kg')
        systolic_bp = self.cleaned_data.get('systolic_bp')
        diastolic_bp = self.cleaned_data.get('diastolic_bp')

        cm_all_2000D = [weight_kg, systolic_bp, diastolic_bp]

        return not any(item is None for item in cm_all_2000D)
    
    @property
    def check_cm_tb(self):
        weight_kg = self.cleaned_data.get('weight_kg')
        systolic_bp = self.cleaned_data.get('systolic_bp')
        diastolic_bp = self.cleaned_data.get('diastolic_bp')
        cm_all_tb = [weight_kg, systolic_bp, diastolic_bp]

        return not any(item is None for item in cm_all_tb)
    
    def check_all_cm_tb_valid(self):
        obtained_all_cm = self.cleaned_data.get('all_measurements')
        confirm_values = self.cleaned_data.get('confirm_values')
        visit_code = self.cleaned_data.get('maternal_visit').visit_code
    
        if visit_code == '2100T':
            if confirm_values == NO:
                message = {'confirm_values':
                'Are you sure about the given values please confirm!'}
                self._errors.update(message)
                raise ValidationError(message)
            
            elif obtained_all_cm == YES and (self.check_cm_tb is False):
                    message = {'all_measurements':
                    'Please provide all measurements'}
                    self._errors.update(message)
                    raise ValidationError(message)  
                
            elif obtained_all_cm == NO and (self.check_cm_tb is True):
                    message = {'all_measurements':
                        'All measurements have been given please select Yes.'}
                    self._errors.update(message)
                    raise ValidationError(message)
    

    def check_all_cm_valid_1000M(self):
        obtained_all_cm = self.cleaned_data.get('all_measurements')
        confirm_values = self.cleaned_data.get('confirm_values')
        visit_code = self.cleaned_data.get('maternal_visit').visit_code

        if visit_code == '1000M':

            if confirm_values != YES:
                message = {'confirm_values':
                'Are you sure about the given values please confirm!'}
                self._errors.update(message)
                raise ValidationError(message)

            elif obtained_all_cm == NO and (self.check_all_cm_1000 is True):
                    message = {'all_measurements':
                    'All measurements have been given please select Yes'}
                    self._errors.update(message)
                    raise ValidationError(message)
                
            elif obtained_all_cm == YES and self.check_all_cm_1000 is False:
                    message = {'all_measurements':
                    'Please provide all measurements'}
                    self._errors.update(message)
                    raise ValidationError(message) 
                   
    def check_all_cm_valid_2000M(self):
        obtained_all_cm = self.cleaned_data.get('all_measurements')
        confirm_values = self.cleaned_data.get('confirm_values')
        visit_code = self.cleaned_data.get('maternal_visit').visit_code

        if visit_code == '2000M':

            if self.check_all_cm is True and obtained_all_cm == YES and confirm_values != YES:
                message = {'confirm_values':
                'Are you sure about the given values please confirm!'}
                self._errors.update(message)
                raise ValidationError(message)

            elif obtained_all_cm == NO and (self.check_all_cm is True):
                    message = {'all_measurements':
                    'All measurements have been given please select Yes'}
                    self._errors.update(message)
                    raise ValidationError(message)
                
            elif obtained_all_cm == YES and self.check_all_cm is False:
                    message = {'all_measurements':
                    'Please provide all measurements'}
                    self._errors.update(message)
                    raise ValidationError(message)    
                
    def check_all_cm_valid_2000D(self):
        obtained_all_cm = self.cleaned_data.get('all_measurements')
        confirm_values = self.cleaned_data.get('confirm_values')
        visit_code = self.cleaned_data.get('maternal_visit').visit_code

        if visit_code == '2000D':
            if obtained_all_cm == NO and self.check_all_cm_2000D is True:
                    message = {'all_measurements':
                    'All measurements have been given please select Yes'}
                    self._errors.update(message)
                    raise ValidationError(message)
                
            elif obtained_all_cm == YES and self.check_all_cm_2000D is False:
                    message = {'all_measurements':
                    'Please provide all measurements'}
                    self._errors.update(message)
                    raise ValidationError(message)   
                
            elif self.check_all_cm_2000D is True and obtained_all_cm == YES and confirm_values != YES:
                message = {'confirm_values':
                'Are you sure about the given values please confirm!'}
                self._errors.update(message)
                raise ValidationError(message)    
                 
