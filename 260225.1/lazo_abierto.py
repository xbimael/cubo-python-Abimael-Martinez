from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
import time

# Builder.load_file('lazo_abierto.kv') # <--- Carga su propio Kivy

class ModoOpenLoop(BoxLayout):
    def ejecutar(self, tiempo):
        app = App.get_running_app()
        if app.ser:
            app.ser.write(f"2\n{tiempo}\n".encode())
            print(f"Modo 2 enviado: {tiempo}s")