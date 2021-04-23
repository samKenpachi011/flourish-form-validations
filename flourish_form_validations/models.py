from django.conf import settings

if settings.APP_NAME == 'flourish_form_validations':
    from .tests import models
