from django import forms


class CRFFormValidator:

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
        super().clean()

    def validate_against_visit_datetime(self, report_datetime):
        if (report_datetime and report_datetime <
                self.cleaned_data.get('maternal_visit').report_datetime):
            raise forms.ValidationError(
                "Report datetime cannot be before visit datetime.")
