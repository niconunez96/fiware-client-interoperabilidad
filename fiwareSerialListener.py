#  INTEROPERABILIDAD
#  FIWARE FOR SERIAL COMMUNICATION
#  POST EXAMPLE 'http://68.183.112.17:7896/iot/d?k=2tggokgpepnvsb2uv4s40d59oc&i=BDTempCasa001#t|30#'
#  GET EXAMPLE  'http://68.183.112.17:1026/v2/entities/urn:ngsd-ld:BDTempCasa:001?options=values&attrs=measure'
from datetime import datetime
from colorit import background, color, Colors
import serial
import serial.tools.list_ports
import requests


# CONST
VERSION = "0.12"
HEADERS = {'fiware-service': "openiot", 'fiware-servicepath': "/"}
# POST_URL = "http://fiware-iot.ddns.net:7896/iot/d?k="
# GET_URL = "http://fiware-iot.ddns.net:1026/v2/entities/"
POST_URL = "UltrasonicSensor"
GET_URL = "TemperatureSensor"


class CantReadPort(Exception):
    pass


class FiwareApi:
    def post(self, buffer):
        return buffer
        # data = buffer[buffer.find('#') + 1: buffer.find('\\')]
        # buffer = buffer[2:buffer.find('#')]
        # try:
        #     r = requests.post(buffer, data)
        #     pastebin_url = r.text
        #     if len(pastebin_url) == 0:
        #         print("{} POST  {}  Data: {}".format(datetime.now(), r, data))
        #         return "POST['{}']".format(data)
        #     else:
        #         print("{} Post Error: {}".format(datetime.now(), pastebin_url))
        #         return "POST|Error"
        # except Exception:
        #     print("{} Hubo un error en la operación POST", datetime.now())
        #     return "POST|Error"

    def get(self, buffer):
        return buffer
        # try:
        #     r = requests.get(url=buffer[2:buffer.find('\\')], headers=HEADERS)
        #     pastebin_url = str(r.json())
        #     print("{} GET  {}  Data: {}".format(
        #         datetime.now(), r, pastebin_url,
        #     ))
        #     if(str(r).find("[200]") >= 0):
        #         return "GET{}".format(pastebin_url)
        #     else:
        #         return 'GET|Error'
        # except Exception:
        #     print("Hubo un error en la operación GET")
        #     return "GET|Error"


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
        except Exception as e:
            raise CantReadPort(str(e))
        try:
            lines_to_process = [
                str(serial_port.readline())
                for n in range(self.LINES_QTY_TO_PROCESS)
            ]
        except Exception:
            pass

        # for line in lines_to_process:
        #     try:
        #         response = call_fiware_api(line)
        #         print(response)
        #         # serial_port.write(response.encode())
        #     except Exception:
        #         print("Serial timeout")
        return lines_to_process


class UI:
    WELCOME = """
***********************************
*     Interoperabilidad 💻        *
*  Arduino Serial Listener v{}  *
***********************************
""".format(VERSION)

    def display_exit(self):
        print(color("exit...", Colors.white))

    def display_welcome(self):
        print(color(str(self.WELCOME), Colors.orange))

    def display_no_ports_error(self):
        print(
            color(
                "No se detectaron puertos, por favor conecte uno y vuelva a intentar",  # noqa
                Colors.red,
            )
        )

    def display_ports_list(self, serial_ports):
        print()
        print(color("Obteniendo Puertos...", Colors.white))
        for number, port in enumerate(serial_ports):
            print(color("{}- {}".format(number, port), Colors.green))

    def display_has_selected_invalid_option(self):
        print(color("Ingrese una opcion valida", Colors.red))

    def display_port_input_selection(self):
        print()
        print(color("Por favor seleccione un puerto -> ", Colors.white))

    def display_device_selected(self, device):
        print()
        print(color("Seleccionado: {}".format(device), Colors.white))

    def display_waiting(self):
        print()
        print(color("Esperando frames...", Colors.white))

    def display_cant_read_port_error(self):
        print(color(
            "Error mientras se intento capturar el puerto",
            Colors.red,
        ))

    def display_processing_lines(self):
        print(color("Procesando 10 lineas...", Colors.white))

    def display_process_ten_more_lines_option(self):
        print()
        print(
                color(
                    "Desear procesar otras 10 lineas? 'n' o 'N' para no, cualquier otra tecla para continuar el proceso",  # noqa
                    Colors.white,
                )
            )

    def display_api_response(self, response):
        print(color(response, Colors.blue))

    def display_no_lines_to_process(self):
        print(color("No hay entradas para procesar", Colors.yellow))


def call_fiware_api(buffer):
    """
    Devuelve POST['t|25'], POST|Error, GET['30'], GET|Error
    """
    fiware_api = FiwareApi()
    if POST_URL in buffer:
        return fiware_api.post(buffer)
    elif GET_URL in buffer:
        return fiware_api.get(buffer)
    else:
        return "FrameError: {}".format(buffer)


def is_valid_option(option, serial_ports):
    ports_quantity = sum(1 for _ in serial_ports)
    return option >= 0 and option <= ports_quantity


def show_menu(serial_ports):
    option = -1
    should_show_menu = True
    while should_show_menu:
        ui.display_ports_list(serial_ports)
        try:
            ui.display_port_input_selection()
            option = int(input())
            should_show_menu = not is_valid_option(option, serial_ports)
            if should_show_menu:
                ui.display_has_selected_invalid_option()
        except ValueError:
            ui.display_has_selected_invalid_option()
            should_show_menu = True
    return option


def should_keep_capture_lines(ui: UI):
    ui.display_process_ten_more_lines_option()
    option = str(input())
    return option not in ["N", "n"]


def capture_port_lines(ui: UI, serial_port_reader: SerialPortReader, port):
    keep_capture_lines = True
    ui.display_waiting()
    try:
        while keep_capture_lines:
            ui.display_processing_lines()
            lines = serial_port_reader.process_port_input_lines(port)
            if not lines:
                ui.display_no_lines_to_process()
            else:
                for line in lines:
                    response = call_fiware_api(line)
                    ui.display_api_response(response)
            keep_capture_lines = should_keep_capture_lines(ui)
    except CantReadPort:
        ui.display_cant_read_port_error()


def run_program(ui: UI, serial_port_reader: SerialPortReader):
    serial_ports = serial_port_reader.serial_ports
    option = show_menu(serial_ports)
    ui.display_device_selected(serial_ports[option].device)
    capture_port_lines(ui, serial_port_reader, serial_ports[option].device)


if __name__ == '__main__':
    serial_port_reader = SerialPortReader()
    ui = UI()
    serial_ports = serial_port_reader.serial_ports
    ui.display_welcome()
    if not serial_ports:
        ui.display_no_ports_error()
    else:
        try:
            while(True):
                run_program(ui, serial_port_reader)
        except KeyboardInterrupt:
            ui.display_exit()
