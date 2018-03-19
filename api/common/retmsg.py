
def ret_msg(status=True, msg="success", data={}):
    return {                            \
                "status" : status,      \
                "msg" : msg,            \
                "data" : data           \
            }
