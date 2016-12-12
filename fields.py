from django.db import models

class CharNullableField(models.CharField):
    description = "CharField that stores NULL but returns ''"

    def to_python(self, value):
        if isinstance(value, models.CharField):
            return value
        return value or ''
    
    def get_prep_value(self, value):
        return value
