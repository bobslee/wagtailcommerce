"""
Contains application edit handlers.
"""
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.admin.utils import quote

from wagtail.wagtailadmin.edit_handlers import EditHandler, ObjectList, get_edit_handler

def add_panel_to_edit_handler(model, panel_cls, heading, index=None):
    """
    Adds specified panel class to model class.

    :param model: the model class.
    :param panel_cls: the panel class.
    :param heading: the panel heading.
    :param index: the index position to insert at.
    """
    edit_handler = model.get_edit_handler()
    
    panel_instance  = ObjectList(
        [panel_cls(),],
        heading = heading
    ).bind_to_model(model)

    if index:
        edit_handler.children.insert(index, panel_instance)
    else:
        edit_handler.children.append(panel_instance)

class BaseProductPanel(EditHandler):
    template = 'commerce_wagtail/edit_handlers/product.html'

    def __init__(self, instance=None, form=None):
        super(BaseProductPanel, self).__init__(instance, form)
        self.instance = instance

    def render(self):
        context = {
            'self': self,
        }

        # TODO and if user has_permission for (django)admin product_change
        if getattr(self.instance, 'product', False) != False:
            admin_url = reverse('admin:commerce_wagtail_product_change',
                          args=(quote(self.instance.product.pk),),
                          current_app='commerce_wagtail',
            )
            context['admin_url'] = admin_url
            context['product'] = self.instance.product

        return mark_safe(
            render_to_string(self.template, context)
        )

class ProductPanel(object):
    @staticmethod
    def bind_to_model(model):
        base = {'model': model}
        return type(str('_ProductPanel'), (BaseProductPanel,), base)
