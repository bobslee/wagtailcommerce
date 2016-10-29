from django import forms
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.forms import WagtailAdminPageForm

class AdminProductPageForm(WagtailAdminPageForm):
    product_title = forms.CharField(
        required=False,
        label=_('Title'),
    )
    product_description = forms.CharField(
        required=False,
        label=_('Description'),
        help_text=_('For admin/backoffice purposes only.')
    )

    def __init__(self, *args, **kwargs):
        super(AdminProductPageForm, self).__init__(*args, **kwargs)

        # TODO
        # - Disable and colorize (to contrast the light-grey)
        # - Set/copy help_text from the product if any?
        self.fields['product_title'].initial = self.instance.product.title
        self.fields['product_description'].initial = self.instance.product.description
