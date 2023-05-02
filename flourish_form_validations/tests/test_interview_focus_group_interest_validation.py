from django.test import TestCase
from django.core.exceptions import ValidationError
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import InterviewFocusGroupInterestFormValidator
from .models import (FlourishConsentVersion, SubjectConsent, MaternalDelivery,
                     Appointment, MaternalVisit, CaregiverChildConsent)

from dateutil.relativedelta import relativedelta


class CustomInterviewFocusGroupInterestFormValidator(InterviewFocusGroupInterestFormValidator):

    def caregiver_child_consent_cls(self):
        return CaregiverChildConsent


class TestMaternalDeliveryFormValidator(TestCase):

    def setUp(self):
        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111',
            screening_identifier='ABC12345',
            gender='F',
            dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(),
            version='1')

        self.caregiver_child_consent = CaregiverChildConsent.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            child_dob=get_utcnow(),
            consent_datetime=get_utcnow(),
            preg_enroll=False,
        )

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow())

        self.clean_data = {
            'maternal_visit': self.maternal_visit,
            'discussion_pref': 'group',
            'hiv_group_pref': 'same_status',
            'infant_feeding': 'one_on_one',
            'school_performance': 'one_on_one',
            'adult_mental_health': 'one_on_one',
            'child_mental_health': 'one_on_one',
            'sexual_health': 'one_on_one',
            'hiv_topics': 'one_on_one',
            'food_insecurity': 'one_on_one',
            'wellness': 'one_on_one',
            'non_comm_diseases': 'one_on_one',
            'social_issues': 'one_on_one',
            'covid19': 'one_on_one',
            'vaccines': 'one_on_one',
            'infant_feeding_group_interest': 'YES',
            'same_status_comfort': 'YES',
            'diff_status_comfort': 'YES',
            'women_discussion_topics': 'Family planning methods',
            'adolescent_discussion_topics': 'Peer pressure and decision-making'
        }

    def test_hiv_group_pref_not_required(self):
        self.clean_data['discussion_pref'] = 'unsure'
        self.clean_data['hiv_group_pref'] = 'same_status'
        form_validator = InterviewFocusGroupInterestFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hiv_group_pref', form_validator._errors)

    def test_hiv_group_pref_required(self):
        self.clean_data['discussion_pref'] = 'group'
        self.clean_data['hiv_group_pref'] = None
        form_validator = InterviewFocusGroupInterestFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hiv_group_pref', form_validator._errors)

    def test_infant_feeding_group_interest_required(self):
        self.clean_data['infant_feeding_group_interest'] = None
        form_validator = CustomInterviewFocusGroupInterestFormValidator(cleaned_data=self.clean_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_infant_feeding_group_interest_not_required(self):
        self.caregiver_child_consent.preg_enroll = True
        self.caregiver_child_consent.save()
        form_validator = CustomInterviewFocusGroupInterestFormValidator(cleaned_data=self.clean_data)

        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_same_status_comfort_required(self):
        self.clean_data['hiv_group_pref'] = 'group'
        self.clean_data['same_status_comfort'] = None
        self.caregiver_child_consent.preg_enroll = True
        self.caregiver_child_consent.save()

        form_validator = CustomInterviewFocusGroupInterestFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('same_status_comfort', form_validator._errors)

    def test_same_status_comfort_not_required(self):
        self.clean_data['discussion_pref'] = 'unsure'
        self.clean_data['hiv_group_pref'] = None
        self.clean_data['same_status_comfort'] = "blah"
        self.caregiver_child_consent.preg_enroll = True
        self.caregiver_child_consent.save()

        form_validator = CustomInterviewFocusGroupInterestFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('same_status_comfort', form_validator._errors)
