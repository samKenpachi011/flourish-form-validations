from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NOT_APPLICABLE

from ..form_validators import CaregiverClinicalMeasurementsFormValidator
from .models import SubjectConsent, MaternalVisit, Appointment, FlourishConsentVersion
from .test_model_mixin import TestModeMixin


@tag('ccm')
class TestCaregiverClinicalMeasurementsForm(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(CaregiverClinicalMeasurementsFormValidator, *args, **kwargs)

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

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2001M')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow())
        
        self.options = {
            'maternal_visit': self.maternal_visit,
            
        }
           
        

    def test_waist_circ_required_invalid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_preg': YES,
            'waist_circ': 15,            
        }
        form_validator = CaregiverClinicalMeasurementsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('waist_circ', form_validator._errors)

    def test_hip_circ_required_invalid(self):

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2000D')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow())

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'hip_circ': 15
        }
        form_validator = CaregiverClinicalMeasurementsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hip_circ', form_validator._errors)

    def test_hip_circ_required_valid(self):

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2000')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow())

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'hip_circ': 15,
            'waist_circ': 15
        }
        form_validator = CaregiverClinicalMeasurementsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_weight_required(self):
        """
        If weigh is available (YES), then weight_kg is required or else
        """

        self.options['weight_available'] = YES
        self.options['weight_kg'] = None

        form_validator = CaregiverClinicalMeasurementsFormValidator(cleaned_data=self.options)

        self.assertRaises(ValidationError, form_validator.validate)


    

   