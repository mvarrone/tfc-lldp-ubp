from log.log_function import write_to_log_just_root


def welcome(dict_fastapi):
    write_to_log_just_root(dict_fastapi)
    return {"endpoint": "root"}
