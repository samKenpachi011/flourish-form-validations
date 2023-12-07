from django.apps import AppConfig as DjangoApponfig
from edc_appointment.constants import COMPLETE_APPT
from edc_odk.apps import AppConfig as BaseEdcOdkAppConfig
from edc_timepoint import Timepoint, TimepointCollection
from edc_timepoint.apps import AppConfig as BaseEdcTimepointAppConfig
from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig


class AppConfig(DjangoApponfig):
    name = 'flourish_form_validations'
    verbose_name = 'Flourish Form Validations'


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    visit_models = {
        'flourish_caregiver': (
            'maternal_visit', 'flourish_caregiver.maternalvisit'),
        'flourish_child': (
            'child_visit', 'flourish_child.childvisit'),
        'pre_flourish': (
            'maternal_visit', 'pre_flourish.preflourishcaregivervisit'), }


class EdcOdkAppConfig(BaseEdcOdkAppConfig):
    clinician_notes_form_ids = {
        'flourish_child': 'child_cliniciannotes_v1.0',
        'flourish_caregiver': 'caregiver_cliniciannotes_v1.0'}

    clinician_notes_models = {
        'flourish_child': 'childcliniciannotes',
        'flourish_caregiver': 'cliniciannotes'}


class EdcTimepointAppConfig(BaseEdcTimepointAppConfig):
    timepoints = TimepointCollection(
        timepoints=[
            Timepoint(
                model='edc_appointment.appointment',
                datetime_field='appt_datetime',
                status_field='appt_status',
                closed_status=COMPLETE_APPT),
            Timepoint(
                model='edc_appointment.historicalappointment',
                datetime_field='appt_datetime',
                status_field='appt_status',
                closed_status=COMPLETE_APPT),
        ])
