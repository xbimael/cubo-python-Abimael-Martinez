from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

class ModoCalentamiento(BoxLayout):
    def ejecutar(self, tiempo):
        app = App.get_running_app()
        # Accedemos al manager que vive dentro del widget de conexión
        arduino = app.root.ids.con_widget.arduino
        arduino.enviar_datos(1, tiempo)
        respuesta = arduino.enviar_datos(modo=1, valor=tiempo)
        print(f"Respuesta: {respuesta}")