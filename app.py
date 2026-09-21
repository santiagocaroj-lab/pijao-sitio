import streamlit as st
import base64
from pathlib import Path
import os
import streamlit.components.v1 as components

# -----------------------------------------
# 1. CONFIGURACIÓN BÁSICA
# -----------------------------------------
st.set_page_config(
    page_title="Pijao, Ciudad Sin Prisa",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------
# 2. GESTIÓN DE ARCHIVOS (ROBUSTA)
# -----------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

def find_asset(name):
    """Busca el archivo ignorando la extensión y las mayúsculas/minúsculas."""
    if not ASSETS_DIR.exists():
        return None
    
    exts = ['.mp4', '.mov', '.webm', '.jpg', '.jpeg', '.png', '.webp', '.mp3', '.wav', '.ogg']
    name_variations = [name, name.lower(), name.upper()]
    
    for n in name_variations:
        for ext in exts:
            path_lower = ASSETS_DIR / f"{n}{ext}"
            path_upper = ASSETS_DIR / f"{n}{ext.upper()}"
            if path_lower.exists(): return str(path_lower)
            if path_upper.exists(): return str(path_upper)
    return None

def display_missing(name):
    """Mensaje discreto si falta un archivo."""
    st.markdown(f"<p style='color: #888; font-style: italic; font-size: 12px; text-align: center;'>(Recurso {name} no disponible)</p>", unsafe_allow_html=True)

def get_audio_base64(name):
    path = find_asset(name)
    if not path: return None
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    ext = path.split('.')[-1].lower()
    mime = f"audio/{ext}" if ext in ['mp3', 'wav', 'ogg'] else "audio/mpeg"
    return f"data:{mime};base64,{b64}"

# -----------------------------------------
# 3. ENRUTAMIENTO (DOS PÁGINAS)
# -----------------------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'bienvenida'

# =====================================================================
# PÁGINA 1: BIENVENIDA CINEMATOGRÁFICA
# =====================================================================
if st.session_state.page == 'bienvenida':
    
    # CSS específico para la Bienvenida
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
        
        /* Ocultar barra superior y márgenes de Streamlit */
        header {visibility: hidden;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        
        /* Convertir el video nativo en fondo a pantalla completa */
        [data-testid="stVideo"] {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1;
        }
        [data-testid="stVideo"] video {
            object-fit: cover; width: 100vw; height: 100vh;
        }

        /* Capa de fotografías que entra con FADE */
        #photos-overlay-div {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: 2; opacity: 0; transition: opacity 4s ease-in-out;
            background-color: black;
        }
        #photos-overlay-div img {
            width: 100vw; height: 100vh; object-fit: cover; opacity: 0.7;
        }

        /* Interfaz de Texto y Botón sobre todo lo demás */
        .ui-layer {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: 10; display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            background: rgba(0,0,0,0.4); text-align: center;
        }
        .ui-title {
            font-family: 'Playfair Display', serif; color: white;
            font-size: 4.5rem; letter-spacing: 4px; margin-bottom: 0px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        }
        .ui-subtitle {
            font-family: 'Playfair Display', serif; font-style: italic;
            color: #E8E5DF; font-size: 1.5rem; margin-bottom: 50px;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.8);
        }
        
        /* Estilizar el botón nativo de Streamlit para integrarlo */
        .stButton {
            position: fixed; top: 65vh; left: 50%; transform: translateX(-50%); z-index: 20;
        }
        .stButton button {
            background-color: transparent !important;
            border: 1px solid white !important;
            color: white !important;
            font-family: 'Lato', sans-serif;
            font-size: 14px !important;
            letter-spacing: 2px;
            padding: 12px 35px !important;
            text-transform: uppercase;
            transition: all 0.4s ease;
            border-radius: 2px !important;
        }
        .stButton button:hover {
            background-color: white !important;
            color: #2C3E2D !important;
        }
        
        @media (max-width: 768px) {
            .ui-title { font-size: 2.5rem; }
            .ui-subtitle { font-size: 1.1rem; }
        }
        </style>
    """, unsafe_allow_html=True)

    # 1. Video de Fondo
    vpinicio = find_asset("VPINICIO")
    if vpinicio:
        st.video(vpinicio, autoplay=True, muted=True, loop=False)
    else:
        st.markdown("<div style='position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #2C3E2D; z-index: 1;'></div>", unsafe_allow_html=True)
    
    # 2. Capa de Fotografías (Fade)
    f_bg = find_asset("F1") or find_asset("F13") or find_asset("F7")
    if f_bg:
        st.markdown(f"""
            <div id="photos-overlay-div">
                <img src="data:image/jpeg;base64,{base64.b64encode(open(f_bg, 'rb').read()).decode()}" />
            </div>
        """, unsafe_allow_html=True)

    # 3. Interfaz de Textos
    st.markdown("""
        <div class="ui-layer">
            <h1 class="ui-title">PIJAO, CIUDAD SIN PRISA</h1>
            <p class="ui-subtitle">Te invitamos a recorrer lento a nuestro municipio</p>
        </div>
    """, unsafe_allow_html=True)

    # 4. Botón de transición a la Travesía
    if st.button("INICIAR TRAVESÍA"):
        st.session_state.page = 'travesia'
        st.rerun()

    # 5. Inyección JS para detectar el fin del video y hacer Fade de fotos
    components.html("""
        <script>
            function waitForVideo() {
                const videos = window.parent.document.getElementsByTagName('video');
                if(videos.length > 0) {
                    videos[0].onended = function() {
                        const overlay = window.parent.document.getElementById('photos-overlay-div');
                        if(overlay) overlay.style.opacity = '1';
                    };
                } else {
                    setTimeout(waitForVideo, 500);
                }
            }
            waitForVideo();
        </script>
    """, height=0)


# =====================================================================
# PÁGINA 2: LA TRAVESÍA
# =====================================================================
elif st.session_state.page == 'travesia':

    # CSS Editorial y Cinematográfico
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
        
        html, body, [class*="st-"] {
            font-family: 'Lato', sans-serif;
            background-color: #F9F8F6;
            color: #333333;
        }
        
        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            color: #2C3E2D; /* Verde profundo */
            text-align: center;
            margin-top: 40px;
            margin-bottom: 20px;
        }
        
        /* Navegación */
        .navbar {
            position: fixed; top: 0; left: 0; width: 100vw;
            background: rgba(249, 248, 246, 0.95);
            z-index: 9998; padding: 15px 0; text-align: center;
            box-shadow: 0 1px 10px rgba(0,0,0,0.05);
            backdrop-filter: blur(5px);
        }
        .navbar a {
            margin: 0 12px; text-decoration: none; color: #4A3B32;
            font-size: 12px; font-weight: 700; text-transform: uppercase;
            letter-spacing: 1px; transition: color 0.3s;
        }
        .navbar a:hover { color: #2C3E2D; }

        /* Ajuste de márgenes superiores para no pisar la navbar */
        .block-container { padding-top: 80px !important; }

        /* Widget de Sonido Lateral */
        .audio-control {
            position: fixed; right: 20px; top: 50%; transform: translateY(-50%);
            z-index: 9999; background: rgba(249,248,246,0.9); padding: 8px 12px;
            border-radius: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 3px solid #4A3B32;
        }
        .audio-control button {
            background: none; border: none; color: #4A3B32;
            font-family: 'Lato', sans-serif; font-size: 11px;
            font-weight: bold; cursor: pointer; letter-spacing: 1px;
        }

        /* Video Horizontal (Regla 15 y 17) */
        [data-testid="stVideo"] video {
            object-fit: cover !important;
            aspect-ratio: 16 / 9 !important;
            width: 100% !important;
            border-radius: 4px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }

        /* Textos y botones */
        .frase-poetica {
            font-family: 'Playfair Display', serif; font-style: italic;
            text-align: center; color: #555; margin-top: 15px; margin-bottom: 30px;
        }
        .editorial-text { font-size: 1.1rem; line-height: 1.8; color: #444; }
        
        .btn-link {
            display: inline-block; padding: 10px 25px; background: #4A3B32;
            color: white !important; text-decoration: none; text-transform: uppercase;
            font-size: 12px; letter-spacing: 1px; border-radius: 2px;
            margin-top: 15px;
        }
        </style>

        <div class="navbar">
            <a href="#casas-del-ayer">Casas del Ayer</a>
            <a href="#historia-de-guerreros">Historia</a>
            <a href="#conoce-pijao">Conoce Pijao</a>
            <a href="#el-territorio">Territorio</a>
            <a href="#descubre-pijao">Descubre</a>
            <a href="#recorrido-audiovisual">Recorrido</a>
        </div>
    """, unsafe_allow_html=True)

    # Widget de Audio (Reglas 9 y 10)
    audio_src = get_audio_base64("M1")
    if audio_src:
        st.markdown(f"""
            <div class="audio-control">
                <audio id="m1-audio" autoplay loop>
                    <source src="{audio_src}">
                </audio>
                <button onclick="var a=document.getElementById('m1-audio'); a.muted=!a.muted; this.innerText=a.muted?'ACTIVAR SONIDO':'QUITAR SONIDO';">QUITAR SONIDO</button>
            </div>
        """, unsafe_allow_html=True)

    # --- SECCIÓN: VIDEO INTRODUCTORIO ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    video_path = find_asset("VIDEO")
    if video_path:
        # Regla 16: Comienza en el segundo 5.
        st.video(video_path, start_time=5)
        st.markdown("<p class='frase-poetica'>El tiempo se detiene en la montaña.</p>", unsafe_allow_html=True)

    # --- SECCIÓN: CASAS DEL AYER ---
    st.header("CASAS DEL AYER", anchor="casas-del-ayer")
    st.markdown("<p class='editorial-text' style='text-align:center; max-width:800px; margin:auto; margin-bottom:30px;'>La arquitectura tradicional de Pijao es un testimonio vivo del patrimonio cafetero. El bahareque, la madera y los amplios balcones son la respuesta de adaptación al clima y conservación del paisaje.</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if find_asset("F1"): st.image(find_asset("F1"), use_container_width=True); st.markdown("<p class='frase-poetica'>Memoria en cada ventana.</p>", unsafe_allow_html=True)
        if find_asset("F4"): st.image(find_asset("F4"), use_container_width=True); st.markdown("<p class='frase-poetica'>Arquitectura que respira café.</p>", unsafe_allow_html=True)
    with c2:
        if find_asset("F3"): st.image(find_asset("F3"), use_container_width=True); st.markdown("<p class='frase-poetica'>Madera y tradición.</p>", unsafe_allow_html=True)
        if find_asset("F7"): st.image(find_asset("F7"), use_container_width=True); st.markdown("<p class='frase-poetica'>Colores del patrimonio.</p>", unsafe_allow_html=True)

    # --- SECCIÓN: HISTORIA DE GUERREROS ---
    st.markdown("---")
    st.header("HISTORIA DE GUERREROS", anchor="historia-de-guerreros")
    cols_g = st.columns(5)
    for i, foto in enumerate(["F2", "F5", "F6", "F16", "F17"]):
        with cols_g[i]:
            path = find_asset(foto)
            if path: st.image(path, use_container_width=True)
    st.markdown("<p class='frase-poetica'>La identidad de un pueblo vive en los rostros y los momentos compartidos.</p>", unsafe_allow_html=True)

    # --- SECCIÓN: CONOCE PIJAO ---
    st.markdown("---")
    st.header("CONOCE PIJAO", anchor="conoce-pijao")
    cp1, cp2 = st.columns([1.2, 1])
    with cp1:
        f13 = find_asset("F13")
        if f13: st.image(f13, use_container_width=True)
    with cp2:
        st.markdown("""
        <div class="editorial-text">
        <br>
        <strong>La Ciudad Sin Prisa</strong><br><br>
        Pijao invita a mirar de otra manera. Un municipio donde convergen el paisaje, la arquitectura, la cultura del café y el turismo responsable. Caminar despacio es una forma profunda de conocer nuestra identidad.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<a href='https://www.youtube.com/watch?v=UPRAk3g7YVg' target='_blank' class='btn-link'>CONOCE MÁS (VIDEO)</a>", unsafe_allow_html=True)

    # --- SECCIÓN: EL TERRITORIO, CLIMA E HISTORIA ---
    st.markdown("---")
    st.header("EL TERRITORIO", anchor="el-territorio")
    
    t1, t2, t3 = st.tabs(["Geografía", "Clima", "Ubicación e Historia"])
    with t1:
        st.markdown("<p class='editorial-text'><b>Región Andina / Cordillera Central</b><br>Pijao se asienta en un entorno de montaña, piedemonte y valle.</p>", unsafe_allow_html=True)
        if find_asset("F9"): st.image(find_asset("F9"), use_container_width=True)
    with t2:
        st.markdown("<p class='editorial-text'><b>Dinámica Climática</b><br>Precipitaciones superiores a 2400 mm en zonas montañosas y aproximadamente 1800 mm anuales en otras zonas señaladas. Durante el día, vientos ascienden desde el valle del río Cauca hacia la montaña.</p>", unsafe_allow_html=True)
        if find_asset("F10"): st.image(find_asset("F10"), use_container_width=True)
    with t3:
        st.markdown("""
        <div class="editorial-text">
        <b>Límites:</b><br>
        Norte: Córdoba | Este: Tolima | Sur: Génova | Oeste: Valle del Cauca | Noroeste: Buenavista.<br><br>
        <b>Línea de tiempo:</b><br>
        • <b>1902:</b> Fundación como San José de Colón.<br>
        • <b>1905:</b> Corregimiento de Calarcá.<br>
        • <b>1912:</b> Creación de la parroquia.<br>
        • <b>1926:</b> Erección como municipio.<br>
        • <b>1931:</b> Adopción del nombre Pijao.<br>
        • <b>2014:</b> Vinculación a Cittaslow (Ciudad Sin Prisa).
        </div>
        """, unsafe_allow_html=True)

    # --- SECCIÓN: DESCUBRE PIJAO ---
    st.markdown("---")
    st.header("DESCUBRE PIJAO", anchor="descubre-pijao")
    desc_cols = st.columns(3)
    cats = [("Arquitectura", "F11"), ("Naturaleza", "F12"), ("Cultura", "F13"), ("Café", "F14"), ("Patrimonio", "F15"), ("Rutas y experiencias", "F18")]
    for idx, (titulo, foto) in enumerate(cats):
        with desc_cols[idx % 3]:
            path = find_asset(foto)
            if path: st.image(path, use_container_width=True)
            st.markdown(f"<h4 style='text-align:center; font-family:Lato;'>{titulo}</h4>", unsafe_allow_html=True)

    # --- SECCIÓN: RECORRIDO AUDIOVISUAL MANUAL ---
    st.markdown("---")
    st.header("RECORRIDO AUDIOVISUAL", anchor="recorrido-audiovisual")
    
    # Generar lista de assets existentes
    all_items = [f"F{i}" for i in range(1, 19)] + ["VIDEO", "VPINICIO"]
    valid_items = [i for i in all_items if find_asset(i) is not None]

    frases = [
        "En Pijao, el tiempo también hace parte del paisaje.",
        "Cada rincón guarda una historia que merece ser recorrida sin prisa.",
        "Aquí la vida conserva el ritmo de las cosas hechas con tiempo.",
        "Entre montañas, memoria y caminos, Pijao invita a mirar de otra manera.",
        "Hay lugares que no se visitan solamente: se viven.",
        "La identidad de un pueblo también vive en sus pequeños momentos.",
        "Pijao es territorio de memoria, paisaje y encuentro.",
        "Caminar despacio también es una forma de conocer."
    ]

    if valid_items:
        if 'slider_index' not in st.session_state:
            st.session_state.slider_index = 0
            
        col_btn1, col_cnt, col_btn2 = st.columns([1, 2, 1])
        
        with col_btn1:
            if st.button("← ANTERIOR", use_container_width=True):
                st.session_state.slider_index = (st.session_state.slider_index - 1) % len(valid_items)
        with col_cnt:
            st.markdown(f"<h4 style='text-align:center; margin-top:5px; font-family:Lato;'>{st.session_state.slider_index + 1} / {len(valid_items)}</h4>", unsafe_allow_html=True)
        with col_btn2:
            if st.button("SIGUIENTE →", use_container_width=True):
                st.session_state.slider_index = (st.session_state.slider_index + 1) % len(valid_items)

        current_item = valid_items[st.session_state.slider_index]
        current_path = find_asset(current_item)
        frase = frases[st.session_state.slider_index % len(frases)]
        
        st.markdown("<br>", unsafe_allow_html=True)
        _, center_col, _ = st.columns([1, 4, 1])
        with center_col:
            if current_item in ["VIDEO", "VPINICIO"]:
                if current_item == "VIDEO":
                    st.video(current_path, start_time=5)
                else:
                    st.video(current_path, autoplay=True, loop=True, muted=True)
            else:
                st.image(current_path, use_container_width=True)
            st.markdown(f"<p class='frase-poetica'>{frase}</p>", unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown("<br><hr>", unsafe_allow_html=True)
    _, f_col, _ = st.columns([2, 1, 2])
    with f_col:
        if st.button("↑ VOLVER AL INICIO", use_container_width=True):
            st.session_state.page = 'bienvenida'
            st.rerun()
    st.markdown("<p style='text-align:center; font-size:12px; color:#888; margin-top:20px;'>Pijao, Ciudad Sin Prisa. Patrimonio Cafetero de Colombia.</p>", unsafe_allow_html=True)
