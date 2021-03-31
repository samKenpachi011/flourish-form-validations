from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .crf_form_validator import CRFFormValidator


class SocioDemographicDataFormValidator(CRFFormValidator, FormValidator):

    def clean(self):
        super().clean()

        other_specify_fields = ['marital_status', 'ethnicity',
                                'current_occupation', 'provides_money',
                                'money_earned', 'toilet_facility']
        for field in other_specify_fields:
            self.validate_other_specify(field=field)

        required_fields = ['own_phone', 'water_source', 'house_electrified',
                           'house_fridge', 'cooking_method', 'toilet_facility', ]
        for field in required_fields:
            self.required_if(
                YES,
                field='stay_with_child',
                field_required=field)
