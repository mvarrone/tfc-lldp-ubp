

device_type_list = [
    "juniper_junos",
    "huawei_vrp",
    "hp_procurve",
    "hp_comware",
    "cisco_xr",
    "cisco_s300",
    "cisco_nxos",
    "cisco_ios",
    "brocade_netiron",
    "brocade_fastiron",
    "broadcom_icos",
    "aruba_aoscx",
    "arista_eos"
]

vendor_name_list = []
vendor_os_name_list = []
for vendor in device_type_list:
    vendor_name = vendor.split("_")

    vendor_name_list.append(vendor_name[0])
    vendor_os_name_list.append(vendor_name[1])

print("\nvendor_name_list: \n", vendor_name_list, "\n")
print("\nvendor_os_name_list: \n", vendor_os_name_list, "\n")
