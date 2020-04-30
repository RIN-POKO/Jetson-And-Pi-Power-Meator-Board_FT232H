import smbus
i2c = smbus.SMBus(1)
word = i2c.read_word_data(0x40, 0x02) & 0xFFFF
result = ( (word << 8) & 0xFF00 ) + (word >> 8)
volt = result * 1.25 / 1000
print(volt)

