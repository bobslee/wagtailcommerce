import re

"""
>>> camel_case_to_underscores('CamelCase')
'camel_case'
>>> camel_case_to_underscores('CamelCamelCase')
'camel_camel_case'
>>> camel_case_to_underscores('Camel2Camel2Case')
'camel2_camel2_case'
>>> camel_case_to_underscores'getHTTPResponseCode')
'get_http_response_code'
>>> camel_case_to_underscores'get2HTTPResponseCode')
'get2_http_response_code'
>>> camel_case_to_underscores'HTTPResponseCode')
'http_response_code'
>>> camel_case_to_underscores'HTTPResponseCodeXYZ')
'http_response_code_xyz'
"""
def camel_case_to_underscores(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
