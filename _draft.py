test = ['sprinklers', 'backup power supply', 'access control', 'telephone cabling', 'computer cabling', 'power cabling', 'switchboard', 'air-conditioning', 'smoke/heat detectors', 'raised floor', 'suspended ceiling', 'carpeting', 'openable windows', 'fibre optic connection', 'partition walls', 'BMS']
# for e in test:
#     print(e)

test_dict = {
"sprinklers"                :			"sprinklers",
"access_control"            :			"access control",
"computer_cabling"          :			"computer cabling",
"switchboard"               :  			"switchboard",
"smoke_detectors"           :			"smoke/heat detectors",
"suspended_ceiling"         :			"suspended ceiling",
"openable_windows"          :			"openable windows",
"partition_walls"           :			"partition walls",
"backup_power_supply"       :			"backup power supply",
"telephone_cabling"         :			"telephone cabling",
"power_cabling"             :			"power cabling",
"air_conditioning"          :			"air-conditioning",
"raised_floor"              :			"raised floor",
"carpeting"                 :			"carpeting",
"fibre_optic_connections"   :			"fibre optic connection",
"BMS"                       :			"BMS",
}
for i in test_dict:
    print('"{}" : "{}",'.format(test_dict[i],i))