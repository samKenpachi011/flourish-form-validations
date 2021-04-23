from django.apps import apps as django_apps


class ConsentsFormValidatorMixin:

    maternal_dataset_model = 'flourish_caregiver.maternaldataset'

    child_dataset_model = 'flourish_child.childdataset'

    @property
    def maternal_dataset_cls(self):
        return django_apps.get_model(self.maternal_dataset_model)

    @property
    def child_dataset_cls(self):
        return django_apps.get_model(self.child_dataset_model)

    @property
    def maternal_dataset(self):
        try:
            maternal_dataset = self.maternal_dataset_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except self.maternal_dataset_cls.DoesNotExist:
            return None
        else:
            return maternal_dataset

    def child_dataset(self, study_maternal_identifier=None):
        try:
            child_dataset = self.child_dataset_cls.objects.get(
                study_maternal_identifier=study_maternal_identifier)
        except self.child_dataset_cls.DoesNotExist:
            return None
        else:
            return child_dataset
