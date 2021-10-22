from django.core.exceptions import ValidationError
from edc_constants.constants import YES, OTHER, NOT_APPLICABLE
from edc_form_validators import FormValidator


class Covid9FormValidator(FormValidator):
    def clean(self):

        required_fields = [
            'date_of_test', 'is_test_estimated', 'reason_for_testing', 'result_of_test',
            'isolation_location', 'isolations_symptoms'
        ]



        for field in required_fields:

            if field == 'isolations_symptoms':
                self.m2m_required_if(YES,
                                     field='test_for_covid',
                                     m2m_field='isolations_symptoms')
                continue

            self.required_if(YES, field='test_for_covid', field_required=field)

        self.validate_other_specify(field='reason_for_testing',
                                    other_specify_field='other_reason_for_testing')
        self.validate_other_specify(field='isolation_location',
                                    other_specify_field='other_isolation_location')

        required_fields = ['date_of_test_member', 'is_test_estimated', 'close_contact']

        for field in required_fields:

            self.required_if(YES,
                             field='has_tested_positive',
                             field_required=field)

        self.m2m_single_selection_if('no_symptoms', m2m_field='symptoms_for_past_14days')

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
