import base64
import time
from pathlib import Path
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Pijao, Ciudad Sin Prisa",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Directorios de recursos
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# Extensiones permitidas
IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".webp"]
VIDEO_EXTS = [".mp4", ".webm", ".mov"]
AUDIO_EXTS = [".mp3", ".wav", ".ogg"]

def find_asset(name):
    """Busca un recurso en la carpeta assets independientemente de su extensión."""
    if not ASSETS_DIR.exists():
        return None

    all_exts = IMAGE_EXTS + VIDEO_EXTS + AUDIO_EXTS
    for ext in all_exts:
        for path in ASSETS_DIR.glob(f"{name}{ext}"):
            if path.exists(): return path
        for path in ASSETS_DIR.glob(f"{name.lower()}{ext}"):
            if path.exists(): return path
        for path in ASSETS_DIR.glob(f"{name.upper()}{ext}"):
            if path.exists(): return path

    for path in ASSETS_DIR.iterdir():
        if path.stem.upper() == name.upper():
            return path
    return None

def get_asset_base64(path):
    """Convierte un archivo local a base64 para incrustarlo de manera segura en HTML/JS."""
    if not path or not path.exists():
        return ""
    mime_map = {
        ".mp4": "video/mp4", ".webm": "video/webm", ".mov": "video/quicktime",
        ".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg",
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp",
    }
    mime = mime_map.get(path.suffix.lower(), "application/octet-stream")
    b64_data = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{b64_data}"

# Cargar rutas de recursos clave
video_intro_path = find_asset("VIDEO")
vpinicio_path = find_asset("VPINICIO")
audio_m1_path = find_asset("M1")

video_intro_b64 = get_asset_base64(video_intro_path) if video_intro_path else ""
vpinicio_b64 = get_asset_base64(vpinicio_path) if vpinicio_path else ""
audio_m1_b64 = get_asset_base64(audio_m1_path) if audio_m1_path else ""

# Cargar colección de fotografías F1–F18
photos_b64 = {}
for i in range(1, 19):
    p = find_asset(f"F{i}")
    if p:
        photos_b64[f"F{i}"] = get_asset_base64(p)


# INICIALIZACIÓN DE ESTADOS
if "nav_state" not in st.session_state:
    st.session_state.nav_state = "inicio"
if "recorrido_idx" not in st.session_state:
    st.session_state.recorrido_idx = 0


