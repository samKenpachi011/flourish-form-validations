from django.forms import ValidationError
from flourish_form_validations.form_validators.crf_form_validator import FormValidatorMixin


from edc_constants.constants import NO, YES
from edc_form_validators import FormValidator


class MaternalIterimIdccFormVersion2Validator(FormValidatorMixin,
                                              FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        for field in ['laboratory_information_available', 'vl_result_availiable',
                      'cd4_value_and_date_availiable', 'vl_value_and_date_availiable',
                      'any_new_diagnoses']:

            self.required_if(YES,
                             field='info_since_lastvisit',
                             field_required=field)

        self.required_if(YES,
                         field='laboratory_information_available',
                         field_required='last_visit_result')

        self.required_if(NO,
                         field='last_visit_result',
                         field_required='reason_cd4_not_availiable')

        for field in ['recent_cd4', 'recent_cd4_date']:
            self.required_if(YES,
                             field='cd4_value_and_date_availiable',
                             field_required=field)

        self.required_if(NO, field='vl_result_availiable',
                         field_required='reason_vl_not_availiable')

        for field in ['value_vl_size', 'value_vl', 'recent_vl_date']:
            self.required_if(YES,
                             field='vl_value_and_date_availiable',
                             field_required=field)

        self.required_if(YES,
                         field='any_new_diagnoses',
                         field_required='new_other_diagnoses')

        self.validate_viral_load_value()

    def validate_viral_load_value(self):

        vl_value = self.cleaned_data.get('value_vl', None)
        info_since_lastvisit = self.cleaned_data.get(
            'info_since_lastvisit', None)

        if info_since_lastvisit == YES and vl_value:
            if (vl_value != 400
                    and self.cleaned_data.get('value_vl_size') == 'less_than'):
                msg = {'value_vl': 'You indicated that the value of the most recent VL is '
                       f'less_than a {vl_value}, therefore the value of VL should be 400'}
                self._errors.update(msg)
                raise ValidationError(msg)

            if (vl_value != 10000000
                    and self.cleaned_data.get('value_vl_size') == 'greater_than'):
                msg = {'value_vl': 'You indicated that the value of the most recent VL is '
                       f'greater_than a {vl_value}, therefore the value of VL should be 10,000,000'}
                self._errors.update(msg)
                raise ValidationError(msg)
