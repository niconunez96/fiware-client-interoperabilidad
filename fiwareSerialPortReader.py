from serial.serialutil import SerialException
import serial
import serial.tools.list_ports


class CantReadPort(Exception):
    pass


class SerialPortReader:

    LINES_QTY_TO_PROCESS = 10

    @property
    def serial_ports(self):
        """ Lists serial port names
        :returns:
            A list of the serial ports available on the system
        """
        return serial.tools.list_ports.comports()

    def process_port_input_lines(self, port):
        try:
            serial_port = serial.Serial(
                port=port,
                baudrate=9600,
                bytesize=8,
                timeout=2,
                stopbits=serial.STOPBITS_ONE,
            )
            lines_to_process = [
                str(serial_port.readline())
                for n in range(self.LINES_QTY_TO_PROCESS)
            ]
        except SerialException as e:
            raise CantReadPort(str(e))
        except Exception:
            pass

        return lines_to_process
