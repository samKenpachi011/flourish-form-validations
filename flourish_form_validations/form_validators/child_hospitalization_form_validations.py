from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .crf_form_validator import \
    CRFFormValidator


class ChildHospitalizationFormValidations(CRFFormValidator,
                                          FormValidator):

    def clean(self):
        super().clean()

        self.required_if(
            YES,
            field='hospitalized',
            field_required='number_hospitalised'
        )


class AdmissionsReasonFormValidations(CRFFormValidator,
                                      FormValidator
                                      ):
    def clean(self):
        super().clean()

        self.validate_other_specify(
            field='hospital_name',
            other_specify_field='hospital_name_other'
        )

        self.required_if(
            'Surgical',
            field='reason',
            field_required='reason_surgical'
        )

        self.validate_other_specify(
            field='reason',
            other_specify_field='reason_other'
        )
