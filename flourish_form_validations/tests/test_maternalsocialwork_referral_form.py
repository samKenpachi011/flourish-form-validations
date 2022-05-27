from django.test import TestCase
from django.core.exceptions import ValidationError
from edc_constants.constants import OTHER 

from ..form_validators import CaregiverSocialWorkReferralFormValidator
from .models import ListModel

class TestMaternalSocialWorkReferralForm(TestCase):
    
    
    def setUp(self):
        
        ListModel.objects.create(name='financial_challenges')
        
        self.options = {
            'referral_reason': ListModel.objects.all()
        }


    def test_socialwork_referral_specify_required(self):
        """ Assert that the SocialWork Referral specify raises an error if referral
            reason includes other referral specify, but not specified.
        """
        ListModel.objects.create(name=OTHER)
        self.options.update(
            referral_reason=ListModel.objects.all(),
            reason_other=None)
        form_validator = CaregiverSocialWorkReferralFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reason_other', form_validator._errors)

    def test_socialwork_referral_specify_valid(self):
        """ Tests if SocialWork Referral includes other referral and
            reason_other is specified, cleaned data validates or fails the
            tests if the Validation Error is raised unexpectedly.
        """
        ListModel.objects.create(name=OTHER)
        self.options.update(
            referral_reason=ListModel.objects.all(),
            reason_other='blah')
        form_validator = CaregiverSocialWorkReferralFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
