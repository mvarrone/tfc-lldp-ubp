# from get_process_info import diagram
from db.add_data_sqlite_db import add_data_db, device_type_list_data_db
from db.db_functions import (check_db, check_db_for_logs,
                             check_db_table_device_types,
                             check_db_for_users, check_db_for_extras)
from db.delete_data_sqlite_db import delete_data_db, hostname_list_data_db
from db.get_data_sqlite_db import inventory_data_db
from db.modify_data_sqlite_db import mod_dev_val, modify_data_db
from log.logs_inventory import show_log
from log.log_function import write_to_log_on_startup, write_to_log_on_shutdown
from various.about_situation import about
from various.welcome_situation import welcome
from various.dashboard_situation import dashboard
from various.logout_situation import logout
from db.get_diagrams_in_db import get_prev_diagrams, get_prev_diagram_info_in_db


# def get_diagram(dict_fastapi):
#     diagram(dict_fastapi)

def startup_function():
    return write_to_log_on_startup()


def shutdown_function():
    return write_to_log_on_shutdown()


def welcome_function(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    return welcome(dict_fastapi)


def bd_add_device(hostname, creds, dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    add_data_db(hostname, creds, dict_fastapi)


def bd_show_device_type_list(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    return device_type_list_data_db(dict_fastapi)


def bd_modify_device(hostname_selected, info_creds, dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    modify_data_db(hostname_selected, info_creds, dict_fastapi)


def bd_delete_device(hostname, dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    delete_data_db(hostname, dict_fastapi)


def bd_show_hostname_list(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    return hostname_list_data_db(dict_fastapi)


def bd_show_inventory(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    return inventory_data_db(dict_fastapi)


def about_function(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    return about(dict_fastapi)


def bd_modify_device_values(value, dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    return mod_dev_val(value, dict_fastapi)


def bd_show_logs(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    return show_log(dict_fastapi)


def dashboard_function(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    return dashboard(dict_fastapi)


def logout_function(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    return logout(dict_fastapi)


def bd_get_saved_diagrams(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    return get_prev_diagrams(dict_fastapi)


def bd_get_diagram_info_by_id(id, dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    check_db_for_extras(dict_fastapi)
    return get_prev_diagram_info_in_db(id, dict_fastapi)
