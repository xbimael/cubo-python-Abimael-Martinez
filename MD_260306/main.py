from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

# Componentes de KivyMD
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

# Importación de tus módulos
from conexion_widget import ConexionWidget
from monitor_grafico import MonitorGrafico
from logic_calentamiento import ModoCalentamiento
from logic_open_loop import ModoOpenLoop
from logic_velocity_actions import ModoVelocityActions
from logic_velocity_zp import ModoVelocityZP
from logic_position_actions import ModoPositionActions
from logic_position_zp import ModoPositionZP
from guardar import GuardarResultadosWidget

class Tab(MDFloatLayout, MDTabsBase):
    '''Clase para el contenido de cada pestaña.'''
    pass

class TesterApp(MDApp): # <--- Cambio a MDApp
    def build(self):
        # 1. Configuración del Tema Material Design
        self.theme_cls.primary_palette = "Blue"  # Color principal
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_hue = "700"

        # 2. Contenedor Principal (Usamos MDBoxLayout para sombras y elevación)
        main_layout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        # 3. Módulo de Conexión
        self.conexion = ConexionWidget()
        main_layout.add_widget(self.conexion)

        # 4. Zona de trabajo (Horizontal)
        zona_trabajo = MDBoxLayout(orientation='horizontal', spacing=dp(10))

        # --- PANEL DE PESTAÑAS (MATERIAL DESIGN) ---
        # MDTabs sustituye al TabbedPanel para un look más moderno
        self.tabs = MDTabs(size_hint_x=0.5)

        # --- MONITOR GRÁFICO Y BOTÓN DE GUARDADO ---
        panel_derecho = MDBoxLayout(orientation='vertical', size_hint_x=0.5, spacing=dp(5))
        
        self.grafica = MonitorGrafico(size_hint_y=1)
        self.boton_guardar = GuardarResultadosWidget(grafica_ref=self.grafica)

        panel_derecho.add_widget(self.grafica)
        panel_derecho.add_widget(self.boton_guardar)

        # --- CONFIGURACIÓN DE PESTAÑAS ---
        # En MDTabs, cada pestaña se añade con un método específico o vía .kv
        # Por ahora las creamos y las vinculamos
        
        self._añadir_pestana("WARM UP", ModoCalentamiento(conexion_ref=self.conexion))
        self._añadir_pestana("OPEN LOOP", ModoOpenLoop(conexion_ref=self.conexion, grafica_ref=self.grafica))
        self._añadir_pestana("VELOCITY ACTIONS", ModoVelocityActions(conexion_ref=self.conexion, grafica_ref=self.grafica))
        self._añadir_pestana("VELOCITY ZP", ModoVelocityZP(conexion_ref=self.conexion, grafica_ref=self.grafica))
        self._añadir_pestana("POSITION ACTIONS", ModoPositionActions(conexion_ref=self.conexion, grafica_ref=self.grafica))
        self._añadir_pestana("POSITION ZP", ModoPositionZP(conexion_ref=self.conexion, grafica_ref=self.grafica))

        # Ensamblaje final
        zona_trabajo.add_widget(self.tabs)
        zona_trabajo.add_widget(panel_derecho)
        main_layout.add_widget(zona_trabajo)

        return main_layout

    def _añadir_pestana(self, titulo, contenido_widget):
        """Método auxiliar para añadir pestañas de forma limpia en MDTabs"""
        class Tab(MDFloatLayout, MDTabsBase):
            '''Clase necesaria para que MDTabs funcione correctamente'''
            pass

        nueva_tab = Tab(title=titulo)
        nueva_tab.add_widget(contenido_widget)
        self.tabs.add_widget(nueva_tab)

    def on_start(self):
        Window.maximize()

if __name__ == '__main__':
    TesterApp().run()