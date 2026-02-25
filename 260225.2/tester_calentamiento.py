from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from conexion_widget import ConexionWidget
from logic_calentamiento import ModoCalentamiento # <--- NUEVO

class ContenedorPrincipal(BoxLayout):
    pass

class TesterApp(App):
    def build(self):
        Builder.load_string('''
<ContenedorPrincipal>:
    orientation: 'vertical'
    padding: 10
    spacing: 20
''')
        
        root = ContenedorPrincipal()
        
        # 1. Creamos el widget de conexión
        self.conexion = ConexionWidget()
        
        # 2. Creamos el widget de calentamiento y le pasamos el de conexión
        self.calentamiento = ModoCalentamiento()
        self.calentamiento.conexion_ref = self.conexion # <--- EL PUENTE
        
        # Añadimos ambos al layout
        root.add_widget(self.conexion)
        root.add_widget(self.calentamiento)
        
        return root

if __name__ == '__main__':
    TesterApp().run()