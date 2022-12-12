from django.apps import apps as django_apps
from django.forms import ValidationError
from edc_constants.constants import OTHER, YES, POS, NEG
from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class BreastFeedingQuestionnaireFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_preg_influence_required()
        self.validate_feeding_hiv_status()
        self.validate_hiv_status_neg()

        self.m2m_other_specify(OTHER,
                               m2m_field='during_preg_influencers',
                               field_other='during_preg_influencers_other')

        self.m2m_other_specify(OTHER,
                               m2m_field='after_delivery_influencers',
                               field_other='after_delivery_influencers_other')

        self.m2m_other_specify(OTHER,
                               m2m_field='infant_feeding_reasons',
                               field_other='infant_feeding_other')

        hiv_status = self.cleaned_data.get('hiv_status_during_preg')
        self.required_if_true(not hiv_status == NEG,
                              field_required='use_medicines')

        required_fields = ['training_outcome',
                           'feeding_advice', ]
        for required_field in required_fields:
            self.required_if(POS,
                             field='hiv_status_during_preg',
                             field_required=required_field)

        self.required_if_true(not hiv_status == POS,
                              field_required='received_training',)

        self.required_if(YES,
                         field='six_months_feeding',
                         field_required='infant_feeding_reasons')

        self.required_if(YES,
                         field='six_months_feeding',
                         field_required='infant_feeding_reasons')

        self.validate_other_specify(field='after_birth_opinion')

    def validate_hiv_status_neg(self):
        hiv_status = self.cleaned_data.get('hiv_status_during_preg')
        required_fields = [
            'hiv_status_known_by',
            'father_knew_hiv_status',
            'delivery_advice_vl_results',
            'delivery_advice_on_viralload',
            'after_delivery_advice_vl_results',
            'after_delivery_advice_on_viralload',
            'breastfeeding_duration',
        ]
        for field in required_fields:
            self.required_if_true(not hiv_status == NEG,
                                  field_required=field,)

    def validate_preg_influence_required(self):
        influencers = self.cleaned_data.get('during_preg_influencers')
        self.required_if_true(influencers != 'OTHER',
                              field='during_preg_influencers',
                              field_required='influenced_during_preg')

        influencers = self.cleaned_data.get('after_delivery_influencers')
        self.required_if_true((influencers != 'OTHER'),
                              field='after_delivery_influencers',
                              field_required='influenced_after_delivery')

    def validate_feeding_hiv_status(self):

        status = self.cleaned_data.get('feeding_hiv_status')
        required_fields = ['hiv_status_aware', 'on_hiv_status_aware']
        for field in required_fields:
            self.required_if_true(status in ['No', 'rather_not_answer'],
                                  field='feeding_hiv_status',
                                  field_required=field)
