from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase,tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from ..form_validators import MaternalArvPostAdherenceFormValidator
from .models import ArvsPrePregnancy, SubjectConsent, FlourishConsentVersion
from .models import MaternalVisit, Appointment
from .test_model_mixin import TestModeMixin

@tag('mdp')
class TestMaternalArvPostAdherenceForm(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(MaternalArvPostAdherenceFormValidator, *args, **kwargs)

    def setUp(self):

        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')

        self.subject_identifier = '11111111'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(),)

        self.appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000M')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=self.appointment,
            subject_identifier=self.subject_consent.subject_identifier)

    def test_medication_interrupted_invalid(self):
        '''Assert raises if arvs was interrupted but
        no reasons were given.

                'maternal_visit',
                'report_datetime',
                'missed_arv',
                'interruption_reason',
                'interruption_reason_other',
                'comment',
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'missed_arv': 2,
            'interruption_reason': NOT_APPLICABLE,
            'comment': 'comment',
        }
        form_validator = MaternalArvPostAdherenceFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
