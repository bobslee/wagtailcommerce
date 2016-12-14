from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.forms.models import ModelMultipleChoiceField
from django.utils.html import escape
from django.utils.safestring import mark_safe

class CharNullableField(models.CharField):
    description = "CharField that stores NULL but returns ''"

    def to_python(self, value):
        if isinstance(value, models.CharField):
            return value
        return value or ''
    
    def get_prep_value(self, value):
        return value

class TreeLabelFromInstanceMixin(object):
    error_message = ''

    def label_from_instance(self, obj):
        prefix = ''
        bullet = '- '
        try:
            if obj.depth > 1:
                prefix = '&nbsp;&nbsp;' * (obj.depth - 1)
                bullet = ' - ' * (obj.depth)
                name = ' / '.join(map(str,obj.get_ancestors())) + " / %s" % obj
            else:
                name = obj

            label = "{prefix}{bullet}{name}".format(prefix=prefix, name=escape(name),bullet=bullet)
            return mark_safe(label)
        except AttributeError:
            raise ImproperlyConfigured(self.error_message)

class TreeMultipleChoiceField(TreeLabelFromInstanceMixin,
                                  ModelMultipleChoiceField):
    error_message = (
        "TreeMultipleChoiceField should only be used for M2M ")
    
class TreeManyToManyField(ManyToManyField):
    """
    Simply a normal ManyToManyField, but with a custom *default* form field
    which hierarchically displays the set of choices.
    """

    # This is necessary for Django 1.7.4+
    def get_internal_type(self):
        return 'ManyToManyField'

    def formfield(self, form_class=TreeMultipleChoiceField,
                  choices_form_class=None, **kwargs):
        kwargs["form_class"] = form_class
        kwargs["choices_form_class"] = choices_form_class
        return super(TreeManyToManyField, self).formfield(**kwargs)
