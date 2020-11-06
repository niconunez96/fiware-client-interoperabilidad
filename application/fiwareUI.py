from colorit import color, Colors


class ConsoleUI:
    VERSION = "0.12"
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

    def display_cant_read_port_error(self, exception_msg):
        print(color(
            "Error mientras se intento capturar el puerto:",
            Colors.red,
        ))
        print(color(exception_msg, Colors.red))

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
        if "FrameError" in response:
            print(color(response, Colors.red))
        else:
            print(color(response, Colors.blue))

    def display_no_lines_to_process(self):
        print(color("No hay entradas para procesar", Colors.yellow))
