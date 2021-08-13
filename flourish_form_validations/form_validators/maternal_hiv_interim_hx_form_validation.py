from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator
from django.core.exceptions import ValidationError


class MaternalHivInterimHxFormValidator(CRFFormValidator,
                                        FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        required_fields = ('cd4_date', 'cd4_result')
        for required in required_fields:
            self.required_if(
                YES,
                field='has_cd4',
                field_required=required,
                required_msg=('You indicated that a CD4 count was performed. '
                              f'Please provide the {required}'),
                not_required_msg=('You indicated that a CD4 count was NOT '
                                  f'performed, yet provided a {required} '
                                  'CD4 was performed. Please correct.')
            )
        self.required_if(
            YES,
            field='has_vl',
            field_required='vl_date',
            required_msg=('You indicated that a VL count was performed. '
                          'Please provide the date.'),
            not_required_msg=('You indicated that a VL count was NOT performed, '
                              'yet provided a date VL was performed. Please correct.')
        )
        self.applicable_if(
            YES,
            field='has_vl',
            field_applicable='vl_detectable'
        )

        self._validate_vl_result()

    def _validate_vl_result(self):
        """
        Used to validate vl_result based on vl_detectable
        """
        # Get data fro the form and convert to on integer
        vl_detectable = self.cleaned_data.get('vl_detectable')
        vl_result = self.cleaned_data.get('vl_result')

        # Check if the vl_result is null
        if vl_detectable == YES and vl_result is None:
            raise ValidationError({'vl_result', 'Cannot be empty'})
        if vl_detectable == NO and vl_result is None:
            raise ValidationError({'vl_result', 'Cannot be empty'})

        # if not null, then convert vl_resut to int through reassignment
        vl_result = int(vl_result)

        # This is the original required condition, Superposed for readability
        if vl_detectable == YES and not (vl_result > 400):
            raise ValidationError({'vl_result': 'Viral load should be more than 400 if it is'
                                   ' detectable'})
        elif vl_detectable == NO and not (vl_result <= 400):
            raise ValidationError({'vl_result': 'Viral load should be 400 or less if it is'
                                   ' not detectable'})
