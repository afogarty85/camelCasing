import os
import sys
from camelCasing import camelCasing as cc


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
case11 = 'Custom.9579bc93-160a-45ac-b3e7-df2aac872478'

s1 = 'AssetRUHeight'
s2 = 'AssetUCnt'
s3 = 'MemorySpeed_Corrected'
s4 = 'Wmi_SMBIOSMemoryType'
s5 = 'Fru_MemorySPDSize'
s6 = 'Wmi_CS_SystemSKUNumber'
s7 = 'UefiDbx_UefiDbxKeyStatus'
s8 = 'L5_Board_Serial_Number'
s9 = 'Power Load (40%)'
s10 = 'iaasByMicrosoft'
s11 = 'ASECRCqaasAutomation'
s12 = 'Custom.CHMEFactoryManufacturing.inactive'
s13 = 'Custom.CHMEFactoryManufacturing.inactive.active.test'



if __name__ == '__main__':

	assert cc.toCamelCase(case1, None) == 'thisIsATest', 'failed'
	assert cc.toCamelCase(case2, None) == 'thisIsATest', 'failed'
	assert cc.toCamelCase(case3, None) == 'thisIsATEst', 'failed'
	assert cc.toCamelCase(case4, None) == 'theQuickBrownFox', 'failed'
	assert cc.toCamelCase(case5, None) == 'theQuickBrownFox', 'failed'
	assert cc.toCamelCase(case6, None) == 'THISISATESTAndThisISATEstB', 'failed'
	assert cc.toCamelCase(case7, None) == 'thisIsATEstimatedT', 'failed'
	assert cc.toCamelCase(case8, None) == 'theQuickBrownFox', 'failed'
	assert cc.toCamelCase(case9, None) == 'theQuickBrownFox', 'failed'
	assert cc.toCamelCase(case10, None) == 'Generation', 'failed'
	assert cc.toCamelCase(case11, None) == 'custom9579bc93160a45acb3e7df2aac872478', 'failed'

	assert cc.toCamelCase(s1, None) == 'assetRUHeight', 'failed'
	assert cc.toCamelCase(s2, None) == 'assetUCnt', 'failed'
	assert cc.toCamelCase(s3, None) == 'memorySpeedCorrected', 'failed'
	assert cc.toCamelCase(s4, ['WMI']) == 'WMISMBIOSMemoryType', 'failed'
	assert cc.toCamelCase(s5, ['WMI', 'FRU']) == 'FRUMemorySPDSize', 'failed'
	assert cc.toCamelCase(s6, ['WMI', 'FRU', 'SKU']) == 'WMICSSystemSKUNumber', 'failed'
	assert cc.toCamelCase(s7, ['WMI', 'FRU', 'SKU', 'UEFI']) == 'UEFIDbxUEFIDbxKeyStatus', 'failed'
	assert cc.toCamelCase(s8, ['WMI', 'FRU', 'SKU', 'UEFI']) == 'L5BoardSerialNumber', 'failed'
	assert cc.toCamelCase(s9, ['WMI', 'FRU', 'SKU', 'UEFI']) == 'powerLoad40', 'failed'
	assert cc.toCamelCase(s10, ['IaaS']) == 'IaaSByMicrosoft', 'failed'
	assert cc.toCamelCase(s11, ['ASECRC', 'QaaS']) == 'ASECRCQaaSAutomation', 'failed'
	assert cc.toCamelCase(s12, ['WMI', 'FRU']) == 'customCHMEFactoryManufacturingInactive', 'failed'
	assert cc.toCamelCase(s13, ['WMI', 'FRU']) == 'customCHMEFactoryManufacturingInactiveActiveTest', 'failed'
	print('all tests passed!')
