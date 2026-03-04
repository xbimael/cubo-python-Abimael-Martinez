import math
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy_garden.graph import MeshLinePlot
from kivy.properties import ObjectProperty, ListProperty

Builder.load_file('monitor_grafico.kv')

class MonitorGrafico(BoxLayout):
    graph = ObjectProperty(None)
    # ### AÑADIDO: Esta es la "matriz" que leerá el botón de guardar
    experiment = ListProperty([]) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plot = MeshLinePlot(color=[0, 0.7, 1, 1])
        self.plot_ref = MeshLinePlot(color=[1, 0, 0, 1])
        self.experiment = [] 
        
        # Un pequeño truco: usamos Clock para evitar el error de inicialización
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.vincular_plots())

    def vincular_plots(self):
        if self.graph:
            self.graph.add_plot(self.plot)
            self.graph.add_plot(self.plot_ref)

    def limpiar_grafica(self, x_max=10):
        self.plot.points = []
        self.plot_ref.points = []
        self.experiment = [] # ### LIMPIAMOS también los datos de guardado
        self.graph.xmin, self.graph.xmax = 0, x_max
        self.graph.ymin, self.graph.ymax = 0, 1
        self.actualizar_marcas()

    # --- NUEVO MÉTODO PARA RECIBIR LOS 4 DATOS DE MATLAB ---
    def actualizar_datos_completos(self, tiempos, voltajes, salidas, filtrados, ref_val=None):
        self.experiment = list(zip(tiempos, voltajes, salidas, filtrados))
        
        # Dibujamos la señal filtrada
        self.dibujar_lote(list(zip(tiempos, filtrados)))

        # Si nos pasan una referencia, dibujamos la línea horizontal
        if ref_val is not None and tiempos:
            # Creamos dos puntos: uno al inicio (0, ref) y otro al final (t_final, ref)
            self.plot_ref.points = [(0, ref_val), (tiempos[-1], ref_val)]

    def actualizar_marcas(self):
        if not self.graph: return
        
        # --- EJE X (Tiempo) ---
        rango_x = self.graph.xmax - self.graph.xmin
        # Ajustamos para tener aprox 10 valores en el eje X
        if rango_x <= 2: self.graph.x_ticks_major = 0.2
        elif rango_x <= 5: self.graph.x_ticks_major = 0.5
        elif rango_x <= 15: self.graph.x_ticks_major = 1
        elif rango_x <= 30: self.graph.x_ticks_major = 2
        else: self.graph.x_ticks_major = 5

        # --- EJE Y (Amplitud) ---
        rango_y = self.graph.ymax - self.graph.ymin
        # Ajustamos para que salgan más etiquetas en el eje Y
        if rango_y <= 1.5: 
            self.graph.y_ticks_major = 0.1  # Salen etiquetas cada 0.1
        elif rango_y <= 5: 
            self.graph.y_ticks_major = 0.5  # Salen etiquetas cada 0.5
        elif rango_y <= 20: 
            self.graph.y_ticks_major = 2    # Salen etiquetas cada 2
        elif rango_y <= 50: 
            self.graph.y_ticks_major = 5    # Salen etiquetas cada 5
        else: 
            self.graph.y_ticks_major = 10   # Salen etiquetas cada 10   

    def añadir_punto(self, x, y):
        self.plot.points.append((x, y))
        cambio = False
        if x > self.graph.xmax:
            self.graph.xmax = x
            cambio = True
        if y > self.graph.ymax:
            self.graph.ymax = math.ceil(y / 5.0) * 5
            cambio = True
        if y < self.graph.ymin:
            self.graph.ymin = math.floor(y / 5.0) * 5
            cambio = True
        if cambio:
            self.actualizar_marcas()

    def dibujar_lote(self, lista_puntos):
        self.plot.points = lista_puntos
        if lista_puntos:
            max_y = max(p[1] for p in lista_puntos)
            min_y = min(p[1] for p in lista_puntos)
            self.graph.ymax = math.ceil(max(1, max_y) / 5.0) * 5
            self.graph.ymin = math.floor(min(0, min_y) / 5.0) * 5
            self.actualizar_marcas()