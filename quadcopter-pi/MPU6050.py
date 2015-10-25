import math
import threading
import time
__author__ = 'janco'


class MPU6050(threading.Thread):
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c
    gyro_scale = 131.0
    accel_scale = 16384.0

    def __init__(self, bus, address):
        """Init class """
        self.bus = bus
        self.address = address
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)

        (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = self.__read_all()
        self.last_x = self.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
        self.last_y = self.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
        self.gyro_offset_x = gyro_scaled_x
        self.gyro_offset_y = gyro_scaled_y
        self.gyro_total_x = self.last_x - self.gyro_offset_x
        self.gyro_total_y = self.last_y - self.gyro_offset_y
        threading.Thread.__init__(self)

    def run(self):
        time_diff = 0.01
        while(True):
            time.sleep(time_diff - 0.005)
            (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = self.__read_all()

            gyro_scaled_x -= self.gyro_offset_x
            gyro_scaled_y -= self.gyro_offset_y

            gyro_x_delta = (gyro_scaled_x * time_diff)
            gyro_y_delta = (gyro_scaled_y * time_diff)

            self.gyro_total_x += gyro_x_delta
            self.gyro_total_y += gyro_y_delta

            rotation_x = self.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
            rotation_y = self.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

            self.last_x = 0.98 * (self.last_x + gyro_x_delta) + (0.02 * rotation_x)
            self.last_y = 0.98 * (self.last_y + gyro_y_delta) + (0.02 * rotation_y)

    def __read_all(self):
        raw_gyro_data = self.bus.read_i2c_block_data(self.address, 0x43, 6)
        raw_accel_data = self.bus.read_i2c_block_data(self.address, 0x3b, 6)

        gyro_scaled_x = self.twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / self.gyro_scale
        gyro_scaled_y = self.twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / self.gyro_scale
        gyro_scaled_z = self.twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / self.gyro_scale

        accel_scaled_x = self.twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / self.accel_scale
        accel_scaled_y = self.twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / self.accel_scale
        accel_scaled_z = self.twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / self.accel_scale

        return gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z

    def twos_compliment(self,val):
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.dist(y, z))
        return -math.degrees(radians)

    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.dist(x, z))
        return math.degrees(radians)

    def getlastvalues(self):
        return self.last_x, self.last_y

