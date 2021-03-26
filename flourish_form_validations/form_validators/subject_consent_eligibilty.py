from edc_constants.constants import NO


class SubjectConsentEligibility:

    def subject_eligible(self, cleaned_data):
        if (cleaned_data.get('remain_in_study') == NO or
            cleaned_data.get('hiv_testing') == NO or
            cleaned_data.get('breastfeed_intent') == NO or
            cleaned_data.get('consent_reviewed') == NO or
            cleaned_data.get('study_questions') == NO or
            cleaned_data.get('assessment_score') == NO or
            cleaned_data.get('consent_signature') == NO or
                cleaned_data.get('consent_copy') == NO):
                return False
        return True
