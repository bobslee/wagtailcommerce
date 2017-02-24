"""
get_model taken from django-oscar in
oscar.core.loading.

Copyright (c) 2011-2014 Tangent Communications PLC and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
   
    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Tangent Communications PLC nor the names of its contributors 
       may be used to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from importlib import import_module

from django.apps import apps
from django.apps.config import MODELS_MODULE_NAME
from django.conf import settings
from django.core.exceptions import AppRegistryNotReady, ImproperlyConfigured

def get_model(app_label, model_name):
    """
    Fetches a Django model using the app registry.

    This doesn't require that an app with the given app label exists,
    which makes it safe to call when the registry is being populated.
    All other methods to access models might raise an exception about the
    registry not being ready yet.
    Raises LookupError if model isn't found.
    """
    try:
        return apps.get_model(app_label, model_name)
    except AppRegistryNotReady:
        if apps.apps_ready and not apps.models_ready:
            # If this function is called while `apps.populate()` is
            # loading models, ensure that the module that defines the
            # target model has been imported and try looking the model up
            # in the app registry. This effectively emulates
            # `from path.to.app.models import Model` where we use
            # `Model = get_model('app', 'Model')` instead.
            app_config = apps.get_app_config(app_label)
            # `app_config.import_models()` cannot be used here because it
            # would interfere with `apps.populate()`.
            import_module('%s.%s' % (app_config.name, MODELS_MODULE_NAME))
            # In order to account for case-insensitivity of model_name,
            # look up the model through a private API of the app registry.
            return apps.get_registered_model(app_label, model_name)
        else:
            # This must be a different case (e.g. the model really doesn't
            # exist). We just re-raise the exception.
            raise

def get_product_model():
    """
    Returns the Product model that is active in this project.
    """
    try:
        app_label, model_name = settings.COMMERCE_PRODUCT_MODEL.split('.')
        return get_model(app_label, model_name)
    except AttributeError:
        from wagtailcommerce.models import Product
        return Product
    except ValueError:
        raise ImproperlyConfigured("COMMERCE_PRODUCT_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "COMMERCE_PRODUCT_MODEL refers to model '%s' that has not been installed"
            % settings.COMMERCE_PRODUCT_MODEL)
