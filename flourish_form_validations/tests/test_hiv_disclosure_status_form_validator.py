from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import tag, TestCase
from django.utils import timezone
from edc_base import get_utcnow
from edc_constants.constants import FEMALE

from flourish_form_validations.form_validators import HIVDisclosureStatusFormValidator
from flourish_form_validations.tests.models import Appointment, CaregiverChildConsent, \
    MaternalVisit
from flourish_form_validations.tests.test_model_mixin import TestModeMixin


@tag('hiv_disclosure_status')
class TestHIVDisclosureStatusFormValidator(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(HIVDisclosureStatusFormValidator, *args, **kwargs)

    def setUp(self):
        self.subject_identifier = '2334432'

        CaregiverChildConsent.objects.create(
            consent_datetime=get_utcnow(),
            child_dob=get_utcnow() - relativedelta(years=6),
            subject_identifier='2334432-10')

        appointment = Appointment.objects.create(
            subject_identifier='2334432-10',
            appt_datetime=timezone.now(),
            visit_code='2000',)

        self.maternal_visit = MaternalVisit.objects.create(
            subject_identifier=appointment.subject_identifier,
            appointment=appointment)

    def test_validation_for_child_age_passes(self):
        form_data = {'maternal_visit': self.maternal_visit,
                     'disclosed_status': 'Yes',
                     'disclosure_age': 2}
        form_validator = HIVDisclosureStatusFormValidator(
            cleaned_data=form_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.assertNotIn('disclosure_age', e)

    def test_validation_for_child_age_fail(self):
        form_data = {'maternal_visit': self.maternal_visit,
                     'disclosed_status': 'Yes',
                     'who_disclosed': 'blah blah',
                     'disclosure_difficulty': 'blah blah',
                     'child_reaction': 'blah blah',
                     'disclosure_age': 10}
        form_validator = HIVDisclosureStatusFormValidator(
            cleaned_data=form_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('disclosure_age', form_validator._errors)
