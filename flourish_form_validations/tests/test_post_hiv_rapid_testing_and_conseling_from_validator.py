
from datetime import timedelta
from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from edc_base.utils import get_utcnow

from .test_model_mixin import TestModeMixin
from ..form_validators import PostHIVRapidTestCounselingFormValidator
from .models import FlourishConsentVersion, SubjectConsent, Appointment, MaternalVisit
from dateutil.relativedelta import relativedelta


class TestPostHIVRapidTestCounselingFormValidator(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(PostHIVRapidTestCounselingFormValidator, *args, **kwargs)

    def setUp(self):

        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow())

        appointment = Appointment.objects.create(
            subject_identifier=subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='3000')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=appointment.subject_identifier,
            report_datetime=get_utcnow())

        self.cleaned_data = {
            'report_datetime': get_utcnow(),
            'subject_identifier': appointment.subject_identifier,
            'maternal_visit': self.maternal_visit,
            'rapid_test_done': 'Yes',
            'result_date': get_utcnow().date(),
            'result': 'POS',
            'reason_not_tested': None,
            'reason_not_tested_other': None,
            'comment': ''
        }

    def test_result_date_within_3months(self):
        """An exception should be thrown when test results are 3 months and older
        """

        form_validator = PostHIVRapidTestCounselingFormValidator(
            cleaned_data=self.cleaned_data)

        result_date = get_utcnow().date() - relativedelta(months=4)

        self.assertRaises(
            ValidationError, form_validator.validate_test_date, result_date)
        self.assertIn('result_date', form_validator._errors)
