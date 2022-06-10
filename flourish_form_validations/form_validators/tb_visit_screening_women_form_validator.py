from edc_constants.constants import YES, NO, UNKNOWN, DWTA
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class TbVisitScreeningWomenFormValidator(FormValidatorMixin, FormValidator):
    responses = [NO, UNKNOWN, DWTA]

    def clean(self):
        super().clean()

        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        self.validate_fever()
        self.validate_night_sweats()
        self.validate_weight_loss()
        self.validate_cough_blood()
        self.validate_enlarged_lymph_nodes()
        self.validate_cough()

    def validate_cough(self):
        have_cough_required_field = [
            'cough_duration_preg',
            'seek_med_help',
            'cough_num'
        ]
        cough_illness_required_field = [
            'cough_illness_times',
            'cough_illness_preg',
            'cough_illness_med_help'
        ]
        self.required_if(
            YES,
            field='have_cough',
            field_required='cough_duration'
        )
        for field in have_cough_required_field:
            self.required_if(
                YES,
                field='cough_intersects_preg',
                field_required=field
            )
        for field in cough_illness_required_field:
            self.required_if(
                YES,
                field='cough_illness',
                field_required=field
            )

    def validate_fever(self):
        fever_during_preg_required_fields = [
            'fever_illness_times',
            'fever_illness_preg',
        ]
        fever_illness_postpartum_required_fields = [
            'fever_illness_postpartum_times',
            'fever_illness_postpartum_preg',
        ]
        for field in fever_during_preg_required_fields:
            self.required_if(
                YES,
                field='fever_during_preg',
                field_required=field
            )
        for field in fever_illness_postpartum_required_fields:
            self.required_if(
                YES,
                field='fever_illness_postpartum',
                field_required=field
            )

    def validate_night_sweats(self):
        night_sweats_during_preg_required_fields = [
            'night_sweats_during_preg_times',
            'night_sweats_during_preg_clinic',
        ]
        night_sweats_postpartum_required_fields = [
            'night_sweats_postpartum_times',
            'night_sweats_postpartum_clinic',
        ]
        for field in night_sweats_during_preg_required_fields:
            self.required_if(
                YES,
                field='night_sweats_during_preg',
                field_required=field
            )
        for field in night_sweats_postpartum_required_fields:
            self.required_if(
                YES,
                field='night_sweats_postpartum',
                field_required=field
            )

    def validate_weight_loss(self):
        weight_loss_during_preg_required_fields = [
            'weight_loss_during_preg_times',
            'weight_loss_during_preg_clinic',
        ]
        weight_loss_postpartum_required_fields = [
            'weight_loss_postpartum_times',
            'weight_loss_postpartum_clinic',
        ]
        for field in weight_loss_during_preg_required_fields:
            self.required_if(
                YES,
                field='weight_loss_during_preg',
                field_required=field
            )
        for field in weight_loss_postpartum_required_fields:
            self.required_if(
                YES,
                field='weight_loss_postpartum',
                field_required=field
            )

    def validate_enlarged_lymph_nodes(self):
        enlarged_lymph_nodes_during_preg_required_fields = [
            'enlarged_lymph_nodes_during_preg_times',
            'enlarged_lymph_nodes_during_preg_clinic',
        ]
        enlarged_lymph_nodes_postpartum_required_fields = [
            'enlarged_lymph_nodes_postpartum_times',
            'enlarged_lymph_nodes_postpartum_clinic',
        ]
        for field in enlarged_lymph_nodes_during_preg_required_fields:
            self.required_if(
                YES,
                field='enlarged_lymph_nodes_during_preg',
                field_required=field
            )
        for field in enlarged_lymph_nodes_postpartum_required_fields:
            self.required_if(
                YES,
                field='enlarged_lymph_nodes_postpartum',
                field_required=field
            )

    def validate_cough_blood(self):
        cough_blood_during_preg_required_fields = [
            'cough_blood_during_preg_times',
            'cough_blood_during_preg_clinic',
        ]
        cough_blood_postpartum_required_fields = [
            'cough_blood_postpartum_times',
            'cough_blood_postpartum_clinic',
        ]
        for field in cough_blood_during_preg_required_fields:
            self.required_if(
                YES,
                field='cough_blood_during_preg',
                field_required=field
            )
        for field in cough_blood_postpartum_required_fields:
            self.required_if(
                YES,
                field='cough_blood_postpartum',
                field_required=field
            )

    def validate_unexplained_fatigues(self):
        unexplained_fatigue_during_preg_required_fields = [
            'unexplained_fatigue_during_preg_times',
            'unexplained_fatigue_during_preg_clinic',
        ]
        unexplained_fatigue_postpartum_required_fields = [
            'unexplained_fatigue_postpartum_times',
            'unexplained_fatigue_postpartum_clinic',
        ]
        for field in unexplained_fatigue_during_preg_required_fields:
            self.required_if(
                YES,
                field='unexplained_fatigue_during_preg',
                field_required=field
            )
        for field in unexplained_fatigue_postpartum_required_fields:
            self.required_if(
                YES,
                field='unexplained_fatigue_postpartum',
                field_required=field
            )
