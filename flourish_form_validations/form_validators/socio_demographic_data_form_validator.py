from edc_form_validators import FormValidator

from .crf_form_validator import CRFFormValidator


class SocioDemographicDataFormValidator(CRFFormValidator, FormValidator):

    def clean(self):
        super().clean()

        self.validate_other_specify(
            field='marital_status',
        )

        self.validate_other_specify(
            field='ethnicity',
        )

        self.validate_other_specify(
            field='current_occupation',
        )

        self.validate_other_specify(
            field='provides_money',
        )

        self.validate_other_specify(
            field='money_earned',
        )

        self.validate_other_specify(
            field='toilet_facility',
        )
