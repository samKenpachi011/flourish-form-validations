from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from edc_constants.choices import YES, NO


class HivViralLoadCd4FormValidator(FormValidator):

    def clean(self):

        required_fields = ['cd4_count', 'cd4_count_date']
        for field in required_fields:
            self.required_if(
                YES,
                field='last_cd4_count_known',
                field_required=field)

        self.required_if(
            YES,
            field='last_vl_known',
            field_required='vl_detectable')

        viral_load_fields = ['vl_detectable', 'recent_vl_results',
                             'hiv_results_quantifier', 'last_vl_date']
        for field in viral_load_fields:
            self.required_if(
                YES,
                field='last_vl_known',
                field_required=field)

        vl_detectable = self.cleaned_data.get('vl_detectable')
        results_quantifier = self.cleaned_data.get('hiv_results_quantifier')
        recent_vl_results = self.cleaned_data.get('recent_vl_results')
        if vl_detectable == YES:
            if not results_quantifier == 'equal':
                message = {'hiv_results_quantifier':
                           'The viral load is detectable, the results quantifier '
                           'should be equal(=)'}
                self._errors.update(message)
                raise ValidationError(message)
            if recent_vl_results <= 400:
                message = {'recent_vl_results':
                           'The viral load is detectable, the vl results '
                           'should be more than 400'}
                self._errors.update(message)
                raise ValidationError(message)
        elif vl_detectable == NO:
            if not results_quantifier == 'less_than':
                message = {'hiv_results_quantifier':
                           'The viral load is not detectable, the results '
                           'quantifier should be less than(<)'}
                self._errors.update(message)
                raise ValidationError(message)
            if recent_vl_results != 400:
                message = {'recent_vl_results':
                           'The viral load is not detectable, the vl results '
                           'should be 400'}
                self._errors.update(message)
                raise ValidationError(message)
