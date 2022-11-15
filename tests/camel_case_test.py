import os
import sys
sys.path.append(os.getcwd())
from src.camelCasing.camel_case_generator import to_camel_case


# tests
case1 = 'ThisIsATest'
case2 = 'thisIsATest'
case3 = 'ThisIsATEst'
case4 = 'TheQuickBrownFox'
case5 = 'The Quick Brown Fox'
case6 = 'THISISATESTAndThisISATEstB'
case7 = 'thisIsATEstimatedT'
case8 = 'The_Quick_Brown_Fox'
case9 = 'the_quick_brown_fox'
case10 = 'Generation'

s1 = 'AssetRUHeight'
s2 = 'AssetUCnt'
s3 = 'MemorySpeed_Corrected'
s4 = 'Wmi_SMBIOSMemoryType'
s5 = 'Fru_MemorySPDSize'
s6 = 'Wmi_CS_SystemSKUNumber'
s7 = 'UefiDbx_UefiDbxKeyStatus'
s8 = 'L5_Board_Serial_Number'
s9 = 'Power Load (40%)'

if __name__ == '__main__':

	assert to_camel_case(case1, None) == 'thisIsATest', 'failed'
	assert to_camel_case(case2, None) == 'thisIsATest', 'failed'
	assert to_camel_case(case3, None) == 'thisIsATEst', 'failed'
	assert to_camel_case(case4, None) == 'theQuickBrownFox', 'failed'
	assert to_camel_case(case5, None) == 'theQuickBrownFox', 'failed'
	assert to_camel_case(case6, None) == 'THISISATESTAndThisISATEstB', 'failed'
	assert to_camel_case(case7, None) == 'thisIsATEstimatedT', 'failed'
	assert to_camel_case(case8, None) == 'theQuickBrownFox', 'failed'
	assert to_camel_case(case9, None) == 'theQuickBrownFox', 'failed'
	assert to_camel_case(case10, None) == 'Generation', 'failed'

	assert to_camel_case(s1, None) == 'assetRUHeight', 'failed'
	assert to_camel_case(s2, None) == 'assetUCnt', 'failed'
	assert to_camel_case(s3, None) == 'memorySpeedCorrected', 'failed'
	assert to_camel_case(s4, ['WMI']) == 'WMISMBIOSMemoryType', 'failed'
	assert to_camel_case(s5, ['WMI', 'FRU']) == 'FRUMemorySPDSize', 'failed'
	assert to_camel_case(s6, ['WMI', 'FRU', 'SKU']) == 'WMICSSystemSKUNumber', 'failed'
	assert to_camel_case(s7, ['WMI', 'FRU', 'SKU', 'UEFI']) == 'UEFIDbxUEFIDbxKeyStatus', 'failed'
	assert to_camel_case(s8, ['WMI', 'FRU', 'SKU', 'UEFI']) == 'L5BoardSerialNumber', 'failed'
	assert to_camel_case(s9, ['WMI', 'FRU', 'SKU', 'UEFI']) == 'powerLoad40', 'failed'
	print('all tests passed!')
