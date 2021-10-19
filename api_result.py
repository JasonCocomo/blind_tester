import process_code as p


def api_result(code=p.OK, msg='OK', data=None):
    return {
        "success": code == p.OK,
        "code": code,
        "msg": p.CODE_MSG[code],
        "data": data
    }
