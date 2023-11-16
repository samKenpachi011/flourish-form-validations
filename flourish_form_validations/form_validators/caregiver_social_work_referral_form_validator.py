from .crf_form_validator import FormValidatorMixin
from .social_work_referral_validator_mixin import SocialWorkReferralValidatorMixin


class CaregiverSocialWorkReferralFormValidator(
        SocialWorkReferralValidatorMixin, FormValidatorMixin):

    def clean(self):
        super().clean()
