from __future__ import absolute_import, unicode_literals

from importlib import import_module

from django.apps import apps
from django.apps.config import MODELS_MODULE_NAME
from django.conf import settings
from django.core.exceptions import AppRegistryNotReady, ImproperlyConfigured

from wagtailcommerce.utils.version import get_version

from wagtailcommerce.utils.loading import get_product_model

# major.minor.patch.release.number
# release must be one of alpha, beta, rc, or final
VERSION = (1, 0, 0, 'alpha', 0)

__version__ = get_version(VERSION)
