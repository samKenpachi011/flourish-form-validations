from edc_form_validators import FormValidator
from edc_constants.constants import OTHER, YES, POS, NEG
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class BreastFeedingQuestionnaireFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_during_preg_influencers()
        self.validate_after_delivery_influencers()
        self.validate_infant_feeding_reasons()
        self.validate_influenced_during_preg_required()
        self.validate_influenced_after_delivery_required()
        self.validate_feeding_hiv_status()
        self.validate_infant_feeding_reasons_required()
        self.validate_hiv_status_during_preg_not_req()
        self.validate_hiv_status_during_preg_applicable()
        self.validate_six_months_feeding_req()

    def validate_during_preg_influencers(self):
        self.m2m_other_specify(OTHER,
                               m2m_field='during_preg_influencers',
                               field_other='during_preg_influencers_other')

    def validate_after_delivery_influencers(self):
        self.m2m_other_specify(OTHER,
                               m2m_field='after_delivery_influencers',
                               field_other='after_delivery_influencers_other')

    def validate_infant_feeding_reasons(self):
        self.m2m_other_specify(OTHER,
                               m2m_field='infant_feeding_reasons',
                               field_other='infant_feeding_other')

    def validate_hiv_status_during_preg_not_req(self):
        hiv_status = self.cleaned_data.get('hiv_status_during_preg')
        required_fields = ['breastfeeding_duration',
                           'use_medicines',
                           'delivery_advice_vl_results',
                           'father_knew_hiv_status',
                           'hiv_status_known_by',
                           'after_delivery_advice_vl_results',
                           'delivery_advice_on_viralload',
                           'after_delivery_advice_on_viralload']
        for required_field in required_fields:
            self.required_if_true(not hiv_status == NEG,
                                  field_required=required_field)

    def validate_hiv_status_during_preg_applicable(self):
        required_fields = ['use_medicines',
                           'received_training',
                           'training_outcome',
                           'feeding_advice', ]
        for required_field in required_fields:
            self.applicable_if(POS,
                               field='hiv_status_during_preg',
                               field_applicable=required_field)

    def validate_influenced_during_preg_required(self):
        influencers = self.cleaned_data.get('during_preg_influencers')
        self.required_if_true(influencers != 'OTHER',
                              field='during_preg_influencers',
                              field_required='influenced_during_preg')

    def validate_influenced_after_delivery_required(self):
        influencers = self.cleaned_data.get('after_delivery_influencers')
        self.required_if_true((influencers != 'OTHER'),
                              field='after_delivery_influencers',
                              field_required='influenced_after_delivery')

    def validate_infant_feeding_reasons_required(self):

        status = self.cleaned_data.get('six_months_feeding')
        self.required_if_true(status in ['Yes', 'do_not_remember'],
                              field='six_months_feeding',
                              field_required='infant_feeding_reasons')

    def validate_feeding_hiv_status(self):

        status = self.cleaned_data.get('feeding_hiv_status')
        required_fields = ['hiv_status_aware', 'on_hiv_status_aware']
        for field in required_fields:
            self.required_if_true(status in ['No', 'rather_not_answer'],
                                  field='feeding_hiv_status',
                                  field_required=field)

    def validate_six_months_feeding_req(self):
        self.required_if(YES,
                         field='six_months_feeding',
                         field_required='infant_feeding_reasons')
