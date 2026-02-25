from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from serial_manager import SerialArduino
from kivy.app import App

# Cargamos su diseño
# Builder.load_file('conexion.kv')

class ConexionWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.arduino = SerialArduino() # El manager vive aquí

    def actualizar_puertos(self):
        print("Buscando puertos...") # Añade este print para depurar
        puertos = self.arduino.listar_puertos()
        self.ids.selector_puerto.values = puertos

    def gestionar_conexion(self, puerto):
        if not self.arduino.conectado:
            exito, mensaje = self.arduino.conectar(puerto)
            if exito:
                self.arduino.conectado = True
                self.ids.estado_conexion.text = "Estado: Connected"
                self.ids.estado_conexion.color = [0, 1, 0, 1]
                self.ids.btn_conectar.text = "DISCONNECT"
                self.ids.btn_conectar.background_color = [1, 0, 0, 1]
            else:
                self.ids.estado_conexion.text = f"Error: {mensaje}"
        else:
            self.arduino.desconectar()
            self.ids.estado_conexion.text = "Estado: Disconnected"
            self.ids.estado_conexion.color = [1, 1, 1, 1]
            self.ids.btn_conectar.text = "CONNECT"
            self.ids.btn_conectar.background_color = [0, 0.6, 0.2, 1]
        app = App.get_running_app()
        app.property('conectado').dispatch(app)