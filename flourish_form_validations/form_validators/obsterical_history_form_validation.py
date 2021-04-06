from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators.form_validator import FormValidator

from .crf_form_validator import CRFFormValidator


class ObstericalHistoryFormValidator(CRFFormValidator, FormValidator):
    ultrasound_model = 'flourish_caregiver.ultrasound'

    @property
    def ultrasound_model_cls(self):
        return django_apps.get_model(self.ultrasound_model)

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.validate_prev_pregnancies(cleaned_data=self.cleaned_data)
        self.validate_children_deliv(cleaned_data=self.cleaned_data)

    def validate_children_deliv(self, cleaned_data=None):
        if None not in [cleaned_data.get('children_deliv_before_37wks'),
                        cleaned_data.get('children_deliv_aftr_37wks'),
                        cleaned_data.get('lost_before_24wks'),
                        cleaned_data.get('lost_after_24wks')]:

            sum_deliv_37_wks = \
                (cleaned_data.get('children_deliv_before_37wks') +
                 cleaned_data.get('children_deliv_aftr_37wks'))
            sum_lost_24_wks = (cleaned_data.get('lost_before_24wks') +
                               cleaned_data.get('lost_after_24wks'))
            total_children = cleaned_data.get('prev_pregnancies') - sum_lost_24_wks
            if (cleaned_data.get('prev_pregnancies') and sum_deliv_37_wks != total_children):
                raise ValidationError('The sum of Q9 and Q10 must be equal to  '
                                      '(Q3 - Q5 + Q6). Please correct.')

    def validate_prev_pregnancies(self, cleaned_data=None):

        if (('prev_pregnancies' in cleaned_data and
                cleaned_data.get('prev_pregnancies') > 1)):
            if (cleaned_data.get('pregs_24wks_or_more') and
                    cleaned_data.get('lost_before_24wks')):
                sum_pregs = (cleaned_data.get('pregs_24wks_or_more') +
                             (cleaned_data.get('lost_before_24wks')))

                previous_pregs = (cleaned_data.get('prev_pregnancies'))

                if (sum_pregs != previous_pregs):
                    raise ValidationError(
                        'Total pregnancies should be equal to sum of pregancies'
                        ' lost and current')

                if (cleaned_data.get('pregs_24wks_or_more') <
                        cleaned_data.get('lost_after_24wks')):
                    message = {'pregs_24wks_or_more':
                               'Sum of pregnancies more than 24 weeks should NOT be'
                               ' less than those lost'}
                    self._errors.update(message)
                    raise ValidationError(message)
