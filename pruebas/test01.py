from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        # El layout organiza los elementos (vertical u horizontal)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Creamos los componentes
        self.mensaje = Label(text="¡Hola! Este es tu primer test en Kivy")
        boton = Button(text="Haz clic aquí", size_hint=(1, 0.5))
        
        # Conectamos el botón a una función
        boton.bind(on_press=self.saludar)
        
        # Añadimos los componentes al layout
        self.layout.add_widget(self.mensaje)
        self.layout.add_widget(boton)
        
        return self.layout

    def saludar(self, instance):
        self.mensaje.text = "¡Funciona! Ya estás programando en Kivy."

if __name__ == '__main__':
    TestApp().run()