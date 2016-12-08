from collections import OrderedDict

from django.contrib.admin.utils import quote
from django.shortcuts import render
from django.urls import reverse

from wagtail.wagtailcore.query import TreeQuerySet

# TODO still fragile!
# Slightly copied from: django.contrib.admin.views.ChangeList
# Check properties like is_pop etc.
class IndexTree(object):
    def __init__(self, request, model, model_admin):
        self.model = model
        self.model_admin = model_admin
        self.list_display = model_admin.list_display
        self.opts = model._meta
        self.lookup_opts = self.opts
        self.params = {}
        self.formset = None

        self.list_display_links = []
        self.to_field = None
        self.is_popup = None        

        self.root_queryset = self.get_queryset(request)
        self.queryset = self.get_queryset(request)
        
        self.get_results()

    def get_ordering_field_columns(self):
        ordering_fields = OrderedDict()
        return ordering_fields

    def get_query_string(self, new_params=None, remove=None):
        pass

    def get_queryset(self, request):
        return TreeQuerySet(self.model).order_by('path')

    def get_results(self):
        self.result_list = self.queryset._clone()

    def url_for_result(self, result):
        return reverse('wagtailcommerce_category_modeladmin_edit',
                       args=(quote(result.pk),),
                       current_app='wagtailcommerce',
        )
