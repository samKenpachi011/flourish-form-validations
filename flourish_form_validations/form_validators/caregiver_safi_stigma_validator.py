from edc_form_validators import FormValidator

from .crf_form_validator import FormValidatorMixin


class CaregiverSafiStigmaFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        super().clean()
        self.validate_period_required()

    def validate_period_required(self):

        fields = [
            'judged',
            'avoided',
            'discriminated',
            'at_home',
            'at_neigborhood',
            'at_religious',
            'at_clinic',
            'at_workplace',
            'finacial_support',
            'social_support',
            'stressed',
            'saddened',
            'isolated',
            'insulted',
            'home_discr',
            'neighborhood_discr',
            'religious_place_discr',
            'clinic_discr',
            'social_effect',
            'emotional_effect',
            'pespective_changed'
        ]

        for field in fields:
            self.required_if(
                'ever_happened',
                field=field,
                field_required=f'{field}_period'
            )

        fields_required = {'other_place': 'other_place_period',
                           'other_discr': 'other_discr_period'}

        for field, required in fields_required.items():
            self.required_if_not_none(
                field=field,
                field_required=required, )