# ESTILOS GLOBALES
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #FAF8F5;
    color: #2C2A29;
}
header, footer, [data-testid="stHeader"] {visibility: hidden; display: none !important;}
.block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
[data-testid="stAppViewContainer"] {padding-top: 0 !important;}
h1, h2, h3, h4, .serif-title {
    font-family: 'Cinzel', serif;
    font-weight: 500;
    color: #1F1E1D;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# PÁGINA 1: BIENVENIDA
# ==========================================
if st.session_state.nav_state == "inicio":
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .welcome-wrapper {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #111110; z-index: 10;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .bg-media-layer {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        object-fit: cover; z-index: 1; opacity: 0.8;
    }
    .vignette-overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(180deg, rgba(17,17,16,0.3) 0%, rgba(17,17,16,0.7) 100%);
        z-index: 2;
    }
    .welcome-content {
        position: relative; z-index: 3; text-align: center; color: #FAF8F5;
        margin-bottom: 80px;
    }
    .welcome-title {
        font-family: 'Cinzel', serif; font-size: clamp(2.5rem, 5vw, 4.5rem);
        font-weight: 600; margin-bottom: 10px; letter-spacing: 0.08em;
        text-shadow: 0 4px 20px rgba(0,0,0,0.6);
        opacity: 0; animation: fadeIn 2s ease forwards;
    }
    .welcome-subtitle {
        font-size: clamp(1rem, 2vw, 1.3rem); font-weight: 300; color: #E2DFDB;
        letter-spacing: 0.04em;
        opacity: 0; animation: fadeIn 2.5s ease forwards 0.5s;
    }
    div[data-testid="stButton"] {
        position: fixed !important; 
        top: 65% !important; 
        left: 50% !important; 
        transform: translateX(-50%) !important;
        z-index: 20 !important; 
        opacity: 0; 
        animation: fadeIn 3s ease forwards 1s;
        width: auto !important;
        display: flex;
        justify-content: center;
    }
    div[data-testid="stButton"] button {
        background: rgba(250, 248, 245, 0.1) !important;
        color: #FAF8F5 !important;
        border: 2px solid rgba(250, 248, 245, 0.8) !important;
        padding: 15px 40px !important;
        font-family: 'Cinzel', serif !important;
        font-size: 1.1rem !important; font-weight: 600 !important;
        letter-spacing: 0.2em !important; border-radius: 0 !important;
        transition: all 0.4s ease !important;
        white-space: nowrap !important;
    }
    div[data-testid="stButton"] button:hover {
        background: #FAF8F5 !important; color: #1F1E1D !important;
        transform: scale(1.05) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="welcome-wrapper">
        <video class="bg-media-layer" autoplay muted loop playsinline>
            <source src="{video_intro_b64}" type="video/mp4">
        </video>
        <div class="vignette-overlay"></div>
        <div class="welcome-content">
            <h1 class="welcome-title">PIJAO, CIUDAD SIN PRISA</h1>
            <p class="welcome-subtitle">Te invitamos a recorrer lento a nuestro municipio</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("INICIAR TRAVESÍA"):
        st.session_state.nav_state = "carga"
        st.rerun()

# ==========================================
# PÁGINA 1.5: PANTALLA DE CARGA FALSA
# ==========================================
elif st.session_state.nav_state == "carga":
    pantalla_carga = st.empty()
    pantalla_carga.markdown("""
    <style>
    .loading-wrapper {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #111110; z-index: 9999;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        color: #FAF8F5; font-family: 'Cinzel', serif;
    }
    .loading-text {
        font-size: 1.3rem; letter-spacing: 0.25em; margin-bottom: 25px;
        animation: pulse 1.5s infinite;
    }
    .loading-bar-container {
        width: 250px; height: 2px; background: rgba(250, 248, 245, 0.15);
        overflow: hidden; border-radius: 2px;
    }
    .loading-bar {
        width: 0%; height: 100%; background: #FAF8F5;
        animation: fillBar 2.5s ease forwards;
    }
    @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
    @keyframes fillBar { 0% { width: 0%; } 100% { width: 100%; } }
    </style>
    <div class="loading-wrapper">
        <div class="loading-text">LLEGANDO A LA MONTAÑA</div>
        <div class="loading-bar-container"><div class="loading-bar"></div></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detenemos la ejecución 2.5 segundos para que se vea la animación y se limpie la vista
    time.sleep(2.5)
    st.session_state.nav_state = "desarrollo"
    st.rerun()


# ==========================================
# PÁGINA 2: DESARROLLO
# ==========================================
elif st.session_state.nav_state == "desarrollo":
    
    st.markdown("""
    <style>
    .nav-bar {
        position: fixed; top: 0; left: 0; width: 100%;
        background: rgba(250, 248, 245, 0.95); backdrop-filter: blur(10px);
        z-index: 1000; display: flex; justify-content: space-between;
        align-items: center; padding: 18px 5%; border-bottom: 1px solid rgba(44, 42, 41, 0.1);
    }
    .nav-brand {
        font-family: 'Cinzel', serif; font-weight: 600; font-size: 1.1rem;
        letter-spacing: 0.15em; color: #1F1E1D; text-decoration: none;
    }
    .nav-links {
        display: flex; gap: 28px; list-style: none; margin: 0; padding: 0;
    }
    .nav-links a {
        font-size: 0.85rem; font-weight: 600; color: #5A5652;
        text-decoration: none; letter-spacing: 0.05em; transition: color 0.3s ease;
    }
    .nav-links a:hover { color: #1F1E1D; }
    
    .audio-control-container {
        position: fixed; bottom: 40px; right: 40px; z-index: 1100;
    }
    .audio-btn {
        display: inline-block; background: #1F1E1D; color: #FAF8F5; border: 2px solid #FAF8F5;
        padding: 12px 24px; border-radius: 50px; font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.95rem; font-weight: 600; letter-spacing: 0.1em;
        cursor: pointer; backdrop-filter: blur(5px); transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4); user-select: none;
    }
    .audio-btn:hover {
        background: #FAF8F5; color: #1F1E1D; border-color: #1F1E1D; transform: scale(1.05);
    }
    
    .editorial-section {
        padding: 100px 10% 80px 10%; background-color: #FAF8F5; border-bottom: 1px solid #EBE7E1;
    }
    .editorial-section.alt { background-color: #F2EFE9; }
    .section-title { font-size: clamp(2rem, 3.5vw, 3rem); margin-bottom: 24px; color: #1F1E1D; }
    .section-subtitle {
        font-family: 'Cinzel', serif; font-size: 0.9rem; letter-spacing: 0.2em;
        text-transform: uppercase; color: #6B705C; margin-bottom: 12px;
    }
    .editorial-text {
        font-size: 1.05rem; line-height: 1.8; color: #4A4643; font-weight: 300; margin-bottom: 20px;
    }
    
    .category-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 30px; margin-top: 40px;
    }
    .category-card {
        background: #FAF8F5; padding: 40px 30px; border: 1px solid #E4E0D8;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .category-card:hover { transform: translateY(-4px); box-shadow: 0 10px 30px rgba(0,0,0,0.04); }
    
    .recorrido-box {
        background: #F2EFE9; border: 1px solid #E4E0D8; padding: 50px;
        text-align: center; margin-top: 40px;
    }
    
    div[data-testid="stButton"] button {
        background-color: #1F1E1D !important; color: #FAF8F5 !important;
        border: 1px solid #1F1E1D !important; border-radius: 2px !important;
        font-family: 'Cinzel', serif !important; letter-spacing: 0.1em !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #FAF8F5 !important; color: #1F1E1D !important; border-color: #1F1E1D !important;
    }

    @media(max-width: 768px) {
        .nav-links {display: none;}
        .editorial-section {padding: 90px 6% 60px 6%;}
    }
    </style>
    """, unsafe_allow_html=True)

    # 1. CONTROL DE AUDIO (CORREGIDO CON TRUCO DE ONERROR PARA STREAMLIT)
    audio_html = f"""
    <audio id="global-audio-m1" loop autoplay>
        <source src="{audio_m1_b64}" type="audio/mpeg">
    </audio>
    <div class="audio-control-container">
        <label class="audio-btn">
            <input type="checkbox" id="audio-toggle" style="display:none;" checked>
            <span id="audio-btn-text">◖ QUITAR SONIDO</span>
        </label>
    </div>
    <!-- Inyección JS segura en Streamlit mediante onerror -->
    <img src="dummy.png" style="display:none;" onerror="
        var toggle = document.getElementById('audio-toggle');
        var audio = document.getElementById('global-audio-m1');
        var text = document.getElementById('audio-btn-text');
        if(toggle && audio && text) {{
            toggle.addEventListener('change', function(e) {{
                if(e.target.checked) {{
                    audio.play();
                    text.innerText = '◖ QUITAR SONIDO';
                }} else {{
                    audio.pause();
                    text.innerText = '◖ ACTIVAR SONIDO';
                }}
            }});
        }}
    ">
    """
    st.markdown(audio_html, unsafe_allow_html=True)

    # 2. NAVEGACIÓN PRINCIPAL
    st.markdown("""
    <nav class="nav-bar">
        <a href="#seccion-principal" class="nav-brand">PIJAO</a>
        <ul class="nav-links">
            <li><a href="#casas-ayer">Casas del ayer</a></li>
            <li><a href="#historia-guerreros">Historia</a></li>
            <li><a href="#conoce-pijao">Conoce Pijao</a></li>
            <li><a href="#territorio">Territorio</a></li>
            <li><a href="#descubre-pijao">Descubre Pijao</a></li>
            <li><a href="#recorrido-audiovisual">Recorrido audiovisual</a></li>
        </ul>
    </nav>
    <div id="seccion-principal" style="height: 60px;"></div>
    """, unsafe_allow_html=True)

    # 3. INTRODUCCIÓN
    st.markdown("""
    <section class="editorial-section">
        <div style="max-width: 900px; margin: 0 auto; text-align: center;">
            <p class="section-subtitle">Territorio y Memoria</p>
            <h2 class="section-title">Una experiencia sin prisa</h2>
            <p class="editorial-text">
                Pijao es un refugio en la Cordillera Central de los Andes colombianos donde el tiempo adquiere otra dimensión. 
                Lejos del vértigo contemporáneo, este municipio invita a caminar lento, a observar los detalles de su arquitectura 
                en bahareque y madera, y a escuchar las conversaciones en la plaza principal frente a una taza de café cultivado 
                con respeto por la tierra.
            </p>
        </div>
    </section>
    """, unsafe_allow_html=True)

    if vpinicio_path and vpinicio_path.exists():
        st.markdown(f"""
        <div style="width: 100%; padding: 40px 0; text-align: center; background: transparent;">
            <div style="max-width: 1100px; margin: 0 auto; padding: 0 20px;">
                <video width="100%" autoplay muted loop playsinline style="border-radius: 4px; box-shadow: 0 20px 40px rgba(0,0,0,0.3);">
                    <source src="{vpinicio_b64}" type="video/mp4">
                </video>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 4. VIDEO CINEMATOGRÁFICO PRINCIPAL
    st.markdown("""
    <section class="editorial-section alt">
        <div style="max-width: 900px; margin: 0 auto; text-align: center; margin-bottom: 40px;">
            <p class="section-subtitle">Documental y Paisaje</p>
            <h2 class="section-title">El latido de la montaña</h2>
            <p class="editorial-text">
                Una mirada cinematográfica a la cotidianidad, los caminos y el pulso apacible de una comunidad que protege su identidad cultural.
            </p>
        </div>
    </section>
    """, unsafe_allow_html=True)

    if video_intro_path and video_intro_path.exists():
        st.markdown(f"""
        <div style="width: 100%; padding: 20px 0 60px 0; text-align: center; background: transparent;">
            <div style="max-width: 1100px; margin: 0 auto; padding: 0 20px;">
                <video width="100%" controls preload="auto" style="border-radius: 4px; box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
                    <source src="{video_intro_b64}" type="video/mp4">
                </video>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 5. CASAS DEL AYER
    st.markdown("""
    <div id="casas-ayer"></div>
    <section class="editorial-section">
        <div style="max-width: 1100px; margin: 0 auto;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 60px; align-items: center;">
                <div>
                    <p class="section-subtitle">Patrimonio Arquitectónico</p>
                    <h2 class="section-title">Casas del ayer</h2>
                    <p class="editorial-text">
                        La arquitectura tradicional de Pijao es un testimonio vivo de la colonización antioqueña y la maestría 
                        en el uso del bahareque, la guadua y la madera. Sus viviendas exhiben coloridos balcones florecidos, 
                        aleros generosos diseñados para proteger las paredes de las lluvias cordilleranas y zaguanes que conectan 
                        la intimidad del hogar con la vida apacible de la calle.
                    </p>
                </div>
    """, unsafe_allow_html=True)

    casa_img = photos_b64.get("F1") or photos_b64.get("F3")
    if casa_img:
        st.markdown(f"""
                <div>
                    <img src="{casa_img}" style="width: 100%; border-radius: 2px; box-shadow: 0 15px 35px rgba(0,0,0,0.08); object-fit: cover;">
                </div>
        """, unsafe_allow_html=True)

    st.markdown("""
            </div>
        </div>
    </section>
    """, unsafe_allow_html=True)

    # 6. HISTORIA DE GUERREROS
    st.markdown("""
    <div id="historia-guerreros"></div>
    <section class="editorial-section alt">
        <div style="max-width: 1100px; margin: 0 auto;">
            <div style="max-width: 800px; margin-bottom: 50px;">
                <p class="section-subtitle">Raíces y Profundidad</p>
                <h2 class="section-title">Historia de guerreros</h2>
                <p class="editorial-text">
                    El nombre de Pijao evoca a la valerosa estirpe indígena que habitó y defendió estos escarpados territorios.
                    Más allá de las crónicas de conquista, el espíritu de aquellos pobladores originales pervive en la dignidad 
                    cotidiana de sus habitantes actuales y en su capacidad de resistencia cultural.
                </p>
            </div>
    """, unsafe_allow_html=True)

    hist_imgs = [photos_b64.get(k) for k in ["F2", "F5", "F6", "F16"] if k in photos_b64]
    if hist_imgs:
        st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-top: 30px;">', unsafe_allow_html=True)
        for img_src in hist_imgs:
            st.markdown(f'<div style="overflow: hidden; border-radius: 2px;"><img src="{img_src}" style="width: 100%; height: 260px; object-fit: cover; transition: transform 0.5s ease;" onmouseover="this.style.transform=\'scale(1.03)\'" onmouseout="this.style.transform=\'scale(1)\'"></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div></section>", unsafe_allow_html=True)

    # 7. EL TERRITORIO
    st.markdown("""
    <div id="territorio"></div>
    <section class="editorial-section">
        <div style="max-width: 1100px; margin: 0 auto;">
            <p class="section-subtitle">Geografía y Entorno</p>
            <h2 class="section-title">El territorio</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px; margin-top: 40px;">
                <div style="background: #FAF8F5; padding: 35px; border: 1px solid #E4E0D8;">
                    <h3 style="font-family: 'Cinzel', serif; font-size: 1.1rem; margin-bottom: 15px; color: #1F1E1D;">Región y Montaña</h3>
                    <p class="editorial-text" style="font-size: 0.95rem;">Enclavado en la cordillera Central de la región Andina, el municipio se despliega entre empinadas montañas, frondosos bosques de niebla y profundos valles.</p>
                </div>
                <div style="background: #FAF8F5; padding: 35px; border: 1px solid #E4E0D8;">
                    <h3 style="font-family: 'Cinzel', serif; font-size: 1.1rem; margin-bottom: 15px; color: #1F1E1D;">Clima</h3>
                    <p class="editorial-text" style="font-size: 0.95rem;">Las condiciones atmosféricas están marcadas por una precipitación superior a 2400 mm en zonas montañosas y vientos constantes.</p>
                </div>
                <div style="background: #FAF8F5; padding: 35px; border: 1px solid #E4E0D8;">
                    <h3 style="font-family: 'Cinzel', serif; font-size: 1.1rem; margin-bottom: 15px; color: #1F1E1D;">Límites</h3>
                    <p class="editorial-text" style="font-size: 0.95rem;">Limita por el norte con Córdoba, por el este con Tolima, por el sur con Génova, por el oeste con el Valle del Cauca, y por el noroeste con Buenavista.</p>
                </div>
            </div>
        </div>
    </section>
    """, unsafe_allow_html=True)

    # 8. DESCUBRE PIJAO
    st.markdown("""
    <div id="descubre-pijao"></div>
    <section class="editorial-section alt">
        <div style="max-width: 1100px; margin: 0 auto;">
            <p class="section-subtitle">Ejes Temáticos</p>
            <h2 class="section-title">Descubre Pijao</h2>
            <div class="category-grid">
                <div class="category-card"><h3 style="font-family: 'Cinzel', serif;">Arquitectura</h3><p>Balcones tallados y bahareque artesanal.</p></div>
                <div class="category-card"><h3 style="font-family: 'Cinzel', serif;">Naturaleza</h3><p>Bosques de niebla y biodiversidad cordillerana.</p></div>
                <div class="category-card"><h3 style="font-family: 'Cinzel', serif;">Cultura</h3><p>Tradiciones orales y un profundo sentido de comunidad.</p></div>
                <div class="category-card"><h3 style="font-family: 'Cinzel', serif;">Café</h3><p>Cultura cafetera cuidada en suelos volcánicos.</p></div>
            </div>
        </div>
    </section>
    """, unsafe_allow_html=True)

    # 9. RECORRIDO AUDIOVISUAL
    recorrido_items = [f"F{i}" for i in range(1, 19)]
    if vpinicio_path: recorrido_items.append("VPINICIO")
    if video_intro_path: recorrido_items.append("VIDEO")

    frases_poeticas = [
        "En Pijao, el tiempo también hace parte del paisaje.",
        "Cada rincón guarda una historia que merece ser recorrida sin prisa.",
        "Aquí la vida conserva el ritmo de las cosas hechas con tiempo.",
        "Entre montañas, memoria y caminos, Pijao invita a mirar de otra manera.",
        "Hay lugares que no se visitan solamente: se viven.",
    ]

    total_recorrido = len(recorrido_items)

    st.markdown("""
    <div id="recorrido-audiovisual"></div>
    <section class="editorial-section">
        <div style="max-width: 900px; margin: 0 auto; text-align: center;">
            <p class="section-subtitle">Inmersión Visual</p>
            <h2 class="section-title">Recorrido audiovisual</h2>
        </div>
    """, unsafe_allow_html=True)

    current_item_key = recorrido_items[st.session_state.recorrido_idx]
    current_phrase = frases_poeticas[st.session_state.recorrido_idx % len(frases_poeticas)]

    st.markdown(f"""
    <div style="max-width: 900px; margin: 0 auto;" class="recorrido-box">
        <div style="font-family: 'Cinzel', serif; color: #6B705C; margin-bottom: 20px;">{st.session_state.recorrido_idx + 1:02d} / {total_recorrido:02d}</div>
        <div style="font-family: 'Cinzel', serif; font-size: 1.3rem; margin-bottom: 30px; font-style: italic;">"{current_phrase}"</div>
    """, unsafe_allow_html=True)

    if current_item_key.startswith("F"):
        img_b64 = photos_b64.get(current_item_key)
        if img_b64: st.markdown(f'<img src="{img_b64}" style="width: 100%; max-height: 550px; object-fit: contain;">', unsafe_allow_html=True)
    elif current_item_key == "VPINICIO" and vpinicio_b64:
        st.markdown(f'<video width="100%" controls autoplay muted loop playsinline><source src="{vpinicio_b64}" type="video/mp4"></video>', unsafe_allow_html=True)
    elif current_item_key == "VIDEO" and video_intro_b64:
        st.markdown(f'<video width="100%" controls preload="auto"><source src="{video_intro_b64}" type="video/mp4"></video>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← ANTERIOR", use_container_width=True):
            st.session_state.recorrido_idx = (st.session_state.recorrido_idx - 1) % total_recorrido
            st.rerun()
    with col3:
        if st.button("SIGUIENTE →", use_container_width=True):
            st.session_state.recorrido_idx = (st.session_state.recorrido_idx + 1) % total_recorrido
            st.rerun()
    st.markdown("</section>", unsafe_allow_html=True)

    # 10. FOOTER
    st.markdown("""
    <section style="padding: 60px 10%; background-color: #1F1E1D; color: #FAF8F5; text-align: center;">
        <h3 style="font-family: 'Cinzel', serif; font-size: 1.5rem; margin-bottom: 20px;">PIJAO, CIUDAD SIN PRISA</h3>
    </section>
    """, unsafe_allow_html=True)
