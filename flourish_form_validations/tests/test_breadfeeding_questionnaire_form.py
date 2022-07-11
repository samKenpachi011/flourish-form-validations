from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS, NEG
from ..form_validators import BreastFeedingQuestionnaireFormValidator
from flourish_form_validations.tests.test_model_mixin import TestModeMixin
from .models import (FlourishConsentVersion, SubjectConsent,
                     Appointment, MaternalVisit, ListModel)
from dateutil.relativedelta import relativedelta
from edc_constants.constants import OTHER


@tag('breastfeeding')
class TestBreastFeedingQuestionnaireForm(TestModeMixin, TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(BreastFeedingQuestionnaireFormValidator, *args, **kwargs)

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

    def test_during_preg_influencers_specify_required(self):
        """ Assert that the During Pregnancy Influencers specify raises an error if 
            during pregnancy influencers includes other, but not specified.
        """

        ListModel.objects.create(short_name=OTHER)
        self.options.update(
            during_preg_influencers=ListModel.objects.all(),
            during_preg_influencers_other=None)
        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('during_preg_influencers_other', form_validator._errors)

    def test_during_preg_influencers_specify_valid(self):
        """ Tests if During Pregnancy Influencers includes other and
            other is specified, cleaned data validates or fails the
            tests if the Validation Error is raised unexpectedly.
        """

        ListModel.objects.create(short_name=OTHER)
        self.options.update(
            during_preg_influencers=ListModel.objects.all(),
            during_preg_influencers_other='blah')

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_after_delivery_influencers_specify_required(self):
        """ Assert that the After Pregnancy Influencers specify raises an error if 
            after pregnancy influencers includes other, but not specified.
        """

        ListModel.objects.create(short_name=OTHER)
        self.options.update(
            after_delivery_influencers=ListModel.objects.all(),
            after_delivery_influencers_other=None)

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('after_delivery_influencers_other', form_validator._errors)

    def test_after_delivery_influencers_specify_valid(self):
        """ Tests if After Pregnancy Influencers includes other and
            other is specified, cleaned data validates or fails the
            tests if the Validation Error is raised unexpectedly.
        """

        ListModel.objects.create(short_name=OTHER)
        self.options.update(
            after_delivery_influencers=ListModel.objects.all(),
            after_delivery_influencers_other='blah')

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_infant_feeding_reasons_specify_required(self):
        """ Assert that the Infant Feeding specify raises an error if 
            infant feeding includes other, but not specified.
        """

        ListModel.objects.create(short_name=OTHER)
        self.options.update(
            infant_feeding_reasons=ListModel.objects.all(),
            infant_feeding_other=None)

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('infant_feeding_other', form_validator._errors)

    def test_infant_feeding_reasons_specify_valid(self):
        """ Tests if Infant Feeding includes other and
            other is specified, cleaned data validates or fails the
            tests if the Validation Error is raised unexpectedly.
        """

        ListModel.objects.create(short_name=OTHER)
        self.options.update(
            six_months_feeding=YES,
            infant_feeding_reasons=ListModel.objects.all(),
            infant_feeding_other='blah')

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hiv_status_aware_required(self):

        self.options.update(
            feeding_hiv_status=NO,
            hiv_status_aware=None)

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hiv_status_aware', form_validator._errors)

    def test_hiv_status_aware_valid(self):

        self.options.update(
            feeding_hiv_status=NO,
            hiv_status_aware='blah')

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_on_hiv_status_aware_required(self):

        self.options.update(
            feeding_hiv_status=NO,
            on_hiv_status_aware=None)

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('on_hiv_status_aware', form_validator._errors)

    def test_on_hiv_status_aware_valid(self):

        self.options.update(
            feeding_hiv_status=NO,
            on_hiv_status_aware='blah')

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hiv_status_known_by_required(self):

        self.options.update(
            hiv_status_during_preg=POS,
            received_training=None,
            training_outcome='blah blah',
            feeding_advice='blah blah',
            hiv_status_known_by='blah blah')

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hiv_status_known_by_valid(self):

        self.options.update(
            hiv_status_during_preg=NEG,
            received_training='blah blah',
            father_knew_hiv_status='blah blah',
            delivery_advice_on_viralload='blah blah',
            after_delivery_advice_vl_results='blah blah',
            after_delivery_advice_on_viralload='blah blah',
            delivery_advice_vl_results='blah blah',
            breastfeeding_duration='blah blah',)

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_influenced_during_preg_required(self):

        ListModel.objects.create(short_name=YES)
        self.options.update(
            during_preg_influencers=ListModel.objects.all(),
            influenced_during_preg=None)

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('influenced_during_preg', form_validator._errors)

    def test_influenced_during_preg_valid(self):

        ListModel.objects.create(short_name=YES)
        self.options.update(
            during_preg_influencers=ListModel.objects.all(),
            influenced_during_preg='blah')

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_infant_feeding_reasons_required(self):

        self.options.update(
            six_months_feeding=YES,
            infant_feeding_reasons=None)

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('infant_feeding_reasons', form_validator._errors)

    def test_infant_feeding_reasons_valid(self):

        ListModel.objects.create(name='test')
        self.options.update(
            six_months_feeding=YES,
            infant_feeding_reasons=ListModel.objects.all())

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_infant_feeding_reasons_unsure_required(self):

        self.options.update(
            six_months_feeding=YES,
            infant_feeding_reasons=None)

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('infant_feeding_reasons', form_validator._errors)

    def test_infant_feeding_reasons_unsure_valid(self):

        ListModel.objects.create(name='test')
        self.options.update(
            six_months_feeding=YES,
            infant_feeding_reasons=ListModel.objects.all())

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hiv_status_during_preg_applicable(self):
        self.options.update(
            use_medicines='blah',
            received_training='blah',
            training_outcome='blah',
            feeding_advice='blah',
            hiv_status_during_preg=NEG
        )

        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('use_medicines', form_validator._errors)

    def test_six_months_feeding_req(self):
        ListModel.objects.create(name='test')
        self.options.update(
            six_months_feeding=NO,
            infant_feeding_reasons=ListModel.objects.all(),
        )
        form_validator = BreastFeedingQuestionnaireFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('infant_feeding_reasons', form_validator._errors)
