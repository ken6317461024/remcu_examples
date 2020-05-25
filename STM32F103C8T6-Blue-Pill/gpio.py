import ctypes
import sys
from remcu_include.STM32F10X_HD_StdPeriph_Lib import *

if sys.platform.startswith('win32'): 	#Windows
    remcu = ctypes.WinDLL("remcu.dll")
elif sys.platform.startswith('cygwin'): #Windows/Cygwin
    remcu = ctypes.WinDLL("remcu.dll")
elif sys.platform.startswith('linux'):  #Linux OS
    remcu = ctypes.CDLL("./libremcu.so")
elif sys.platform.startswith('darwin'): #MacOS
    remcu = ctypes.CDLL("./libremcu.dylib")

success = remcu.remcu_connect2GDB("127.0.0.1", 3333, 3)

if success == 0:
    print("Server error. Possible solutions: ")
    print("1. Check connection to debug server")
    print("2. Check debug server running")
    print("3. Run the script using Python2")
    exit()

remcu.remcu_resetRemoteUnit(1)

"""
!< At this stage the microcontroller clock setting is already configured, 
       this is done through SystemInit() function which is called from startup
       file (startup_stm32f10x_xx.s) before to branch to application main.
       To reconfigure the default setting of SystemInit() function, refer to
       remcu_include/system_stm32f10x.c file
"""
remcu.SystemInit()

remcu.RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE)

GPIO_InitStructure = GPIO_InitTypeDef()

GPIO_InitStructure.GPIO_Pin = GPIO_Pin_13
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_10MHz
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP

remcu.GPIO_Init(GPIOC, GPIO_InitStructure.ref())

from time import sleep
#Toogling
while True:
    remcu.GPIO_SetBits(GPIOC, GPIO_Pin_13)
    sleep(0.1)
    remcu.GPIO_ResetBits(GPIOC, GPIO_Pin_13)
    sleep(0.1)
    print("PC13 pin is toogling...")