import streamlit as st
from pathlib import Path
import os

# -----------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------------
st.set_page_config(
    page_title="Pijao, Ciudad Sin Prisa",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------
# GESTIÓN DE ARCHIVOS (DETECCIÓN ROBUSTA)
# -----------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

def find_asset(name):
    """Busca un archivo ignorando su extensión y formato de mayúsculas/minúsculas."""
    if not ASSETS_DIR.exists():
        return None
    
    # Extensiones comunes soportadas
    exts = ['.mp4', '.mov', '.avi', '.jpg', '.jpeg', '.png', '.webp', '.mp3', '.wav',
            '.MP4', '.MOV', '.AVI', '.JPG', '.JPEG', '.PNG', '.WEBP', '.MP3', '.WAV']
    
    for ext in exts:
        file_path = ASSETS_DIR / f"{name}{ext}"
        if file_path.exists():
            return str(file_path)
    return None

def display_missing(name):
    """Mensaje discreto si un recurso realmente no existe."""
    st.caption(f"*(Recurso visual {name} no disponible)*")

# -----------------------------------------
# ESTILOS CSS Y NAVEGACIÓN
# -----------------------------------------
st.markdown("""
    <style>
        /* Tipografía y colores base */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Lato', sans-serif;
            color: #333333;
            background-color: #F9F8F6; /* Blanco cálido / crema */
        }
        
        h1, h2, h3, h4, h5 {
            font-family: 'Playfair Display', serif;
            color: #2C3E2D; /* Verde profundo */
            text-align: center;
        }

        /* Barra de navegación */
        .navbar {
            position: fixed;
            top: 0;
            width: 100%;
            background-color: rgba(249, 248, 246, 0.95);
            z-index: 9999;
            padding: 15px 0;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            backdrop-filter: blur(5px);
        }
        .navbar a {
            margin: 0 15px;
            text-decoration: none;
            color: #4A3B32; /* Café madera */
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: color 0.3s;
        }
        .navbar a:hover {
            color: #2C3E2D;
        }

        /* Portada Overlay */
        .hero-overlay {
            position: relative;
            margin-top: -50vh; /* Sube el texto sobre el video nativo */
            z-index: 10;
            text-align: center;
            color: white;
            background: rgba(0,0,0,0.4);
            padding: 40px 20px;
            border-radius: 10px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        .hero-overlay h1 {
            color: white;
            font-size: 3rem;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }
        .hero-overlay p {
            font-size: 1.2rem;
            margin-bottom: 30px;
            font-style: italic;
            font-family: 'Playfair Display', serif;
        }
        
        /* Ajuste de videos nativos */
        [data-testid="stVideo"] video {
            object-fit: cover;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* Botones personalizados con enlaces */
        .btn-custom {
            display: inline-block;
            padding: 12px 25px;
            background-color: #4A3B32;
            color: white !important;
            text-decoration: none;
            text-transform: uppercase;
            font-size: 13px;
            letter-spacing: 1px;
            border-radius: 3px;
            transition: background 0.3s;
            margin: 5px;
        }
        .btn-custom:hover {
            background-color: #2C3E2D;
        }

        /* Secciones */
        .section-padding {
            padding-top: 80px;
            padding-bottom: 40px;
        }
        .frase-poetica {
            text-align: center;
            font-style: italic;
            color: #666;
            margin-top: 10px;
            margin-bottom: 30px;
            font-family: 'Playfair Display', serif;
        }
        
        /* Timeline */
        .timeline {
            border-left: 2px solid #2C3E2D;
            padding-left: 20px;
            margin-left: 20px;
        }
        .timeline-item {
            margin-bottom: 25px;
        }
        .timeline-year {
            font-weight: bold;
            color: #2C3E2D;
            font-size: 1.1em;
        }
    </style>

    <!-- HTML DE LA NAVEGACIÓN -->
    <div class="navbar" id="inicio">
        <a href="#inicio">Inicio</a>
        <a href="#experiencia">Experiencia</a>
        <a href="#casas">Casas del Ayer</a>
        <a href="#guerreros">Historia Visual</a>
        <a href="#conoce">Conoce Pijao</a>
        <a href="#territorio">Territorio y Clima</a>
        <a href="#recorrido">Recorrido Audiovisual</a>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------
# 1. PORTADA (VPINICIO)
# -----------------------------------------
st.markdown("<div class='section-padding'></div>", unsafe_allow_html=True)

vpinicio_path = find_asset("VPINICIO")
if vpinicio_path:
    # Mostramos el video ocupando el ancho, en loop y silenciado
    st.video(vpinicio_path, autoplay=True, loop=True, muted=True)
    # Overlay sobre el video
    st.markdown("""
        <div class="hero-overlay">
            <h1>PIJAO, CIUDAD SIN PRISA</h1>
            <p>Te invitamos a recorrer lento a nuestro municipio</p>
            <a href="#experiencia" class="btn-custom">INICIAR TRAVESÍA</a>
            <a href="#recorrido" class="btn-custom">RECORRIDO AUDIOVISUAL</a>
        </div>
    """, unsafe_allow_html=True)
else:
    st.title("PIJAO, CIUDAD SIN PRISA")
    st.markdown("<p style='text-align:center;'>Te invitamos a recorrer lento a nuestro municipio</p>", unsafe_allow_html=True)
    display_missing("VPINICIO")

# Espacio para asegurar que el overlay no pise el siguiente contenido
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# -----------------------------------------
# CONTROL DE AUDIO (M1)
# -----------------------------------------
st.markdown("---")
st.markdown("### 🎧 SONIDO DE AMBIENTE")
st.markdown("<p style='text-align:center; font-size:14px;'>Activa el sonido para acompañar tu travesía.</p>", unsafe_allow_html=True)
m1_path = find_asset("M1")
if m1_path:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.audio(m1_path, format="audio/mp3", loop=True)
else:
    display_missing("M1")
st.markdown("---")

# -----------------------------------------
# 2. LA EXPERIENCIA (VIDEO PRINCIPAL)
# -----------------------------------------
st.markdown("<div id='experiencia' class='section-padding'></div>", unsafe_allow_html=True)
st.header("LA EXPERIENCIA")
st.markdown("<p style='text-align:center;'>Hay lugares que no se visitan solamente: se viven.</p>", unsafe_allow_html=True)

video_path = find_asset("VIDEO")
if video_path:
    # Omitir los primeros 5 segundos nativamente usando el parámetro start_time de Streamlit
    st.video(video_path, start_time=5)
    st.markdown("<p class='frase-poetica'>En Pijao, el tiempo también hace parte del paisaje.</p>", unsafe_allow_html=True)
else:
    display_missing("VIDEO")

# -----------------------------------------
# 3. CASAS DEL AYER
# -----------------------------------------
st.markdown("<div id='casas' class='section-padding'></div>", unsafe_allow_html=True)
st.header("CASAS DEL AYER")
st.markdown("""
<div style='text-align:center; max-width: 800px; margin: 0 auto; margin-bottom: 30px;'>
La arquitectura tradicional de Pijao es un testimonio vivo del patrimonio cafetero. 
El bahareque, la madera y los amplios balcones no son solo elementos estéticos, sino una respuesta 
sabia de adaptación al clima y a la topografía de nuestras montañas.
</div>
""", unsafe_allow_html=True)

col_c1, col_c2 = st.columns(2)
f1 = find_asset("F1")
f3 = find_asset("F3")
f4 = find_asset("F4")
f7 = find_asset("F7")

with col_c1:
    if f1: st.image(f1, use_container_width=True); st.markdown("<p class='frase-poetica'>Memoria viva en cada balcón.</p>", unsafe_allow_html=True)
    if f4: st.image(f4, use_container_width=True); st.markdown("<p class='frase-poetica'>Arquitectura que respira la historia del café.</p>", unsafe_allow_html=True)
with col_c2:
    if f3: st.image(f3, use_container_width=True); st.markdown("<p class='frase-poetica'>La madera conserva el eco de las montañas.</p>", unsafe_allow_html=True)
    if f7: st.image(f7, use_container_width=True); st.markdown("<p class='frase-poetica'>Pijao protege su paisaje y su legado.</p>", unsafe_allow_html=True)

# -----------------------------------------
# 4. HISTORIA DE GUERREROS
# -----------------------------------------
st.markdown("<div id='guerreros' class='section-padding'></div>", unsafe_allow_html=True)
st.header("HISTORIA DE GUERREROS")
st.markdown("<p style='text-align:center;'>La identidad de un pueblo también vive en sus rostros y pequeños momentos.</p>", unsafe_allow_html=True)

# Galería narrativa
guerreros_fotos = ["F2", "F5", "F6", "F16", "F17"]
cols_g = st.columns(len(guerreros_fotos))
for i, foto_name in enumerate(guerreros_fotos):
    f_path = find_asset(foto_name)
    with cols_g[i]:
        if f_path:
            st.image(f_path, use_container_width=True)
st.markdown("<p class='frase-poetica' style='margin-top:20px;'>Territorio de memoria, paisaje y encuentro humano.</p>", unsafe_allow_html=True)

# -----------------------------------------
# 5. CONOCE PIJAO
# -----------------------------------------
st.markdown("<div id='conoce' class='section-padding'></div>", unsafe_allow_html=True)
st.header("CONOCE PIJAO")
col_cp1, col_cp2 = st.columns([1, 1])

with col_cp1:
    f8 = find_asset("F8")
    if f8: st.image(f8, use_container_width=True)

with col_cp2:
    st.markdown("""
    ### La Ciudad Sin Prisa
    Pijao invita a mirar de otra manera. Un municipio donde convergen:
    * **Paisaje y Naturaleza**
    * **Arquitectura y Patrimonio**
    * **Cultura del Café**
    * **Identidad y Turismo Responsable**
    
    Caminar despacio también es una forma de conocer.
    """)
    st.markdown("<br><a href='https://www.youtube.com/watch?v=UPRAk3g7YVg' target='_blank' class='btn-custom'>CONOCE MÁS (VIDEO)</a>", unsafe_allow_html=True)

# -----------------------------------------
# 6. EL TERRITORIO, CLIMA Y UBICACIÓN
# -----------------------------------------
st.markdown("<div id='territorio' class='section-padding'></div>", unsafe_allow_html=True)
st.header("EL TERRITORIO")

tab1, tab2, tab3 = st.tabs(["Geografía", "Clima", "Ubicación e Historia"])

with tab1:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("""
        **Región Andina / Cordillera Central**
        
        Pijao se asienta en un entorno privilegiado de la Cordillera Central de Colombia, 
        caracterizado por su imponente **montaña, el piedemonte y el valle**. Un relieve que define 
        el carácter y la vocación de sus tierras.
        """)
    with col_t2:
        f9 = find_asset("F9")
        if f9: st.image(f9, use_container_width=True)

with tab2:
    st.markdown("""
    **Dinámica Climática**
    * **Precipitaciones:** Superiores a 2400 mm en las zonas montañosas y aproximadamente 1800 mm anuales en otras zonas señaladas.
    * **Vientos:** Durante el día, predominan los vientos que ascienden desde el valle del río Cauca hacia la montaña, refrescando el entorno cafetero.
    """)
    f10 = find_asset("F10")
    if f10: st.image(f10, use_container_width=True)

with tab3:
    col_u1, col_u2 = st.columns([1, 1.5])
    with col_u1:
        st.markdown("""
        **Límites y Ubicación:**
        * **Norte:** Córdoba
        * **Este:** Tolima
        * **Sur:** Génova
        * **Oeste:** Valle del Cauca
        * **Noroeste:** Buenavista
        
        *Población del centro: La Mariela.*
        *Distancia: Aproximadamente a 32 km de Armenia.*
        """)
    with col_u2:
        st.markdown("""
        <div class='timeline'>
            <div class='timeline-item'><span class='timeline-year'>1902</span><br>Fundación y denominación inicial como San José de Colón.</div>
            <div class='timeline-item'><span class='timeline-year'>1905</span><br>Corregimiento de Calarcá.</div>
            <div class='timeline-item'><span class='timeline-year'>1912</span><br>Creación de la parroquia.</div>
            <div class='timeline-item'><span class='timeline-year'>1926</span><br>Erigido como municipio.</div>
            <div class='timeline-item'><span class='timeline-year'>1931</span><br>Adopción del nombre Pijao.</div>
            <div class='timeline-item'><span class='timeline-year'>2014</span><br>Vinculación a Cittaslow / concepto de "Ciudad Sin Prisa".</div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------
# 7. DESCUBRE PIJAO
# -----------------------------------------
st.markdown("<div class='section-padding'></div>", unsafe_allow_html=True)
st.header("DESCUBRE PIJAO")
st.markdown("<p style='text-align:center;'>Categorías de nuestra identidad.</p>", unsafe_allow_html=True)

desc_cols = st.columns(3)
categorias = [
    ("Arquitectura", "F11"), ("Naturaleza", "F12"), ("Cultura", "F13"),
    ("Café", "F14"), ("Patrimonio", "F15"), ("Rutas y experiencias", "F18")
]

for idx, (titulo, foto) in enumerate(categorias):
    with desc_cols[idx % 3]:
        f_path = find_asset(foto)
        if f_path:
            st.image(f_path, use_container_width=True)
        st.markdown(f"<h4 style='margin-top:10px;'>{titulo}</h4>", unsafe_allow_html=True)

# -----------------------------------------
# 8. RECORRIDO AUDIOVISUAL (MANUAL)
# -----------------------------------------
st.markdown("<div id='recorrido' class='section-padding'></div>", unsafe_allow_html=True)
st.markdown("---")
st.header("RECORRIDO AUDIOVISUAL")
st.markdown("<p style='text-align:center;'>Navega a tu propio ritmo.</p>", unsafe_allow_html=True)

# Preparar lista de assets para el recorrido (18 fotos + 2 videos)
recorrido_items = [f"F{i}" for i in range(1, 19)] + ["VIDEO", "VPINICIO"]
# Filtrar solo los que existen
items_disponibles = [item for item in recorrido_items if find_asset(item) is not None]

# Frases poéticas para asignar cíclicamente
frases_recorrido = [
    "En Pijao, el tiempo también hace parte del paisaje.",
    "Cada rincón guarda una historia que merece ser recorrida sin prisa.",
    "Aquí la vida conserva el ritmo de las cosas hechas con tiempo.",
    "Entre montañas, memoria y caminos, Pijao invita a mirar de otra manera.",
    "Hay lugares que no se visitan solamente: se viven.",
    "La identidad de un pueblo también vive en sus pequeños momentos.",
    "Pijao es territorio de memoria, paisaje y encuentro.",
    "Caminar despacio también es una forma de conocer."
]

if items_disponibles:
    # Estado de la sesión para el carrusel
    if 'idx_recorrido' not in st.session_state:
        st.session_state.idx_recorrido = 0

    total_items = len(items_disponibles)
    
    # Controles de navegación
    col_btn1, col_cnt, col_btn2 = st.columns([1, 2, 1])
    
    with col_btn1:
        if st.button("← ANTERIOR"):
            if st.session_state.idx_recorrido > 0:
                st.session_state.idx_recorrido -= 1
            else:
                st.session_state.idx_recorrido = total_items - 1
                
    with col_cnt:
        st.markdown(f"<h4 style='text-align:center;'>{st.session_state.idx_recorrido + 1} / {total_items}</h4>", unsafe_allow_html=True)
        
    with col_btn2:
        if st.button("SIGUIENTE →"):
            if st.session_state.idx_recorrido < total_items - 1:
                st.session_state.idx_recorrido += 1
            else:
                st.session_state.idx_recorrido = 0

    # Mostrar el elemento actual
    current_item = items_disponibles[st.session_state.idx_recorrido]
    current_path = find_asset(current_item)
    frase_actual = frases_recorrido[st.session_state.idx_recorrido % len(frases_recorrido)]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Columna central para limitar el ancho y que se vea elegante
    _, center_col, _ = st.columns([1, 4, 1])
    with center_col:
        if "VIDEO" in current_item or "VPINICIO" in current_item:
            # Si es el VIDEO, aplicamos el corte de los 5 segundos
            if current_item == "VIDEO":
                st.video(current_path, start_time=5)
            else:
                st.video(current_path, autoplay=True, loop=True, muted=True)
        else:
            st.image(current_path, use_container_width=True)
            
        st.markdown(f"<p class='frase-poetica'>{frase_actual}</p>", unsafe_allow_html=True)

else:
    st.info("No hay archivos multimedia disponibles en la carpeta assets.")

# -----------------------------------------
# FOOTER / VOLVER AL INICIO
# -----------------------------------------
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;'>
    <a href="#inicio" class="btn-custom" style='background-color:#2C3E2D;'>↑ VOLVER AL INICIO</a>
    <br><br>
    <p style='font-size: 12px; color: #666;'>Pijao, Ciudad Sin Prisa. Patrimonio Cafetero de Colombia.</p>
</div>
""", unsafe_allow_html=True)