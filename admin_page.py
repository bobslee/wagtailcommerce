from django import forms
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.forms import WagtailAdminPageForm

class AdminProductPageForm(WagtailAdminPageForm):

    def __init__(self, *args, **kwargs):
        super(AdminProductPageForm, self).__init__(*args, **kwargs)

        self.fields['title'].label = "%s - (%s)" % (self.fields['title'].label, _('readonly'))
        self.fields['title'].disabled = True
        self.fields['title'].help_text = _('The title can be set/overriden by the ProductTitleBlock in the body.')
