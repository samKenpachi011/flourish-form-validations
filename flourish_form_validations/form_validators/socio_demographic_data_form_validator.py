from django.core.exceptions import ValidationError

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
        self.validate_number_of_people_living_in_the_household(
            cleaned_data=self.cleaned_data)

    def validate_number_of_people_living_in_the_household(self,
                                                          cleaned_data=None):
        house_members_18older = cleaned_data.get('house_members_18older')
        house_people_number = cleaned_data.get('house_people_number')
        if house_members_18older and (house_members_18older >
                                      house_people_number):
            msg = {'house_members_18older':
                   f'Number of people ({house_members_18older}) who are older '
                   f'than 18 and live in the household cannot be more than the'
                   f' total number ({house_people_number}) of people living in'
                   f' the household'}
            self._errors.update(msg)
            raise ValidationError(msg)
