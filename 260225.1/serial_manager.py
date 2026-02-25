import serial
import serial.tools.list_ports
import time

class SerialArduino:
    def __init__(self):
        self.ser = None
        self.conectado = False

    def listar_puertos(self):
        puertos = serial.tools.list_ports.comports()
        return [p.device for p in puertos] if puertos else ["No detectado"]

    def conectar(self, puerto):
        try:
            # Configuración idéntica a tu MATLAB
            self.ser = serial.Serial(puerto, 115200, timeout=2)
            time.sleep(2) # Esperar reinicio
            
            self.ser.write(b"1\n") # Handshake
            respuesta = self.ser.readline().decode('utf-8').strip()
            
            if respuesta == "1":
                self.conectado = True
                return True, "Connected"
            else:
                self.ser.close()
                return False, "Wrong Handshake"
        except Exception as e:
            return False, str(e)

    def desconectar(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.conectado = False

    def enviar_datos(self, modo, valor):
        if self.conectado and self.ser:
            try:
                self.ser.reset_input_buffer()
                self.ser.write(f"{modo}\n".encode())
                time.sleep(0.1)
                self.ser.write(f"{valor}\n".encode())
                return self.ser.readline().decode('utf-8').strip()
            except Exception as e:
                return f"Error: {e}"
        return "Not connected"