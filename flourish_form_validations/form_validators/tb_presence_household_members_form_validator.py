from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin


class TbPresenceHouseholdMembersFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.required_if(
            YES,
            field='tb_diagnosed',
            field_required='tb_ind_rel')

        self.validate_other_specify(
            field='tb_ind_rel',
            other_specify_field='tb_ind_other')

        self.required_if(
            YES,
            field='tb_in_house',
            field_required='cough_ind_rel')

        self.validate_other_specify(
            field='cough_ind_rel',
            other_specify_field='cough_ind_other')

        self.required_if(
            YES,
            field='fever_signs',
            field_required='fever_ind_rel')

        self.validate_other_specify(
            field='fever_ind_rel',
            other_specify_field='fever_ind_other')

        self.required_if(
            YES,
            field='night_sweats',
            field_required='sweat_ind_rel')

        self.validate_other_specify(
            field='sweat_ind_rel',
            other_specify_field='sweat_ind_other')

        self.required_if(
            YES,
            field='weight_loss',
            field_required='weight_ind_rel')

        self.validate_other_specify(
            field='weight_ind_rel',
            other_specify_field='weight_ind_other')
