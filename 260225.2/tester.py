from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Importamos los widgets que vamos creando (uno a uno)
from conexion_widget import ConexionWidget
# from logic_calentamiento import ModoCalentamiento  # Comentado hasta que esté listo

class ContenedorPrincipal(BoxLayout):
    """Este es el layout que contendrá todos los módulos"""
    pass

class TesterApp(App):
    def build(self):
        # Definimos una estructura básica de prueba en KV
        Builder.load_string('''
<ContenedorPrincipal>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 0.15, 0.15, 0.15, 1
        Rectangle:
            pos: self.pos
            size: self.size
''')
        
        self.root_layout = ContenedorPrincipal()
        
        # --- BLOQUE DE PRUEBAS ---
        # 1. Añadimos el módulo de conexión
        self.conexion = ConexionWidget()
        self.root_layout.add_widget(self.conexion)
        
        # 2. Aquí añadiremos el siguiente módulo cuando esté listo:
        # self.calentamiento = ModoCalentamiento()
        # self.root_layout.add_widget(self.calentamiento)
        
        return self.root_layout

if __name__ == '__main__':
    TesterApp().run()