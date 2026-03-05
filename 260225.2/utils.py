import matplotlib
matplotlib.use('Agg')  # Renderizado en memoria (evita ventanas emergentes)
import matplotlib.pyplot as plt
from io import BytesIO
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage

def crear_ecuacion_latex(texto_latex, altura='100dp'):
    """
    Genera un widget de Imagen de Kivy a partir de código LaTeX.
    Renderizado en blanco con fondo transparente.
    """
    # 1. Crear figura de Matplotlib
    fig = plt.figure(figsize=(6, 1.5), dpi=120)
    fig.patch.set_alpha(0) # Fondo transparente
    
    # 2. Renderizar el texto en BLANCO
    plt.text(0.5, 0.5, f"${texto_latex}$", 
             fontsize=22, color='white',
             ha='center', va='center')
    plt.axis('off')

    # 3. Guardar en un buffer de memoria
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.close(fig) # Liberar memoria
    buf.seek(0)
    
    # 4. Convertir a textura de Kivy y retornar el Widget
    textura = CoreImage(buf, ext='png').texture
    return KivyImage(texture=textura, size_hint_y=None, height=altura)

