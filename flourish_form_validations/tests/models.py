from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


class SubjectConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    screening_identifier = models.CharField(max_length=50)

    gender = models.CharField(max_length=25)

    is_literate = models.CharField(max_length=25,
                                   blank=True,
                                   null=True)

    witness_name = models.CharField(max_length=25,
                                    blank=True,
                                    null=True)

    dob = models.DateField()

    consent_datetime = models.DateTimeField()

    version = models.CharField(
        max_length=10,
        editable=False)


class AntenatalEnrollment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=50)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    last_period_date = models.DateField(
        null=True,
        blank=True)

    current_hiv_status = models.CharField(max_length=15)

    week32_test = models.CharField(max_length=15)

    week32_test_date = models.DateField(
        null=True,
        blank=True)

    enrollment_hiv_status = models.CharField(max_length=15)

    week32_result = models.CharField(max_length=15)

    rapid_test_done = models.CharField(max_length=15)

    rapid_test_result = models.CharField(max_length=15)

    rapid_test_date = models.DateField(
        null=True,
        blank=True)


class SubjectScreening(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    screening_identifier = models.CharField(
        max_length=36,
        unique=True,
        editable=False)

    has_omang = models.CharField(max_length=3)

    age_in_years = age_in_years = models.IntegerField()
