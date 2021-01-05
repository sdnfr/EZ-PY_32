from micropython import const



#define pins
CS_pin = const(19)
RD_pin = const(32)
WR_pin = const(22)
RST_pin = const(21)
CDRS_pin = const(23)

DO_pin = const(12)
D1_pin = const(14)
D2_pin = const(2)
D3_pin = const(15)
D4_pin = const(4)
D5_pin = const(16)
D6_pin = const(17)
D7_pin = const(13)



CS = const(0x01<<CS_pin)
RD = const(0x01<<RD_pin)
WR = const(0x01<<WR_pin)
RST = const(0x01<<RST_pin)
CDRS = const(0x01<<CDRS_pin)
DO = const(0x01<<DO_pin)
D1 = const(0x01<<D1_pin)
D2 = const(0x01<<D2_pin)
D3 = const(0x01<<D3_pin) 
D4 = const(0x01<<D4_pin)
D5 = const(0x01<<D5_pin)
D6 = const(0x01<<D6_pin)
D7 = const(0x01<<D7_pin)
dmask = const(0x01<< DO_pin ^ 0x01<< D1_pin ^0x01<< D2_pin ^ 0x01<< D3_pin ^ 0x01<< D4_pin ^ 0x01<< D5_pin ^ 0x01<< D6_pin ^ 0x01<< D7_pin)

