from edc_form_validators import FormValidator


class CaregiverReferralFormValidator(FormValidator):

    def clean(self):

        self.validate_other_specify(field='referred_to')
