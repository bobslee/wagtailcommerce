from __future__ import absolute_import, unicode_literals

import json

from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.widgets import AdminPageChooser

class AdminPageChooserOrCreate(AdminPageChooser):
    create_text = _('Create a page')

    def render_html(self, name, value, attrs):
        model_class = self._get_lowest_common_page_class()

        instance, value = self.get_instance_and_id(model_class, value)

        original_field_html = super(AdminPageChooser, self).render_html(name, value, attrs)
        return render_to_string("wagtailcommerce/widgets/page_chooser_or_create.html", {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': value,
            'instance': instance,
        })
    
    def render_js_init(self, id_, name, value):
        js_super = super(AdminPageChooserOrCreate, self).render_js_init(id_, name, value)
        js = "createPageChooserOrCreate({0});".format(json.dumps(id_))

        return js_super + js
