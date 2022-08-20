from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS, NEG
from ..form_validators import RelationshipFatherInvolmentFormValidator
from flourish_form_validations.tests.test_model_mixin import TestModeMixin
from .models import (FlourishConsentVersion, SubjectConsent,
                     Appointment, MaternalVisit, ListModel)
from dateutil.relativedelta import relativedelta
from edc_constants.constants import OTHER



@tag('rfi')
class TestRelationshipFatherInvolment(TestModeMixin,TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(RelationshipFatherInvolmentFormValidator, *args, **kwargs)
        
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

        self.options = {
            'maternal_visit': self.maternal_visit,

        }
        
        # self.data = {
            # 'maternal_visit': self.maternal_visit,
            # 'partner_present':YES,
            # 'why_partner_upsent':'test'
            # 'is_partner_the_father':YES,
            # 'duration_with_partner': '12',
            # 'partner_age_in_years':'30',
            # 'living_with_partner':YES,
            # 'not_living_with_partner':,
            # 'disclosure_to_partner':,
            # 'discussion_with_partner':,
            # 'disclose_status':,
            # 'partners_support':,
            # 'ever_separated':,
            # 'times_separated':,
            # 'separation_consideration':,
            # 'after_fight':,
            # 'relationship_progression':,
            # 'confide_in_partner':,
            # 'relationship_regret':,
            # 'quarrel_frequency':,
            # 'bothering_partner':,
            # 'kissing_partner':,
            # 'engage_in_interests':,
            # 'happiness_in_relationship':,
            # 'future_relationship':,
            # 'father_child_contact':,
            # 'fathers_financial_support':,
            # 'child_left_alone':,
            # 'read_books':,
            # 'told_stories':,
            # 'sang_songs':,
            # 'took_child_outside':,
            # 'played_with_child':,
            # 'named_with_child':
            # }
        
        """Test criteria's
        -form valid
                """
    def test_father_involvement_form_valid(self):
        
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'partner_present':YES,
            'is_partner_the_father':YES,
            'duration_with_partner_months': '1',
            'duration_with_partner_years': '1',
            'partner_age_in_years':'30',
            'living_with_partner':YES,
            'disclosure_to_partner':YES,
            'discussion_with_partner': 'easy',
            'disclose_status':YES,
            'partners_support':'supportive',
            'ever_separated':YES,
            'times_separated':'twice',
            'separation_consideration':'occasionally',
            
            'after_fight':'occasionally',
            'relationship_progression':'occasionally',
            'confide_in_partner':'occasionally',
            'relationship_regret':'occasionally',
            'quarrel_frequency':'occasionally',
            'bothering_partner':'occasionally',
            'kissing_partner':'occasionally',
            'engage_in_interests':'occasionally',
            
            'happiness_in_relationship':'happy',
            'future_relationship':'happy',
            'father_child_contact':'every_day',
            'fathers_financial_support':'supportive',
            'child_left_alone':3,
            'read_books':'mother',
            'told_stories':'mother',
            'sang_songs':'mother',
            'took_child_outside':'mother',
            'played_with_child':'mother',
            'named_with_child':'mother',
        } 
            
        form_validator = RelationshipFatherInvolmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}') 
        
        
        """ Validations
        
        -If ‘Yes’ to Q1, continue to Q2, 
        -If “No” to Q1, provide short answer stem question “Why not?” (allow free text) otherwise skip to Q23
        -If “No” to Q5, provide short answer stem question “Why not?” (allow free text) otherwise skip to Q6
        -If “Yes” on Q6 go to Q7
            If “No” skip to Q8
        -If “Yes” to Q10, continue to Q11. Otherwise skip to Q12


        -test validate_why_partner_upsent_required on YES and NO
        -test validate_why_not_living_with_partner
        -test validate_is_partner_the_father_required
        -test validate_not_living_with_partner_required
        -test validate_discussion_with_partner_required
        -test validate_disclose_status_required
        -test validate_times_separated_required
        -test validate_separation_consideration_required


        """

    

        
        
        
        
        