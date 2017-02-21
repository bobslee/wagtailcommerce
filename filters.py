from django.contrib.admin.filters import SimpleListFilter, FieldListFilter
from django.utils.translation import ugettext_lazy as _

class ForeignKeyIsNullFieldListFilter(FieldListFilter):
    template = 'wagtailcommerce/boolean_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = "%s__isnull" % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg)
        super(ForeignKeyIsNullFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)

        if hasattr(field, 'verbose_name'):
            self.lookup_title = field.verbose_name
        self.title = self.lookup_title

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def choices(self, changelist):
        for lookup, title in (
                (None, _('All')),
                ('0', _('Yes')),
                ('1', _('No'))):
            yield {
                'selected': self.lookup_val == lookup,
                'query_string': changelist.get_query_string(
                    {self.lookup_kwarg: lookup}),
                'display': title,
            }
