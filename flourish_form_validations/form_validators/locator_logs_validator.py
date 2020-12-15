from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator


class LocatorLogEntryFormValidator(FormValidator):

    @property
    def locator_model_cls(self):
        return django_apps.get_model('flourish_caregiver.caregiverlocator')

    def clean(self):
        super().clean()

        self.required_if(
            'not_found',
            field='log_status',
            field_required='comment',
            required_msg='Please provide a short brief reason')

        log_status = self.cleaned_data.get('log_status')

        if log_status == 'not_found':
            self.check_locator_obj_exists()

    def check_locator_obj_exists(self):
        locator_log = self.cleaned_data.get('locator_log')
        study_maternal_identifier = locator_log.maternal_dataset.study_maternal_identifier
        try:
            self.locator_model_cls.objects.get(
                study_maternal_identifier=study_maternal_identifier)
        except self.locator_model_cls.DoesNotExist:
            pass
        else:
            msg = {'__all__':
                   'Can not change status of log entry to not found, locator already exists.'}
            self._errors.update(msg)
            raise ValidationError(msg)
