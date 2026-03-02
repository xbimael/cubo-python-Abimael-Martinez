from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import numpy as np
import time
import math

# Cargamos el archivo de diseño correspondiente
Builder.load_file('velocity_zp.kv')

class ModoVelocityZP(BoxLayout):
    conexion_ref = ObjectProperty(None)
    grafica_ref = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.datos_acumulados = []
        self.tsim_limite = 0

    def aplicar_filtro_media_movil(self, datos, ventana=13):
        """Implementa un suavizado básico similar a sgolayfilt."""
        if len(datos) < ventana:
            return datos
        
        datos_suavizados = []
        for i in range(len(datos)):
            if i < ventana:
                # Al principio, usar media de puntos disponibles
                ventana_actual = datos[0:i+1]
            else:
                ventana_actual = datos[i-ventana+1:i+1]
            
            media = sum(ventana_actual) / len(ventana_actual)
            datos_suavizados.append(media)
            
        return datos_suavizados
    
    def ejecutar_velocity_zp(self, k, c, p, ci, pi, ref, t_sim):
        if not (self.conexion_ref and self.conexion_ref.arduino.ser):
            print("ERROR: Arduino no conectado")
            return

        try:
            # Convertimos valores de la interfaz
            k_v = float(k)
            c_v = float(c)
            p_v = float(p)
            ci_v = float(ci)
            pi_v = float(pi)
            ref_v = float(ref) # Voltios
            tsim = float(t_sim)
            
            self.tsim_limite = tsim
            self.datos_acumulados = []
            
            if self.grafica_ref:
                self.grafica_ref.limpiar_grafica(x_max=tsim)

            # --- ENVÍO AL ARDUINO (Protocolo MATLAB Mode 4) ---
            arduino = self.conexion_ref.arduino
            arduino.ser.reset_input_buffer()
            
            # fprintf(app.sp,'%i\n',operationMode); -> Modo 4
            arduino.ser.write(b"4\n")
            time.sleep(0.05)
            
            # fprintf(app.sp,'%f\n',vref);
            arduino.ser.write(f"{ref_v}\n".encode())
            time.sleep(0.02)
            
            # fprintf(app.sp,'%i\n',tsim);
            arduino.ser.write(f"{int(tsim)}\n".encode())
            time.sleep(0.02)
            
            # fprintf(app.sp,'%f\n',k);
            arduino.ser.write(f"{k_v}\n".encode())
            time.sleep(0.02)
            
            # fprintf(app.sp,'%f\n',c);
            arduino.ser.write(f"{c_v}\n".encode())
            time.sleep(0.02)
            
            # fprintf(app.sp,'%f\n',p);
            arduino.ser.write(f"{p_v}\n".encode())
            time.sleep(0.02)
            
            # fprintf(app.sp,'%f\n',c_i);
            arduino.ser.write(f"{ci_v}\n".encode())
            time.sleep(0.02)
            
            # fprintf(app.sp,'%f\n',p_i);
            arduino.ser.write(f"{pi_v}\n".encode())
            time.sleep(0.02)
            
            print("Parámetros Zeros/Poles enviados.")
            
            # --- RECEPCIÓN ---
            Clock.unschedule(self.leer_datos)
            Clock.schedule_interval(self.leer_datos, 0.001) 
            
        except ValueError:
            print("ERROR: Datos numéricos inválidos")

    def leer_datos(self, dt):
        arduino = self.conexion_ref.arduino
        while arduino.ser.in_waiting >= 3:
            try:
                linea_out = arduino.ser.readline().decode('utf-8').strip()
                linea_time = arduino.ser.readline().decode('utf-8').strip()
                linea_volt = arduino.ser.readline().decode('utf-8').strip()
                
                if not linea_out or not linea_time or not linea_volt:
                    continue
                
                dato_salida = float(linea_out)
                dato_tiempo = float(linea_time)
                
                self.datos_acumulados.append((dato_tiempo, dato_salida))
                
                if dato_tiempo >= self.tsim_limite:
                    self.finalizar_y_graficar()
                    return False
            except:
                break
        return True

    def finalizar_y_graficar(self):
        Clock.unschedule(self.leer_datos)
        
        if self.datos_acumulados:
            # 1. Extraer los valores de salida crudos
            valores_crudos = [p[1] for p in self.datos_acumulados]
            tiempos = [p[0] for p in self.datos_acumulados]
            
            # 2. Aplicar el filtro
            valores_filtrados = self.aplicar_filtro_media_movil(valores_crudos, ventana=13)
            
            # 3. Reconstruir los puntos filtrados (tiempo, valor_filtrado)
            self.datos_filtrados = list(zip(tiempos, valores_filtrados))
            
            # 4. Graficar los datos filtrados
            if self.grafica_ref:
                self.grafica_ref.dibujar_lote(self.datos_filtrados)                
        
        print("Simulación Finalizada y Filtrada")