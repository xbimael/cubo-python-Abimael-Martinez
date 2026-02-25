from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.properties import ObjectProperty

# Cargamos el archivo de diseño
Builder.load_file('monitor_grafico.kv')

class MonitorGrafico(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Creamos el objeto Graph de Kivy Garden
        self.graph = Graph(
            xlabel='t (s)', 
            ylabel='rad/s',
            x_ticks_minor=1, 
            x_ticks_major=5, 
            y_ticks_major=50,
            y_grid_label=True, 
            x_grid_label=True, 
            padding=5,
            x_grid=True, 
            y_grid=True, 
            xmin=0, xmax=10, 
            ymin=0, ymax=255, # Rango inicial (PWM o rad/s)
            label_options={'color': [1, 1, 1, 1], 'bold': True}
        )
        
        # Creamos el plot azul (como en MATLAB)
        self.plot = MeshLinePlot(color=[0, 0.7, 1, 1]) 
        self.graph.add_plot(self.plot)
        
        # Lo añadimos al contenedor del .kv
        self.ids.graph_container.add_widget(self.graph)

    def limpiar_grafica(self, x_max=10):
        self.plot.points = []
        self.graph.xmin = 0
        self.graph.xmax = x_max
        # Reseteamos el eje Y si es necesario, o lo dejamos fijo

    def añadir_punto(self, x, y):
        self.plot.points.append((x, y))
        # Si el tiempo real supera el eje X, lo expandimos
        if x > self.graph.xmax:
            self.graph.xmax = x + 1