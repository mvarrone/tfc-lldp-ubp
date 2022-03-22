from log.log_function import write_to_log


def welcome(dict_fastapi):
    write_to_log(dict_fastapi)
    return {"endpoint": "root"}
