from __future__ import absolute_import, unicode_literals

from django import template
from django.template.loader import render_to_string

from wagtail.wagtailcore.models import PAGE_TEMPLATE_VAR, Page, PageRevision

register = template.Library()

def get_page_instance(context):
    """
    Given a template context, try and find a Page variable in the common
    places. Returns None if a page can not be found.
    """
    possible_names = [PAGE_TEMPLATE_VAR, 'self']
    for name in possible_names:
        if name in context:
            page = context[name]
            if isinstance(page, Page):
                return page

@register.simple_tag(takes_context=True)
def wagtailcommerce_product_index(context):
    # Find request object
    try:
        request = context['request']
    except KeyError:
        return ''

    # Don't render if this is a preview. Since some routes can render the userbar without going through Page.serve(),
    # request.is_preview might not be defined.
    if getattr(request, 'is_preview', False):
        return ''

    # Only render if the context contains a variable referencing a saved page
    page = get_page_instance(context)
    if page is None:
        return ''

    # Dont render anything if the page has not been saved - i.e. a preview
    if page.pk is None:
        return ''

    return render_to_string('wagtailcommerce/product_index_page.html', {
        'request': request,
        'page': page,
    })
