from django.apps import AppConfig as DjangoApponfig
from edc_odk.apps import AppConfig as BaseEdcOdkAppConfig
from edc_senaite_interface.apps import AppConfig as BaseEdcSenaiteInterfaceAppConfig
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


class EdcSenaiteInterfaceAppConfig(BaseEdcSenaiteInterfaceAppConfig):
    host = "https://lims-test.bhp.org.bw"
    client = "Flourish"
    courier = ""
    sample_type_match = {'viral_load': 'Whole Blood EDTA',
                         'cd4': 'Whole Blood EDTA',
                         'hematology': 'Whole Blood EDTA',
                         'complete_blood_count': 'Whole Blood EDTA',
                         'dna_pcr': 'Dry Blood Spot',
                         'stool_sample': 'Stool'}
    container_type_match = {'viral_load': 'EDTA tube',
                            'cd4': 'EDTA tube',
                            'hematology': 'EDTA tube',
                            'complete_blood_count': 'EDTA Tube',
                            'dna_pcr': 'Filter paper',
                            'stool_sample': 'Cryogenic Vial'}
    template_match = {'viral_load': 'HIV RNA PCR',
                      'cd4': 'CD4/CD8',
                      'hematology': 'CBC',
                      'complete_blood_count': 'CBC',
                      'dna_pcr': 'HIV DNA PCR',
                      'stool_sample': 'Stool Storage'}
