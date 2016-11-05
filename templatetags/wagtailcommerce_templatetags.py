from __future__ import absolute_import, unicode_literals

from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag(takes_context=True)
def wagtailcommerce_product_index(context, position='bottom-right'):
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

    # # Render the items
    # rendered_items = [item.render(request) for item in items]

    # # Remove any unrendered items
    # rendered_items = [item for item in rendered_items if item]

    # Render the userbar items
    return render_to_string('wagtailcommerce/product/product_index_page.html', {
        'request': request,
        'page': page,
        'revision_id': revision_id
    })
