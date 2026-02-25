from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock

# Cargamos el archivo de diseño
Builder.load_file('open_loop.kv')

class ModoOpenLoop(BoxLayout):
    # Referencias a otros módulos
    conexion_ref = ObjectProperty(None)
    grafica_ref = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tsim_limite = 0
        self.tiempo_actual = 0

    def ejecutar_open_loop(self, v_input, t_sim):
        print("Botón presionado: Iniciando lógica...")
        
        try:
            v = float(v_input)
            u = int(v * 255 / 12)
            tsim = float(t_sim)
            self.tsim_limite = tsim
            
            if self.grafica_ref:
                self.grafica_ref.limpiar_grafica(x_max=tsim)

            # Verificamos si realmente podemos enviar
            if self.conexion_ref and self.conexion_ref.arduino.ser:
                arduino = self.conexion_ref.arduino
                arduino.ser.write(f"2\n{u}\n{tsim}\n".encode())
                print(f"Enviado al puerto: 2, {u}, {tsim}")
                Clock.schedule_interval(self.leer_datos, 0.05)
            else:
                print("AVISO: No hay conexión serie, pero la lógica se ejecutó.")
                
        except ValueError:
            print("Error: Los valores de entrada no son válidos.")

    def leer_datos(self, dt):
        arduino = self.conexion_ref.arduino
        
        # Mientras haya datos esperando en el buffer
        while arduino.ser.in_waiting > 0:
            try:
                linea = arduino.ser.readline().decode('utf-8').strip()
                if not linea: continue
                
                # Tu Arduino envía 3 valores por cada muestra:
                # salida (rad/s), tiempo (s), tensión (V)
                # Según tu código MATLAB, leemos secuencialmente:
                
                dato_salida = float(linea)
                # Leemos las siguientes dos líneas que deberían venir tras la primera
                dato_tiempo = float(arduino.ser.readline().decode('utf-8').strip())
                dato_tension = float(arduino.ser.readline().decode('utf-8').strip())

                # Actualizamos la gráfica
                if self.grafica_ref:
                    self.grafica_ref.añadir_punto(dato_tiempo, dato_salida)
                
                self.tiempo_actual = dato_tiempo
                
                # Si llegamos al final de la simulación
                if self.tiempo_actual >= self.tsim_limite:
                    print("SIMULACIÓN FINALIZADA")
                    return False # Detiene el Clock automáticamente

            except Exception as e:
                print(f"Error en recepción: {e}")
                return False # Detiene el Clock si hay error grave
        
        return True # Mantiene el Clock activo