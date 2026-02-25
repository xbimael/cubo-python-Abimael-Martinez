from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

class ArduinoControlApp(App):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # 1. Sección de entrada de valores
        self.label_info = Label(text="Configuración de Arduino", font_size='20sp')
        self.main_layout.add_widget(self.label_info)

        self.input_valor = TextInput(
            text='', 
            hint_text='Introduce el valor (ej. 150)',
            multiline=False,
            input_filter='float' # Solo permite números
        )
        self.main_layout.add_widget(self.input_valor)

        # 2. Botón de envío
        self.btn_enviar = Button(
            text="Enviar a Arduino", 
            background_color=(0, 0.7, 0.9, 1)
        )
        self.btn_enviar.bind(on_press=self.enviar_datos)
        self.main_layout.add_widget(self.btn_enviar)

        # 3. Consola de estado
        self.estado = Label(text="Estado: Desconectado", color=(1, 0, 0, 1))
        self.main_layout.add_widget(self.estado)

        return self.main_layout

    def enviar_datos(self, instance):
        valor = self.input_valor.text
        if valor:
            # Aquí irá la lógica de pyserial más adelante
            print(f"Enviando {valor} al Arduino...")
            self.estado.text = f"Estado: Enviado valor {valor}"
            self.estado.color = (0, 1, 0, 1) # Cambia a verde
        else:
            self.estado.text = "Error: Introduce un valor primero"
            self.estado.color = (1, 0, 0, 1)

if __name__ == '__main__':
    ArduinoControlApp().run()