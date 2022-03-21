# from get_process_info import diagram
from db.add_data_sqlite_db import add_data_db, device_type_list_data_db
from db.db_functions import (check_db, check_db_for_logs,
                             check_db_table_device_types,
                             check_db_for_users)
from db.delete_data_sqlite_db import delete_data_db, hostname_list_data_db
from db.get_data_sqlite_db import inventory_data_db
from db.modify_data_sqlite_db import mod_dev_val, modify_data_db
from log.logs_inventory import show_log
from various.about_situation import about
from various.welcome_situation import welcome
from various.dashboard_situation import dashboard
from various.logout_situation import logout


# def get_diagram(dict_fastapi):
#     diagram(dict_fastapi)


def welcome_function(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    welcome(dict_fastapi)


def bd_add_device(hostname, creds, dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    add_data_db(hostname, creds, dict_fastapi)


def bd_show_device_type_list(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    return device_type_list_data_db(dict_fastapi)


def bd_modify_device(hostname_selected, info_creds, dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    modify_data_db(hostname_selected, info_creds, dict_fastapi)


def bd_delete_device(hostname, dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    delete_data_db(hostname, dict_fastapi)


def bd_show_hostname_list(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    return hostname_list_data_db(dict_fastapi)


def bd_show_inventory(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    return inventory_data_db(dict_fastapi)


def about_function(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    about(dict_fastapi)


def bd_modify_device_values(value, dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    return mod_dev_val(value, dict_fastapi)


def bd_show_logs(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    return show_log(dict_fastapi)


def dashboard_function(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    dashboard(dict_fastapi)


def logout_function(dict_fastapi):
    check_db(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)
    check_db_for_users(dict_fastapi)
    logout(dict_fastapi)
