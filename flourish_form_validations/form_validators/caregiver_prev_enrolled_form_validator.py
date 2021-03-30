from django.apps import apps as django_apps

from edc_constants.constants import YES, NO
from edc_form_validators.form_validator import FormValidator


class CaregiverPrevEnrolledFormValidator(FormValidator):

    maternal_dataset_model = 'flourish_caregiver.maternaldataset'

    subject_consent_model = 'flourish_caregiver.subjectconsent'

    @property
    def maternal_dataset_model_cls(self):
        return django_apps.get_model(self.maternal_dataset_model)

    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    def clean(self):

        fields_required = ['sex', 'relation_to_child', ]
        for field_required in fields_required:
            self.required_if(
                NO,
                field='maternal_prev_enroll',
                field_required=field_required)

        self.validate_other_specify(field='relation_to_child')
        self.validate_caregiver_previously_enrolled(cleaned_data=self.cleaned_data)

    def validate_caregiver_previously_enrolled(self, cleaned_data=None):
        maternal_prev_enroll = cleaned_data.get('maternal_prev_enroll')
        if (maternal_prev_enroll == YES and
                self.maternal_dataset_obj.mom_hivstatus ==
                'HIV-uninfected'):
            fields_required = ['current_hiv_status', 'last_test_date', ]
            for field_required in fields_required:
                self.required_if(
                    YES,
                    field='maternal_prev_enroll',
                    field_required=field_required)

            self.required_if(
                YES,
                field='last_test_date',
                field_required='test_date')

            self.required_if(
                YES,
                field='last_test_date',
                field_required='is_date_estimated')


    @property
    def maternal_dataset_obj(self):
        try:
            maternal_dataset = self.maternal_dataset_model_cls.objects.get(
                screening_identifier=
                self.subject_consent_obj.screening_identifier)
        except self.maternal_dataset_model_cls.DoesNotExist:
            return None
        else:
            return maternal_dataset

    @property
    def subject_consent_obj(self):
        try:
            subject_consent = self.subject_consent_model_cls.objects.get(
                subject_identifier=self.cleaned_data.get(
                    'subject_identifier'))
        except self.subject_consent_model_cls.DoesNotExist:
            return None
        else:
            return subject_consent
