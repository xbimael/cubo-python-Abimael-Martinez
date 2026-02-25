from kivy.app import App
from kivy.lang import Builder
import numpy as np
from scipy import signal
# Importamos específicamente MeshLinePlot
from kivy_garden.graph import Graph, MeshLinePlot

class Test04App(App):
    def build(self):
        return Builder.load_file('test04.kv')

    def graficar_escalon(self, ceros_raw, polos_raw):
        try:
            # 1. Procesar datos
            z = [float(x.strip()) for x in ceros_raw.split(',') if x.strip()]
            p = [float(x.strip()) for x in polos_raw.split(',') if x.strip()]
            
            if not p:
                print("Error: Se necesita al menos un polo")
                return

            # 2. Cálculo de la respuesta al escalón (MATLAB style)
            sys = signal.ZerosPolesGain(z, p, 1)
            t, y = signal.step(sys)

            # 3. Dibujar en el widget Graph de Kivy
            graph = self.root.ids.mi_grafica
            
            # ELIMINAR PLOTS ANTERIORES:
            # En versiones nuevas se hace vaciando la lista de plots
            for p_antiguo in graph.plots[:]:
                graph.remove_plot(p_antiguo)
            
            # 4. Crear el nuevo trazado
            plot = MeshLinePlot(color=[0, 1, 1, 1]) # Color Cian (R, G, B, A)
            
            # Convertimos los datos de numpy a una lista de tuplas (x, y)
            plot.points = [(float(t[i]), float(y[i])) for i in range(len(t))]
            
            # 5. Ajustar escalas de los ejes
            graph.xmin = 0
            graph.xmax = float(max(t)) if len(t) > 0 else 10
            graph.ymin = float(min(y)) if len(y) > 0 else 0
            graph.ymax = float(max(y)) * 1.1 if len(y) > 0 else 1.1
            
            graph.add_plot(plot)
            print("Gráfica actualizada correctamente")

        except Exception as e:
            print(f"Error en el cálculo: {e}")

if __name__ == '__main__':
    Test04App().run()