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
        app = App.get_running_app()
        
        if not self.arduino.conectado:
            exito, mensaje = self.arduino.conectar(puerto)
            if exito:
                # ... tu código de colores y textos ...
                app.conectado = True # <--- ESTO desbloquea todo al instante
            else:
                self.ids.estado_conexion.text = f"Error: {mensaje}"
        else:
            self.arduino.desconectar()
            # ... tu código de colores y textos ...
            app.conectado = False # <--- ESTO bloquea todo al instante