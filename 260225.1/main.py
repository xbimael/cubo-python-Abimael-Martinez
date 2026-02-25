from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty # Cambiamos a esta
from conexion import ConexionWidget
from calentamiento import ModoCalentamiento
from lazo_abierto import ModoOpenLoop

class TestModosApp(App):
    # Definimos la propiedad aquí directamente
    conectado = BooleanProperty(False)

    def build(self):
        return Builder.load_file('main.kv')

if __name__ == '__main__':
    TestModosApp().run()