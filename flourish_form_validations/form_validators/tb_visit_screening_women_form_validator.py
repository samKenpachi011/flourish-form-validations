from edc_constants.constants import YES, NO, UNKNOWN, DWTA
from edc_form_validators import FormValidator

from .crf_form_validator import CRFFormValidator


class TbVisitScreeningWomenFormValidator(CRFFormValidator, FormValidator):
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
        self.validate_have_cough()

    def validate_have_cough(self):
        self.required_if(
            YES,
            field='have_cough',
            field_required='cough_duration'
        )

    def validate_cough_intersects_preg(self):

        self.required_if(
            YES,
            field='cough_intersects_preg',
            field_required='cough_timing'
        )

    def validate_fever(self):
        self.required_if(
            YES,
            field='fever_during_preg',
            field_required='fever_timing'
        )

    def validate_night_sweats(self):
        self.required_if(
            YES,
            field='night_sweats_postpartum',
            field_required='night_sweats_timing'
        )

    def validate_weight_loss(self):
        self.required_if(
            YES,
            field='weight_loss_postpartum',
            field_required='weight_loss_timing'
        )

    def validate_cough_blood(self):
        self.required_if(
            YES,
            field='cough_blood_postpartum',
            field_required='cough_blood_timing'
        )

    def validate_enlarged_lymph_nodes(self):
        self.required_if(
            YES,
            field='enlarged_lymph_nodes_postpartum',
            field_required='lymph_nodes_timing'
        )
