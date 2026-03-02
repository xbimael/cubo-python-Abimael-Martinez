from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import time

# Cargamos el diseño KV
Builder.load_file('position_zp.kv')

class ModoPositionZP(BoxLayout):
    conexion_ref = ObjectProperty(None) # Referencia al widget de conexión
    grafica_ref = ObjectProperty(None)  # Referencia al monitor gráfico

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.datos_acumulados = []
        self.tsim_limite = 0

    def ejecutar_position_zp(self, k, c, p, ci, pi, ref, t_sim):
        if not (self.conexion_ref and self.conexion_ref.arduino.ser):
            return
        
        try:
            # Convertir inputs
            tsim = float(t_sim)
            k_val = float(k)
            c_val = float(c)
            p_val = float(p)
            ci_val = float(ci)
            pi_val = float(pi)
            r_ef = float(ref)
            
            self.tsim_limite = tsim
            self.datos_acumulados = []
            
            # Limpiar gráfica y configurar ejes
            if self.grafica_ref:
                self.grafica_ref.limpiar_grafica(x_max=tsim)

            arduino = self.conexion_ref.arduino
            arduino.ser.reset_input_buffer()
            
            # Protocolo de comunicación (Modo 6)
            # MATLAB envía: Modo, Ref, Tsim, K, C, P, Ci, Pi
            arduino.ser.write(b"6\n")
            time.sleep(0.05)
            for val in [r_ef, tsim, k_val, c_val, p_val, ci_val, pi_val]:
                arduino.ser.write(f"{val}\n".encode())
                time.sleep(0.02)
            
            # Iniciar lectura de datos
            Clock.unschedule(self.leer_datos)
            Clock.schedule_interval(self.leer_datos, 0.005) # 5ms
            
        except ValueError:
            print("Error: Parámetros inválidos")

    def leer_datos(self, dt):
        arduino = self.conexion_ref.arduino
        
        # Leemos mientras haya datos suficientes (Salida, Tiempo, Voltaje)
        while arduino.ser.in_waiting >= 3:
            try:
                linea_out = arduino.ser.readline().decode('utf-8').strip()
                linea_time = arduino.ser.readline().decode('utf-8').strip()
                arduino.ser.readline() # Descartar línea de voltaje
                
                if not linea_out or not linea_time: continue
                
                dato_salida = float(linea_out)
                dato_tiempo = float(linea_time)
                
                self.datos_acumulados.append((dato_tiempo, dato_salida))
                
                # Actualizar gráfica en tiempo real
                if self.grafica_ref:
                    self.grafica_ref.añadir_punto(dato_tiempo, dato_salida)

                # Verificar fin de simulación
                if dato_tiempo >= self.tsim_limite:
                    self.finalizar_experimento()
                    return False
            except:                
                break
        return True

    def finalizar_experimento(self):
        Clock.unschedule(self.leer_datos)
        if self.grafica_ref and self.datos_acumulados:
            self.grafica_ref.dibujar_lote(self.datos_acumulados)
        print("Simulación Finalizada")