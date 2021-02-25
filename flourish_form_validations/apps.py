from django.apps import AppConfig as DjangoApponfig
from edc_visit_tracking.apps import (
    AppConfig as BaseEdcVisitTrackingAppConfig)


class AppConfig(DjangoApponfig):
    name = 'flourish_form_validations'
    verbose_name = 'Flourish Form Validations'


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    visit_models = {
        'flourish_caregiver': (
            'maternal_visit', 'flourish_caregiver.maternalvisit'),
        'flourish_child': (
            'child_visit', 'flourish_child.childvisit')}
