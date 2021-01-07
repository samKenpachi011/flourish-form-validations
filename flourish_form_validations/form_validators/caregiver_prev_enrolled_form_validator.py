from edc_constants.constants import YES, NO
from edc_form_validators.form_validator import FormValidator


class CaregiverPrevEnrolledFormValidator(FormValidator):

    def clean(self):
        fields_required = ['current_hiv_status', 'last_test_date', ]
        for field_required in fields_required:
            self.required_if(
                YES,
                field='maternal_prev_enroll',
                field_required=field_required)

        self.required_if(
            YES,
            field='last_test_date',
            field_required='test_date')

        self.required_if(
            YES,
            field='last_test_date',
            field_required='is_date_estimated')

        fields_required = ['sex', 'relation_to_child', ]
        for field_required in fields_required:
            self.required_if(
                NO,
                field='maternal_prev_enroll',
                field_required=field_required)

        self.validate_other_specify(field='relation_to_child')
