import serial 
import time as t 
import fuzzy_logic_side

class Main:
    def __init__(self):
        self.dimension_class = fuzzy_logic_side.DimensionFLow()

        self.board = serial.Serial(port='COM7',
                            baudrate=9600)
        self.state = True

        self.delay = 0.1

    def flow(self):
        while self.state:
            t.sleep(self.delay)

            received_data = self.board.read_until(b'\n').decode()
            trimmed = received_data.split('.')[0].strip()

            if trimmed.isdigit():
                fuzzy_output = self.dimension_class.sensor_dimension(float(received_data))

                print(fuzzy_output,received_data)

                self.board.write(f'{fuzzy_output}\n'.encode())

Main().flow()

