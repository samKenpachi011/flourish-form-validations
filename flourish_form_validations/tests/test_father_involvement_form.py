from django.test import tag, TestCase
from django.core.exceptions import ValidationError
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS, NEG
from ..form_validators import RelationshipFatherInvolvementFormValidator
from flourish_form_validations.tests.test_model_mixin import TestModeMixin
from .models import (FlourishConsentVersion, SubjectConsent,
                     Appointment, MaternalVisit, ListModel)
from dateutil.relativedelta import relativedelta
from edc_constants.constants import OTHER
from ..form_validators import RelationshipFatherInvolvementFormValidator


@tag('rfi') 
class TestRelationshipFatherInvolvement(TestModeMixin,TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(RelationshipFatherInvolvementFormValidator, *args, **kwargs)
        
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
            visit_code='1000')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow())
        
        
        self.clean_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present': YES,
            'why_partner_absent': '',
            'is_partner_the_father': YES,
            'duration_with_partner': 10,
            'partner_age_in_years': 29,
            'living_with_partner': YES,
            'why_not_living_with_partner': None,
            'disclosure_to_partner': YES,
            'discussion_with_partner': 'very_easy',
            'disclose_status': YES,
            'partners_support': 'neutral',
            'ever_separated': NO,
            'times_separated': '',
            'separation_consideration': 'most_of_the_time',
            'leave_after_fight': 'most_of_the_time',
            'relationship_progression': 'most_of_the_time',
            'confide_in_partner': 'most_of_the_time',
            'relationship_regret': 'most_of_the_time',
            'quarrel_frequency': 'most_of_the_time',
            'bothering_partner': 'most_of_the_time',
            'kissing_partner': 'most_of_the_time',
            'engage_in_interests': 'most_of_the_time',
            'happiness_in_relationship': 'perfect',
            'future_relationship': 'do_what_I_can',
            'biological_father_alive': YES,
            'father_child_contact': 'every_week_weekend',
            'fathers_financial_support': 'PNTA',
            'child_left_alone': 5,
            'read_books': 'father',
            'told_stories': 'mother',
            'sang_songs': 'mother',
            'took_child_outside': 'mother',
            'played_with_child': 'mother',
            'named_with_child': 'mother',
            'interview_participation': YES,
            'contact_info': YES,
            'partner_cell': '71217787',
            'conunselling_referral': YES}

    def test_partner_present_required_questions(self):
        
        self.clean_data['partner_present'] = YES
        self.clean_data.update({
            'why_partner_absent': None,
            'is_partner_the_father': None,
            'duration_with_partner': None,
            'partner_age_in_years': None,
            'living_with_partner': None,
            'why_not_living_with_partner': None,
            'disclosure_to_partner': None,
            'discussion_with_partner': None,
            'disclose_status': None,
            'partners_support': None,
            'ever_separated': None,
            'times_separated': None,
            'separation_consideration': None,
            'leave_after_fight': None,
            'relationship_progression': None,
            'confide_in_partner': None,
            'relationship_regret': None,
            'quarrel_frequency': None,
            'bothering_partner': None,
            'kissing_partner': None,
            'engage_in_interests': None,
            'happiness_in_relationship': None,
            'future_relationship': None,
        })
  
        
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)
        
        self.assertRaises(ValidationError, form_validator.validate)
        
    def test_why_partner_absent_required(self):
        
        self.clean_data['partner_present'] = NO
        
        self.clean_data.update({
            'why_partner_absent': None,
            'is_partner_the_father': None,
            'duration_with_partner': None,
            'partner_age_in_years': None,
            'living_with_partner': None,
            'why_not_living_with_partner': None,
            'disclosure_to_partner': None,
            'discussion_with_partner': None,
            'disclose_status': None,
            'partners_support': None,
            'ever_separated': None,
            'times_separated': None,
            'separation_consideration': None,
            'leave_after_fight': None,
            'relationship_progression': None,
            'confide_in_partner': None,
            'relationship_regret': None,
            'quarrel_frequency': None,
            'bothering_partner': None,
            'kissing_partner': None,
            'engage_in_interests': None,
            'happiness_in_relationship': None,
            'future_relationship': None,
        })

        
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)
        
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('why_partner_absent', form_validator._errors)
    
    
    def test_why_not_living_with_partner_required(self):
        
        self.clean_data.update({'partner_present': YES,
                                'why_partner_absent': '',
                                'is_partner_the_father': YES,
                                'duration_with_partner': 10,
                                'partner_age_in_years': 29,
                                'living_with_partner': NO,
                                'why_not_living_with_partner': None,
                                'disclosure_to_partner': YES,
                                'discussion_with_partner': 'very_easy',
                                'disclose_status': YES,
                                'partners_support': 'neutral',
                                'ever_separated': NO,
                                'times_separated': '',
                                'separation_consideration': 'most_of_the_time',
                                'leave_after_fight': 'most_of_the_time',
                                'relationship_progression': 'most_of_the_time',
                                'confide_in_partner': 'most_of_the_time',
                                'relationship_regret': 'most_of_the_time',
                                'quarrel_frequency': 'most_of_the_time',
                                'bothering_partner': 'most_of_the_time',
                                'kissing_partner': 'most_of_the_time',
                                'engage_in_interests': 'most_of_the_time',
                                'happiness_in_relationship': 'perfect',
                                'future_relationship': 'do_what_I_can',
                                'biological_father_alive': YES,
                                'father_child_contact': 'every_week_weekend',
                                'fathers_financial_support': 'PNTA',
                                'child_left_alone': 5,
                                'read_books': 'father',
                                'told_stories': 'mother',
                                'sang_songs': 'mother',
                                'took_child_outside': 'mother',
                                'played_with_child': 'mother',
                                'named_with_child': 'mother',
                                'interview_participation': YES,
                                'contact_info': YES,
                                'partner_cell': '71217787',
                                'conunselling_referral': YES})

        
        
        
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('why_not_living_with_partner', form_validator._errors)

                
    def test_contact_info_required(self):
        self.clean_data['contact_info'] = YES
        self.clean_data['partner_cell'] = None

        
        
        
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('partner_cell', form_validator._errors)
        
        
    def test_father_child_contact_required(self):

        self.clean_data['father_child_contact'] = NOT_APPLICABLE
        
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('father_child_contact', form_validator._errors)
        
    def test_fathers_financial_support_required(self):
        self.clean_data['fathers_financial_support'] = NOT_APPLICABLE
        
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('fathers_financial_support', form_validator._errors)
        
    def test_child_left_alone_required(self):
        self.clean_data['child_left_alone'] = 0
        
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('child_left_alone', form_validator._errors)
        
    def test_read_books_required(self):
        self.clean_data['read_books'] = NOT_APPLICABLE
        
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('read_books', form_validator._errors)
        
    def test_told_stories_required(self):
        self.clean_data['told_stories'] = NOT_APPLICABLE
        
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('told_stories', form_validator._errors)
        
    def test_sang_songs_required(self):
        self.clean_data['sang_songs'] = NOT_APPLICABLE
        
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('sang_songs', form_validator._errors)
        
    def test_took_child_outside_required(self):
        self.clean_data['took_child_outside'] = NOT_APPLICABLE
        
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('took_child_outside', form_validator._errors)
        
    def test_father_alive(self):
        self.clean_data['biological_father_alive'] = NO
        
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)

        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('biological_father_alive', form_validator._errors)

    def test_father_alive_valid(self):
        self.clean_data['is_partner_the_father'] = NO
        self.clean_data['biological_father_alive'] = 'PNTA'
        self.clean_data['father_child_contact'] = None
        self.clean_data['fathers_financial_support'] = None
        form_validator = RelationshipFatherInvolvementFormValidator(cleaned_data=self.clean_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')