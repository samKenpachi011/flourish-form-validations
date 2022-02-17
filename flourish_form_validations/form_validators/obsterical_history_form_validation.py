from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators.form_validator import FormValidator
from .crf_form_validator import CRFFormValidator


class ObstericalHistoryFormValidator(CRFFormValidator, FormValidator):
    ultrasound_model = 'flourish_caregiver.ultrasound'

    @property
    def maternal_ultrasound_cls(self):
        return django_apps.get_model(self.ultrasound_model)

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.validate_ultrasound(cleaned_data=self.cleaned_data)
        self.validate_prev_pregnancies(cleaned_data=self.cleaned_data)
        self.validate_children_delivery(cleaned_data=self.cleaned_data)

    @property
    def ultrasound_ga_confirmed(self):

        maternal_visit = self.cleaned_data.get('maternal_visit')
        subject_identifier = maternal_visit.subject_identifier

        try:
            ultrasound = self.maternal_ultrasound_cls.objects.get(
                maternal_visit__subject_identifier=subject_identifier,
                maternal_visit=maternal_visit)

        except self.maternal_ultrasound_cls.DoesNotExist:
            message = 'Please complete ultrasound form first.'
            raise ValidationError(message)
        else:
            return ultrasound.ga_confirmed

    def validate_ultrasound(self, cleaned_data=None):

        prev_pregnancies = cleaned_data.get('prev_pregnancies')

        if prev_pregnancies == 1:

            if self.ultrasound_ga_confirmed > 24:

                    fields = ['pregs_24wks_or_more',
                              'lost_before_24wks', 'lost_after_24wks']

                    for field in fields:
                        if (field in cleaned_data and
                                cleaned_data.get(field) != 0):
                            message = {field: 'You indicated previous pregnancies were '
                                       f'{prev_pregnancies}, {field} should be zero as '
                                       'the current pregnancy is more than 24 weeks.'}
                            self._errors.update(message)
                            raise ValidationError(message)

            else:
                fields = ['prev_pregnancies', 'pregs_24wks_or_more']
                for field in fields:
                    if cleaned_data.get(field) == 0:
                        raise ValidationError(
                            {field: 'You indicated previous pregnancies were '
                             f'{prev_pregnancies}, {field} cannot be zero as '
                             'the current pregnancy is less than 24 weeks.'})

    def validate_children_delivery(self, cleaned_data=None):
        if None not in [cleaned_data.get('children_deliv_before_37wks'),
                        cleaned_data.get('children_deliv_aftr_37wks'),
                        cleaned_data.get('lost_before_24wks'),
                        cleaned_data.get('lost_after_24wks')]:

            sum_deliv_37_wks = \
                (cleaned_data.get('children_deliv_before_37wks') +
                 cleaned_data.get('children_deliv_aftr_37wks'))
            sum_lost_24_wks = (cleaned_data.get('lost_before_24wks') +
                               cleaned_data.get('lost_after_24wks'))

            children_died_b4_5yrs = cleaned_data.get('children_died_b4_5yrs') or 0
            live_children = cleaned_data.get('live_children') or 0

            offset = 0

            if self.ultrasound_ga_confirmed > 24:
                offset = 1

            if (cleaned_data.get('prev_pregnancies') and
                sum_deliv_37_wks != ((cleaned_data.get('prev_pregnancies') - offset)
                                     -sum_lost_24_wks)):
                raise ValidationError('The sum of Q9 and Q10 must be equal to '
                                      f'(Q3 -{offset}) - (Q5 + Q6). Please correct.')

            if (live_children > (sum_deliv_37_wks - children_died_b4_5yrs)):

                raise ValidationError(
                    'Living children cannot be less than pregnancies delivered(Q9 + Q10) '
                    'and childrenn lost. Please correct.')

    def validate_prev_pregnancies(self, cleaned_data=None):

        pregs_24wks_or_more = cleaned_data.get('pregs_24wks_or_more') or 0
        lost_before_24wks = cleaned_data.get('lost_before_24wks') or 0
        lost_after_24wks = cleaned_data.get('lost_after_24wks') or 0

        sum_pregs = pregs_24wks_or_more + lost_before_24wks

        previous_pregs = cleaned_data.get('prev_pregnancies')

        if (sum_pregs != previous_pregs):
            raise ValidationError('Total pregnancies should be '
                                  'equal to sum of pregnancies '
                                  'lost and current')

        if self.ultrasound_ga_confirmed > 24 and pregs_24wks_or_more < 1:
            message = {'pregs_24wks_or_more':
                       'Pregnancies more than 24 weeks should be '
                       'more than 1 including the current pregnancy'}
            self._errors.update(message)
            raise ValidationError(message)

        if lost_after_24wks > pregs_24wks_or_more:
            message = {'lost_after_24wks':
                       'Pregnancies lost after 24 weeks cannot be '
                       'more than pregnancies atleast 24 weeks'}
            self._errors.update(message)
            raise ValidationError(message)
