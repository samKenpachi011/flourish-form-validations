import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE

from ..form_validators import TbAdolConsentFormValidator
from .models import SubjectConsent, ScreeningPregWomen, FlourishConsentVersion
from .test_model_mixin import TestModeMixin
from faker import Faker


@tag('tb_adol')
class TestTBAdolConsent(TestModeMixin, TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(TbAdolConsentFormValidator, *args, **kwargs)
    
    def setUp(self):
        
        fake = Faker()
        subject_identifier = '11111111'
        screening_identifier = ''
        first_name = fake.first_name()
        last_name = fake.last_name()
        initials = f'{first_name[0]}{last_name[0]}'
        is_literate = YES
        dob = (get_utcnow() - relativedelta(years=25)).date()
        is_dob_estimated = NO
        citizen = YES
        identity = '419129017'
        
    
        
        SubjectConsent.objects.create(
            
            subject_identifier=subject_identifier,
            screening_identifier=screening_identifier,
            gender='F',
            dob=dob,
            consent_datetime=get_utcnow(),
            version='1', 
            first_name = first_name,
            last_name = last_name,
            initials = initials,
            is_literate = is_literate,
            is_dob_estimated = is_dob_estimated,
            citizen = citizen,
            identity = identity,
            confirm_identity = identity),
        
        
        self.clean_data = {
            'subject_identifier': subject_identifier,
            'citizen': citizen,
            'legal_marriage': NOT_APPLICABLE,
            'marriage_certificate': NOT_APPLICABLE,
            'marriage_certificate_no': None,
            'identity': identity,
            'confirm_identity': identity,
            'first_name': first_name,
            'last_name': last_name,
            'is_dob_estimated': is_dob_estimated,
            'guardian_name': None,
            'subject_type': '',
            'consent_reviewed': YES,
            'study_questions': YES,
            'assessment_score': YES,
            'consent_signature': YES,
            'consent_copy': YES,
            'is_incarcerated': None,
            'is_literate': is_literate,
            'witness_name': '',
            'language': 'tn',
            'is_verified': False,
            'is_verified_datetime': None,
            'verified_by': None,
            'report_datetime': datetime.datetime(2022, 11, 9, 8, 31, 48),
            'version': '1',
            'updates_versions': False,
            'sid': None,
            'comment': None,
            'dm_comment': None,
            'initials': initials,
            'consent_datetime': datetime.datetime(2022, 11, 9, 8, 31, 48),
            'identity_type': 'country_id',
            'gender': None,
            'dob': dob,
            'tb_blood_test_consent': YES,
            'future_studies_contact': YES,
            'samples_future_studies': YES,
            'is_eligible': True,
            'gender_other': None}
        
    def test_first_name_not_same(self):
        self.clean_data['first_name'] = 'Diff'
        
        form_validator = TbAdolConsentFormValidator(
            cleaned_data=self.clean_data
        )
        
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('first_name', form_validator._errors)
        
    def test_last_name_not_same(self):
        self.clean_data['last_name'] = 'Diff'
        
        form_validator = TbAdolConsentFormValidator(
            cleaned_data=self.clean_data
        )
        
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('last_name', form_validator._errors)
        
    def test_initial_not_same(self):
        self.clean_data['initials'] = 'XX'
        
        form_validator = TbAdolConsentFormValidator(
            cleaned_data=self.clean_data
        )
        
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('initials', form_validator._errors)
    
        
    def test_dob_not_same(self):
        self.clean_data['dob'] = (get_utcnow() - relativedelta(years=24)).date()
        
        
        form_validator = TbAdolConsentFormValidator(
            cleaned_data=self.clean_data
        )
        
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('dob', form_validator._errors)
        
        

                    
                    
                    