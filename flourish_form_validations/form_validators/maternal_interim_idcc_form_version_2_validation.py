from django.forms import ValidationError
from flourish_form_validations.form_validators.crf_form_validator import FormValidatorMixin


from edc_constants.constants import NO, YES, OTHER
from edc_form_validators import FormValidator


class MaternalIterimIdccFormVersion2Validator(FormValidatorMixin,
                                              FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        for field in ['any_new_diagnoses', 'laboratory_information_available']:
            self.required_if(YES,
                             field='info_since_lastvisit',
                             field_required=field)

        for field in ['last_visit_result', 'vl_result_availiable']:

            self.required_if(YES,
                             field='laboratory_information_available',
                             field_required=field)

        self.required_if(NO,
                         field='last_visit_result',
                         field_required='reason_cd4_not_availiable')

        self.required_if(OTHER,
                         field='reason_cd4_not_availiable',
                         field_required='reason_cd4_not_availiable_other')

        for field in ['recent_cd4', 'recent_cd4_date']:
            self.required_if(YES,
                             field='last_visit_result',
                             field_required=field)

        self.required_if(NO, field='vl_result_availiable',
                         field_required='reason_vl_not_availiable')

        self.required_if(OTHER, field='reason_vl_not_availiable',
                         field_required='reason_vl_not_availiable_other')

        for field in ['value_vl_size', 'value_vl', 'recent_vl_date']:
            self.required_if(YES,
                             field='vl_result_availiable',
                             field_required=field)

        self.required_if(YES,
                         field='any_new_diagnoses',
                         field_required='new_other_diagnoses')
        self.required_if(
            YES,
            field='vl_result_availiable',
            field_required='vl_detectable')

        self.validate_viral_load_value()

    def validate_viral_load_value(self):
        vl_detectable = self.cleaned_data.get('vl_detectable')
        value_vl_size = self.cleaned_data.get('value_vl_size')
        value_vl = self.cleaned_data.get('value_vl')
        if vl_detectable == YES:
            if not value_vl_size == 'equal':
                message = {'value_vl_size':
                           'The viral load is detectable, the VL size '
                           'should be equal(=)'}
                self._errors.update(message)
                raise ValidationError(message)
            if value_vl <= 400:
                message = {'value_vl':
                           'The viral load is detectable, the vl results '
                           'should be more than 400'}
                self._errors.update(message)
                raise ValidationError(message)
        elif vl_detectable == NO:
            if not value_vl_size == 'less_than':
                message = {'value_vl_size':
                           'The viral load is not detectable, the VL size '
                           'should be less than(<)'}
                self._errors.update(message)
                raise ValidationError(message)
            if value_vl != 400:
                message = {'value_vl':
                           'The viral load is not detectable, the vl results '
                           'should be 400'}
                self._errors.update(message)
                raise ValidationError(message)
