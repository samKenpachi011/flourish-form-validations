from django.apps import apps as django_apps
from django.forms import ValidationError
from django.conf import settings
from edc_form_validators import FormValidator
from edc_constants.constants import OTHER, YES, POS, NEG, NO, NOT_APPLICABLE
from edc_form_validators import FormValidator
from flourish_caregiver.helper_classes import MaternalStatusHelper
from flourish_caregiver.constants import PNTA
from .crf_form_validator import FormValidatorMixin


class RelationshipFatherInvolvementFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):

        self.validate_required_fields()

        self.validate_positive_mother()

        self.required_if(NO,
                         field='partner_present',
                         field_required='why_partner_absent')

        self.not_required_if(NO,
                             field='partner_present',
                             field_required='disclosure_to_partner')

        self.not_required_if(NO,
                             field='partner_present',
                             field_required='discussion_with_partner')

        self.required_if(NO,
                         field='living_with_partner',
                         field_required='why_not_living_with_partner')

        self.required_if(YES,
                         field='partner_present',
                         field_required='is_partner_the_father')

        self.required_if(YES,
                         field='ever_separated',
                         field_required='times_separated')

        self.required_if(YES,
                         field='contact_info',
                         field_required='partner_cell')
        is_partner_the_father = self.cleaned_data.get('is_partner_the_father', None)
        biological_father_alive = self.cleaned_data.get('biological_father_alive', None)

        if is_partner_the_father and biological_father_alive:
            if is_partner_the_father == YES and biological_father_alive != YES:
                raise ValidationError({
                    'biological_father_alive': 'Currently living with the father, check question 5 '
                })

        self.validate_father_involvement()

        super().clean()

    def validate_required_fields(self):
        required_fields = [
            'is_partner_the_father',
            'duration_with_partner',
            'partner_age_in_years',
            'living_with_partner',
            'partners_support',
            'ever_separated',
            'separation_consideration',
            'leave_after_fight',
            'relationship_progression',
            'confide_in_partner',
            'relationship_regret',
            'quarrel_frequency',
            'bothering_partner',
            'kissing_partner',
            'engage_in_interests',
            'happiness_in_relationship',
            'future_relationship',
        ]

        for field in required_fields:
            self.required_if(YES, field='partner_present',
                             field_required=field)

    def validate_father_involvement(self):

        required_fields = [

            'father_child_contact',
            'fathers_financial_support',
        ]

        for field in required_fields:
            self.not_required_if(
                NO, PNTA, field='biological_father_alive', field_required=field)

    def validate_positive_mother(self):
        # Checker when running tests so it does require addition modules
        if settings.APP_NAME != 'flourish_form_validations':
            partner_present = self.cleaned_data.get('partner_present', None)
            maternal_visit = self.cleaned_data.get('maternal_visit')
            helper = MaternalStatusHelper(
                maternal_visit, maternal_visit.subject_identifier)

            fields = ['disclosure_to_partner',
                      'discussion_with_partner', 'disclose_status']

            # for field in fields:

            self.required_if_true(helper.hiv_status == POS,
                                  field_required='disclosure_to_partner')

            self.required_if(YES, field='disclosure_to_partner',
                             field_required='discussion_with_partner')
            self.required_if(NO, field='disclosure_to_partner',
                             field_required='disclose_status')
