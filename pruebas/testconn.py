import serial
import serial.tools.list_ports
import time
from kivy.app import App
from kivy.lang import Builder

class TestConnApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ser = None
        self.conectado = False

    def build(self):
        return Builder.load_file('testconn.kv')

    def actualizar_puertos(self):
        puertos = serial.tools.list_ports.comports()
        self.root.ids.selector_puerto.values = [p.device for p in puertos] if puertos else ["No detectado"]

    def gestionar_conexion(self, puerto):
        if not self.conectado:
            if puerto in ["Seleccionar Puerto", "No detectado"]: return
            try:
                # 1. Configuración idéntica a tu MATLAB (115200, Timeout largo)
                # MATLAB usa un timeout de 11 segundos, nosotros pondremos algo similar
                self.ser = serial.Serial(puerto, 115200, timeout=2)
                
                # 2. Esperar al reinicio del Arduino (DTR)
                time.sleep(2) 
                
                # 3. ENVIAR EL '1' (Equivalente al fprintf de MATLAB)
                # Enviamos el 1 seguido de un salto de línea como pide tu %i\n
                self.ser.write(b"1\n")
                print("Enviado '1' al Arduino... esperando respuesta")

                # 4. LEER RESPUESTA (Equivalente al fscanf de MATLAB)
                # Leemos la respuesta del Arduino
                respuesta = self.ser.readline().decode('utf-8').strip()
                print(f"Arduino respondió: {respuesta}")

                # 5. VALIDAR CONEXIÓN (Como tu if connection_read == 1)
                if respuesta == "1":
                    self.conectado = True
                    self.actualizar_interfaz_conexion(True)
                    self.root.ids.estado_conexion.text = "Connected"
                    self.root.ids.estado_conexion.color = [0, 1, 0, 1]
                else:
                    self.root.ids.estado_conexion.text = "Not possible to connect (Wrong Answer)"
                    self.ser.close()
                
            except Exception as e:
                print(f"Error: {e}")
                self.root.ids.estado_conexion.text = "Not possible to connect"
        else:
            self.desconectar()

    def desconectar(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.conectado = False
        self.actualizar_interfaz_conexion(False)

    def actualizar_interfaz_conexion(self, conectado):
        btn = self.root.ids.btn_conectar
        if conectado:
            btn.text = "DISCONNECT"
            btn.background_color = [1, 0, 0, 1]
        else:
            btn.text = "CONNECT"
            btn.background_color = [0, 0.6, 0.2, 1]
            self.root.ids.estado_conexion.text = "Disconnected"
            self.root.ids.estado_conexion.color = [1, 1, 1, 1]

if __name__ == '__main__':
    TestConnApp().run()