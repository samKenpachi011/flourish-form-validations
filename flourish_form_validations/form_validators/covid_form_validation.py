from django.core.exceptions import ValidationError
from edc_constants.constants import *
from edc_form_validators import FormValidator


class Covid9FormValidator(FormValidator):
    def clean(self):

        required_fields = [
            'date_of_test', 'is_test_estimated', 'reason_for_testing', 'result_of_test'
        ]

        for field in required_fields:
            self.required_if(YES,
                             field='test_for_covid',
                             field_required=field)

        self.m2m_required_if(YES,
                             field='test_for_covid',
                             m2m_field='isolations_symptoms')

        self.required_if(POS,
                         field='result_of_test',
                         field_required='isolation_location')

        self.validate_other_specify(field='reason_for_testing',
                                    other_specify_field='other_reason_for_testing')
        self.validate_other_specify(field='isolation_location',
                                    other_specify_field='other_isolation_location')

        self.required_if(YES,
                         field='has_tested_positive',
                         field_required='date_of_test_member')

        single_selection_fields = ['isolations_symptoms', 'symptoms_for_past_14days']

        for field in single_selection_fields:
            self.m2m_single_selection_if('no_symptoms', m2m_field=field)

        self._validations_if_fully_vaccinated()

        self._validations_if_partially_vaccinated()

        return super(Covid9FormValidator, self).clean()

    def _validations_if_fully_vaccinated(self):

        if self.cleaned_data.get('fully_vaccinated') == YES:

            required_fields = ['vaccination_type', 'first_dose', 'second_dose']

            for field in required_fields:
                self.required_if(YES,
                                 field='fully_vaccinated',
                                 field_required=field)

            self.validate_other_specify(field='vaccination_type',
                                        other_specify_field='other_vaccination_type')

    def _validations_if_partially_vaccinated(self):

        if self.cleaned_data.get('fully_vaccinated') == 'partially_jab':

            required_fields = ['vaccination_type', 'first_dose']

            for field in required_fields:
                self.required_if('partially_jab',
                                 field='fully_vaccinated',
                                 field_required=field)

        self.validate_other_specify(field='vaccination_type',
                                    other_specify_field='other_vaccination_type')

        self.not_required_if('partially_jab', field='fully_vaccinated', field_required='second_dose')
