from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from edc_form_validators.form_validator import FormValidator
from .crf_form_validator import FormValidatorMixin


class UltrasoundFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):

        cleaned_data = self.cleaned_data
        self.subject_identifier = cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        fields = [
            'bpd', 'hc', 'ac', 'fl', 'amniotic_fluid_volume',
            'ga_by_lmp', 'ga_by_ultrasound_wks', 'ga_by_ultrasound_days', 'est_fetal_weight',
            'est_edd_ultrasound', 'edd_confirmed', 'ga_confirmed', 'ga_confrimation_method',
        ]
        for field in fields:
            self.not_required_if(
                '0',
                field='number_of_gestations',
                field_required=field,
            )

        if cleaned_data.get('est_edd_ultrasound') and (
                cleaned_data.get('est_edd_ultrasound') >
                cleaned_data.get('report_datetime').date() +
                relativedelta(weeks=40)):
            msg = {'est_edd_ultrasound': 'Estimated edd by ultrasound cannot be'
                                         ' greater than 40 weeks from today'}
            self._errors.update(msg)
            raise ValidationError(msg)

        if cleaned_data.get('ga_by_ultrasound_wks') and (
                cleaned_data.get('ga_by_ultrasound_wks') > 40):
            msg = {'ga_by_ultrasound_wks':
                       ('GA by ultrasound cannot be greater than 40 weeks.')}

            self._errors.update(msg)
            raise ValidationError(msg)

        if cleaned_data.get('ga_by_ultrasound_days') and (
                cleaned_data.get('ga_by_ultrasound_days') > 7):
            msg = {'ga_by_ultrasound_days':
                       ('GA by ultrasound days cannot be greater than 7 days.')}

            self._errors.update(msg)
            raise ValidationError(msg)

        ga_by_ultrasound = cleaned_data.get('ga_by_ultrasound_wks')
        est_edd_ultrasound = cleaned_data.get('est_edd_ultrasound')
        report_datetime = cleaned_data.get('report_datetime')
        self.validate_edd_report_datetime()

        if cleaned_data.get('ga_by_ultrasound_wks'):

            est_conceive_date = (report_datetime.date() -
                                 relativedelta(weeks=ga_by_ultrasound))
            if (est_edd_ultrasound):
                weeks_between = (
                                    (est_edd_ultrasound - est_conceive_date).days) / 7

                if (weeks_between + 1) > ga_by_ultrasound:

                    if (int(weeks_between) + 1) not in range(39, 42):
                        msg = {'est_edd_ultrasound':
                                   f'Estimated edd by ultrasound {est_edd_ultrasound} '
                                   'should match GA by ultrasound'}
                        self._errors.update(msg)
                        raise ValidationError(msg)

    def validate_edd_report_datetime(self):
        if (self.cleaned_data.get('est_edd_ultrasound') and
                self.cleaned_data.get('est_edd_ultrasound') <
                self.cleaned_data.get('maternal_visit').report_datetime.date()):
            raise ValidationError('Expected a future date')
