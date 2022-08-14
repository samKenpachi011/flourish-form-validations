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

        visit_code = cleaned_data.get('maternal_visit').visit_code

        obtained_all_measurements = self.cleaned_data.get('all_measurements')
        is_preg = self.cleaned_data.get('is_preg')

        required_fields_not_pregnant = ['waist_circ', 'hip_circ']
        for r_field in required_fields_not_pregnant:
            self.required_if_true(
                obtained_all_measurements == YES and is_preg == NO and visit_code != '2000D',
                field='is_preg',
                field_required=r_field)

        if obtained_all_measurements == YES:

            required_fields_all_measurements = ['systolic_bp', 'diastolic_bp', 'height', 'weight_kg']
            for r_field in required_fields_all_measurements:
                self.required_if(
                    YES,
                    field='all_measurements',
                    field_required=r_field,
                    inverse=True)

            if (cleaned_data.get('systolic_bp') and
                    cleaned_data.get('diastolic_bp')):
                if cleaned_data.get('systolic_bp') < \
                        cleaned_data.get('diastolic_bp'):
                    msg = {'diastolic_bp':
                        'Systolic blood pressure cannot be lower than the'
                        'diastolic blood pressure. Please correct.'}
                    self._errors.update(msg)
                    raise ValidationError(msg)

        self.check_all_cm_valid()
        self.check_bp()

    def check_bp(self):
        field_list = ['systolic_bp', 'diastolic_bp']

        for field in field_list:
            self.required_if_not_none(
                field=field,
                field_required='confirm_values',
                required_msg='Please select either NO or YES',
                not_required_msg='Field not required')

    @property
    def check_cm_not_preg(self):
        height = self.cleaned_data.get('height')
        weight_kg = self.cleaned_data.get('weight_kg')
        systolic_bp = self.cleaned_data.get('systolic_bp')
        diastolic_bp = self.cleaned_data.get('diastolic_bp')
        hip_circ = self.cleaned_data.get('hip_circ')
        waist_circ = self.cleaned_data.get('waist_circ')
        cm_all_not_preg = [height, weight_kg, systolic_bp, diastolic_bp, hip_circ, waist_circ]

        return not any(item is None for item in cm_all_not_preg)

    @property
    def check_cm_is_preg(self):
        height = self.cleaned_data.get('height')
        weight_kg = self.cleaned_data.get('weight_kg')
        systolic_bp = self.cleaned_data.get('systolic_bp')
        diastolic_bp = self.cleaned_data.get('diastolic_bp')
        cm_all_is_preg = [height, weight_kg, systolic_bp, diastolic_bp]

        return not any(item is None for item in cm_all_is_preg)

    def check_all_cm_valid(self):
        obtained_all_cm = self.cleaned_data.get('all_measurements')
        is_preg = self.cleaned_data.get('is_preg')
        confirm_values = self.cleaned_data.get('confirm_values')

        if confirm_values and confirm_values == NO:
            message = {'confirm_values':
            'Are you sure about the given values please confirm!'}
            self._errors.update(message)
            raise ValidationError(message)
        else:
            if obtained_all_cm and obtained_all_cm == NO:
                if (is_preg == YES) and (self.check_cm_is_preg is True):
                    message = {'all_measurements':
                    'All pregnancy measurements have been given please select Yes'}
                    self._errors.update(message)
                    raise ValidationError(message)

            if (is_preg == NO) and (self.check_cm_not_preg is True):
                if obtained_all_cm and obtained_all_cm == NO:
                    message = {'all_measurements':
                        'All measurements have been given please select Yes'}
                    self._errors.update(message)
                    raise ValidationError(message)
