import utime
import machine

class ILI9486:
    """Class for ILI9486 based LCD 8bit parallel interface"""
    rotations = {0: 0x88, 90: 0xf8, 180: 0x48, 270: 0x28}

    def __init__(self, driver, width, height, rotation,xstart=-1, ystart=-1):
        self.width = width
        self.height = height
        self.driver = driver
        self.rotation = rotation

    def _convert_color(self, color):
        """color from 8-8-8 to 5-6-5"""
        rgb = color['R'] << 16 | \
            color['G'] << 8 | \
            color['B']
        return ((rgb & 0x00f80000) >> 8) |\
            ((rgb & 0x0000fc00) >> 5) | ((rgb & 0x000000f8) >> 3)

    def reset(self):
        print("not implemented yet")

    def initDisplay(self):
        """init display"""

        self.reset()

        # Read Display MADCTL
        self.driver.cmd(0x0b)
        self.driver.data(0x00)
        self.driver.data(0x00)

        # Sleep OUT
        self.driver.cmd(0x11)

        # Interface Pixel Format
        self.driver.cmd(0x3a)
        self.driver.data(0x55)  # 0x66 5-6-5 / 55 6-6-6

        # Memory Access Control (
        self.driver.cmd(0x36)
        self.driver.data(self.rotations[self.rotation])

        # Power Control 3 (For Normal Mode)
        self.driver.cmd(0xc2)
        self.driver.data(0x44)

        # VCOM Control
        self.driver.cmd(0xc5)
        self.driver.data(0x00)
        self.driver.data(0x00)
        self.driver.data(0x00)
        self.driver.data(0x00)

        # PGAMCTRL(Positive Gamma Control)
        self.driver.cmd(0xe0)
        self.driver.data(0x0F)
        self.driver.data(0x1F)
        self.driver.data(0x1C)
        self.driver.data(0x0C)
        self.driver.data(0x0F)
        self.driver.data(0x08)
        self.driver.data(0x48)
        self.driver.data(0x98)
        self.driver.data(0x37)
        self.driver.data(0x0A)
        self.driver.data(0x13)
        self.driver.data(0x04)
        self.driver.data(0x11)
        self.driver.data(0x0D)
        self.driver.data(0x00)

        # NGAMCTRL (Negative Gamma Correction)
        self.driver.cmd(0xe1)
        self.driver.data(0x0F)
        self.driver.data(0x32)
        self.driver.data(0x2E)
        self.driver.data(0x0B)
        self.driver.data(0x0D)
        self.driver.data(0x05)
        self.driver.data(0x47)
        self.driver.data(0x75)
        self.driver.data(0x37)
        self.driver.data(0x06)
        self.driver.data(0x10)
        self.driver.data(0x03)
        self.driver.data(0x24)
        self.driver.data(0x20)
        self.driver.data(0x00)

        # Digital Gamma Control 1
        self.driver.cmd(0xe2)
        self.driver.data(0x0F)
        self.driver.data(0x32)
        self.driver.data(0x2E)
        self.driver.data(0x0B)
        self.driver.data(0x0D)
        self.driver.data(0x05)
        self.driver.data(0x47)
        self.driver.data(0x75)
        self.driver.data(0x37)
        self.driver.data(0x06)
        self.driver.data(0x10)
        self.driver.data(0x03)
        self.driver.data(0x24)
        self.driver.data(0x20)
        self.driver.data(0x00)

        # Sleep OUT
        self.driver.cmd(0x11)

        # Display ON
        self.driver.cmd(0x29)

    def _set_area(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """select area to work with"""
        self.driver.cmd(0x2a)
        self.driver.data(pos_x1 >> 8)
        self.driver.data(pos_x1 & 0xff)
        self.driver.data(pos_x2 >> 8)
        self.driver.data(pos_x2 & 0xff)
        self.driver.cmd(0x2b)
        self.driver.data(pos_y1 >> 8)
        self.driver.data(pos_y1 & 0xff)
        self.driver.data(pos_y2 >> 8)
        self.driver.data(pos_y2 & 0xff)
        self.driver.cmd(0x2c)

    def fill_rect(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """fill an area"""
        size = (abs(pos_x2 - pos_x1) + 1) * (abs(pos_y2 - pos_y1) + 1)
        self._set_area(
            min(pos_x1, pos_x2),
            min(pos_y1, pos_y2),
            max(pos_x1, pos_x2),
            max(pos_y1, pos_y2)
        )
        # color = self._converted_background_color()
        # color = self._convert_color(self.options['background_color'])
        for _ in range(0, size):
            self.driver.data(0xCC)


class parallell8bitDriver:
    def __init__(self, rst,cs,rs,wr,rd,d0,d1,d2,d3,d4,d5,d6,d7):
        self.rst = rst
        self.cs	= cs
        self.rs	= rs
        self.wr	= wr
        self.rd	= rd
        self.d0	= d0
        self.d1	= d1
        self.d2	= d2
        self.d3	= d3
        self.d4	= d4
        self.d5	= d5
        self.d6	= d6
        self.d7	= d7
        self.pins8bit = list((d0,d1,d2,d3,d4,d5,d6,d7))
    
    def cmd(self,command):
        self.cs.off()
        self.rs.off() #low level for command
        self.wr.off() 
        utime.sleep_us(1)
        self.write8(command)
        utime.sleep_us(100)
        self.wr.on()
        self.write8(0x00)
        self.cs.on()
        utime.sleep_us(100)



    def data(self,data):
        self.cs.off()
        self.rs.on() #low level for command
        self.wr.off() 
        utime.sleep_us(1)
        self.write8(data)
        utime.sleep_us(100)
        self.wr.on()
        self.write8(0x00)
        self.cs.on()
        utime.sleep_us(100)


    def write8 (self,byte):
        #print("{0:b}".format(byte))
        for x in range(8):
            pin = self.pins8bit[x]
            if (byte>>x)&0x1:
                pin.on()
            else:
                pin.off()
