from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils import translation

LANGUAGES = (
  ('de', _('German')),
  ('en', _('English')),
)

def home(request):
    return render(request, 'welcome_page.html', {'LANGUAGES':LANGUAGES,})