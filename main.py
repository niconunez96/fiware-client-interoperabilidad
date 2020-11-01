"""
INTEROPERABILIDAD
FIWARE FOR SERIAL COMMUNICATION
POST EXAMPLE 'http://68.183.112.17:7896/iot/d?k=2tggokgpepnvsb2uv4s40d59oc&i=BDTempCasa001#t|30#'
GET EXAMPLE  'http://68.183.112.17:1026/v2/entities/urn:ngsd-ld:BDTempCasa:001?options=values&attrs=measure'
"""  # noqa

from fiwareSerialPortReader import SerialPortReader, CantReadPort
from fiwareUI import UI
from fiwareAPI import FiwareApi


POST_URL = "http://fiware-iot.ddns.net:7896/iot/d?k="
GET_URL = "http://fiware-iot.ddns.net:1026/v2/entities/"


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
    except CantReadPort as exc:
        ui.display_cant_read_port_error(str(exc))


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
