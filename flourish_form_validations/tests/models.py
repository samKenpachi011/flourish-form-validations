from django.db import models
from django.db.models.deletion import PROTECT
from django_crypto_fields.fields import FirstnameField, LastnameField
from edc_base.model_mixins import BaseUuidModel, ListModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import GENDER, YES_NO, YES_NO_NA
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


class ListModel(ListModelMixin, BaseUuidModel):
    pass


class CaregiverLocator(BaseUuidModel):
    subject_identifier = models.CharField(max_length=50)

    screening_identifier = models.CharField(max_length=50)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    may_call = models.CharField(
        max_length=3)

    may_visit_home = models.CharField(
        max_length=3)


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


class SubjectScreening(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):
    screening_identifier = models.CharField(max_length=50)

    mother_alive = models.CharField(max_length=50)


class MaternalDelivery(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):
    subject_identifier = models.CharField(max_length=25)


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

    evidence_hiv_status = models.CharField(max_length=15)

    week32_result = models.CharField(max_length=15)

    rapid_test_done = models.CharField(max_length=15)

    rapid_test_result = models.CharField(max_length=15)

    rapid_test_date = models.DateField(
        null=True,
        blank=True)


class Appointment(BaseUuidModel):
    subject_identifier = models.CharField(max_length=25)

    appt_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25)


class MaternalVisit(BaseUuidModel):
    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)

    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField(default=0)

    report_datetime = models.DateTimeField(
        default=get_utcnow)

    def save(self, *args, **kwargs):
        self.visit_code = self.appointment.visit_code
        self.subject_identifier = self.appointment.subject_identifier
        super().save(*args, **kwargs)


class MaternalArvDuringPreg(models.Model):
    took_arv = models.CharField(
        choices=YES_NO,
        max_length=10)
    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)


class MaternalArv(models.Model):
    maternal_arv_durg_preg = models.ForeignKey(MaternalArvDuringPreg, on_delete=PROTECT)

    arv_code = models.CharField(
        verbose_name="ARV code",
        max_length=35)

    start_date = models.DateField(
        null=True,
        blank=False)

    stop_date = models.DateField(
        null=True,
        blank=True)


class ArvsPrePregnancy(models.Model):
    maternal_visit = models.ForeignKey(MaternalVisit, on_delete=PROTECT)

    preg_on_art = models.CharField(max_length=25, choices=YES_NO_NA)

    art_start_date = models.DateField(
        blank=True,
        null=True)


class RegisteredSubject(BaseUuidModel):
    subject_identifier = models.CharField(max_length=25)

    first_name = FirstnameField(null=True)

    last_name = LastnameField(verbose_name="Last name")

    gender = models.CharField(max_length=1, choices=GENDER)


class UltraSound(models.Model):
    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)

    ga_confirmed = models.IntegerField()


class MaternalDataset(BaseUuidModel):
    screening_identifier = models.CharField(max_length=36)

    study_child_identifier = models.CharField(max_length=36)

    study_maternal_identifier = models.CharField(max_length=36)

    delivdt = models.DateField()


class ChildDataset(BaseUuidModel):
    study_child_identifier = models.CharField(max_length=36)

    dob = models.DateField(
        null=True,
        blank=True)

    infant_sex = models.CharField(max_length=7)

