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

def chunk_string_increment(string, n):
    """
    string: 'aabbccdd'
    n: 2

    returns ['aa', 'aabb', 'aabbcc', 'aabbccdd']
    """

    # chunks = ['aa', 'bb', 'cc', 'dd']
    chunks = [string[i:i+n] for i in range(0, len(string), n)]
    result = []
    step = 1

    # for index, e in enumerate(chunks):
    #     end = step - 1
    #     chunk_inc = ''.join(chunks[0:end])
    #     result.append(chunk_inc)
        
    #     step = (index + 1) * n

    for c in chunks:
        #end = step - 1
        chunk_inc = ''.join(chunks[0:step])
        result.append(chunk_inc)
        
        step = step + 1
    return result
        
