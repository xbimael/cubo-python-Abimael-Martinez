from kivy.app import App

class Test03App(App):
    def build(self):
        # Al no devolver nada específico aquí, 
        # Kivy carga automáticamente 'test03.kv'
        return 

    def ejecutar_logica(self, valor):
        # Aquí es donde pondríamos el código de comunicación serial
        if valor:
            print(f"Lógica Python: Enviando {valor} al puerto COM...")
            # Accedemos a los elementos del .kv mediante el ID
            self.root.ids.etiqueta_estado.text = f"Enviado: {valor}"
        else:
            self.root.ids.etiqueta_estado.text = "Error: Escribe algo"

if __name__ == '__main__':
    Test03App().run()