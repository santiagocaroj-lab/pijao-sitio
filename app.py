import base64
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
    """Busca un recurso en la carpeta assets independientemente de su extensión y mayúsculas/minúsculas."""
    if not ASSETS_DIR.exists():
        return None

    all_exts = IMAGE_EXTS + VIDEO_EXTS + AUDIO_EXTS
    # Buscar coincidencia exacta o con extensiones permitidas
    for ext in all_exts:
        for path in ASSETS_DIR.glob(f"{name}{ext}"):
            if path.exists():
                return path
        for path in ASSETS_DIR.glob(f"{name.lower()}{ext}"):
            if path.exists():
                return path
        for path in ASSETS_DIR.glob(f"{name.upper()}{ext}"):
            if path.exists():
                return path

    # Búsqueda flexible por si el archivo tiene sufijos
    for path in ASSETS_DIR.iterdir():
        if path.stem.upper() == name.upper():
            return path
    return None


def get_asset_base64(path):
    """Convierte un archivo local a base64 para incrustarlo de manera segura en HTML/JS."""
    if not path or not path.exists():
        return ""
    mime_map = {
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".mov": "video/quicktime",
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
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

# Estilos CSS editoriales, sobrios y cinematográficos (sin estética dashboard)
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #FAF8F5;
        color: #2C2A29;
    }

    /* Ocultar elementos nativos de Streamlit */
    header, footer, [data-testid="stHeader"] {visibility: hidden; display: none;}
    .block-container {padding: 0 !important; max-width: 100% !important;}

    h1, h2, h3, h4, .serif-title {
        font-family: 'Cinzel', serif;
        font-weight: 500;
        color: #1F1E1D;
        letter-spacing: 0.05em;
    }

    /* Contenedor de bienvenida cinematográfica */
    .welcome-container {
        position: relative;
        width: 100vw;
        height: 100vh;
        background-color: #111110;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    .welcome-content {
        position: absolute;
        z-index: 10;
        text-align: center;
        color: #FAF8F5;
        padding: 0 20px;
        transition: opacity 1.5s ease;
    }

    .welcome-title {
        font-family: 'Cinzel', serif;
        font-size: clamp(2.5rem, 5vw, 4.5rem);
        font-weight: 600;
        margin-bottom: 10px;
        letter-spacing: 0.08em;
        text-shadow: 0 4px 20px rgba(0,0,0,0.6);
        animation: fadeIn 2s ease forwards;
    }

    .welcome-subtitle {
        font-size: clamp(1rem, 2vw, 1.3rem);
        font-weight: 300;
        color: #E2DFDB;
        margin-bottom: 30px;
        letter-spacing: 0.04em;
        animation: fadeIn 2.5s ease forwards;
    }

    .editorial-btn {
        background: transparent;
        color: #FAF8F5;
        border: 1px solid rgba(250, 248, 245, 0.6);
        padding: 12px 36px;
        font-family: 'Cinzel', serif;
        font-size: 0.95rem;
        letter-spacing: 0.2em;
        cursor: pointer;
        transition: all 0.4s ease;
        opacity: 0;
        animation: fadeIn 3s ease forwards 1s;
    }

    .editorial-btn:hover {
        background: #FAF8F5;
        color: #1F1E1D;
        border-color: #FAF8F5;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Elemento de video y slideshow de fondo */
    .bg-media-layer {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: 1;
        opacity: 0.8;
    }

    .bg-photo-layer {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-size: cover;
        background-position: center;
        z-index: 2;
        opacity: 0;
        transition: opacity 2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .vignette-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, rgba(17,17,16,0.3) 0%, rgba(17,17,16,0.7) 100%);
        z-index: 3;
    }

    /* Navegación Principal */
    .nav-bar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(250, 248, 245, 0.92);
        backdrop-filter: blur(10px);
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 5%;
        border-bottom: 1px solid rgba(44, 42, 41, 0.08);
    }

    .nav-brand {
        font-family: 'Cinzel', serif;
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: 0.15em;
        color: #1F1E1D;
        text-decoration: none;
    }

    .nav-links {
        display: flex;
        gap: 28px;
        list-style: none;
        margin: 0;
        padding: 0;
    }

    .nav-links a {
        font-size: 0.85rem;
        font-weight: 500;
        color: #5A5652;
        text-decoration: none;
        letter-spacing: 0.05em;
        transition: color 0.3s ease;
    }

    .nav-links a:hover {
        color: #1F1E1D;
    }

    /* Control de Audio Flotante */
    .audio-control-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1100;
    }

    .audio-btn {
        background: rgba(31, 30, 29, 0.85);
        color: #FAF8F5;
        border: 1px solid rgba(250, 248, 245, 0.2);
        padding: 10px 18px;
        border-radius: 30px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 0.1em;
        cursor: pointer;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .audio-btn:hover {
        background: #1F1E1D;
        transform: scale(1.03);
    }

    /* Secciones Editoriales */
    .editorial-section {
        padding: 120px 10% 80px 10%;
        background-color: #FAF8F5;
        border-bottom: 1px solid #EBE7E1;
    }

    .editorial-section.alt {
        background-color: #F2EFE9;
    }

    .section-title {
        font-size: clamp(2rem, 3.5vw, 3rem);
        margin-bottom: 24px;
        color: #1F1E1D;
    }

    .section-subtitle {
        font-family: 'Cinzel', serif;
        font-size: 0.9rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #6B705C;
        margin-bottom: 12px;
    }

    .editorial-text {
        font-size: 1.05rem;
        line-height: 1.8;
        color: #4A4643;
        font-weight: 300;
        margin-bottom: 20px;
    }

    /* Línea de Tiempo */
    .timeline-container {
        position: relative;
        margin-top: 50px;
        padding-left: 30px;
        border-left: 1px solid #D4CE3;
    }

    .timeline-item {
        position: relative;
        margin-bottom: 40px;
    }

    .timeline-item::before {
        content: '';
        position: absolute;
        left: -35.5px;
        top: 6px;
        width: 11px;
        height: 11px;
        border-radius: 50%;
        background: #6B705C;
        border: 2px solid #FAF8F5;
    }

    .timeline-year {
        font-family: 'Cinzel', serif;
        font-size: 1.2rem;
        font-weight: 600;
        color: #1F1E1D;
        margin-bottom: 6px;
    }

    .timeline-desc {
        font-size: 0.95rem;
        color: #5A5652;
        line-height: 1.6;
    }

    /* Categorías Descubre Pijao */
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 30px;
        margin-top: 40px;
    }

    .category-card {
        background: #FAF8F5;
        padding: 40px 30px;
        border: 1px solid #E4E0D8;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .category-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
    }

    .category-title {
        font-family: 'Cinzel', serif;
        font-size: 1.25rem;
        margin-bottom: 15px;
        color: #1F1E1D;
    }

    .category-text {
        font-size: 0.92rem;
        color: #605C58;
        line-height: 1.7;
    }

    /* Recorrido Audiovisual Manual */
    .recorrido-box {
        background: #F2EFE9;
        border: 1px solid #E4E0D8;
        padding: 50px;
        text-align: center;
        margin-top: 40px;
    }

    .recorrido-counter {
        font-family: 'Cinzel', serif;
        font-size: 0.9rem;
        letter-spacing: 0.2em;
        color: #6B705C;
        margin-bottom: 20px;
    }

    .recorrido-phrase {
        font-family: 'Cinzel', serif;
        font-size: 1.3rem;
        color: #1F1E1D;
        margin-bottom: 30px;
        line-height: 1.5;
        font-style: italic;
    }

    .recorrido-nav-btns {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 30px;
    }

    .editorial-link-btn {
        display: inline-block;
        background: #1F1E1D;
        color: #FAF8F5;
        padding: 14px 32px;
        font-family: 'Cinzel', serif;
        font-size: 0.85rem;
        letter-spacing: 0.15em;
        text-decoration: none;
        margin-top: 20px;
        transition: background 0.3s ease;
    }

    .editorial-link-btn:hover {
        background: #4A4643;
        color: #FAF8F5;
    }

    @media(max-width: 768px) {
        .nav-links {display: none;}
        .editorial-section {padding: 90px 6% 60px 6%;}
    }
</style>
""",
    unsafe_allow_html=True,
)

# Inicializar estado de navegación interna si es necesario
if "nav_state" not in st.session_state:
    st.session_state.nav_state = "inicio"

# ----------------------------------------------------
# 1. PÁGINA DE BIENVENIDA — SECUENCIA CINEMATOGRÁFICA
# ----------------------------------------------------
photos_json_keys = list(photos_b64.keys())
photos_json_values = list(photos_b64.values())

photos_js_array = str(photos_json_values).replace("'", '"')

welcome_html = f"""
<div id="welcome-wrapper" class="welcome-container">
    <video id="intro-video" class="bg-media-layer" autoplay muted playsinline>
        <source src="{video_intro_b64}" type="video/mp4">
    </video>
    <div id="photo-bg" class="bg-photo-layer"></div>
    <div class="vignette-overlay"></div>
    
    <div class="welcome-content" id="welcome-content">
        <h1 class="welcome-title">PIJAO, CIUDAD SIN PRISA</h1>
        <p class="welcome-subtitle">Te invitamos a recorrer lento a nuestro municipio</p>
        <button class="editorial-btn" onclick="iniciarTravesia()">INICIAR TRAVESÍA</button>
    </div>
</div>

<script>
    const video = document.getElementById('intro-video');
    const photoBg = document.getElementById('photo-bg');
    const photos = {photos_js_array};
    let photoInterval = null;
    let currentPhotoIdx = 0;

    // Cuando termina el video principal de bienvenida (22s aprox)
    if (video) {{
        video.onended = function() {{
            setTimeout(() => {{
                if (photos.length > 0) {{
                    startPhotoSlideshow();
                }}
            }}, 1000);
        }};
    }}

    function startPhotoSlideshow() {{
        if (photos.length === 0) return;
        
        // Mostrar primera foto
        photoBg.style.backgroundImage = `url('${{photos[currentPhotoIdx]}}')`;
        photoBg.style.opacity = '0.75';
        
        photoInterval = setInterval(() => {{
            currentPhotoIdx = (currentPhotoIdx + 1) % photos.length;
            photoBg.style.opacity = '0';
            setTimeout(() => {{
                photoBg.style.backgroundImage = `url('${{photos[currentPhotoIdx]}}')`;
                photoBg.style.opacity = '0.75';
            }}, 1000); // Duración de transición fade
        }}, 5000); // Cambio cada 5 segundos
    }}

    function iniciarTravesia() {{
        if (photoInterval) clearInterval(photoInterval);
        
        // Reproducir audio M1 si está disponible y activar sonido
        const audioEl = document.getElementById('global-audio-m1');
        if (audioEl) {{
            audioEl.muted = false;
            audioEl.play().catch(e => console.log("Autoplay con interacción habilitado"));
            const audioBtnText = document.getElementById('audio-btn-text');
            if (audioBtnText) audioBtnText.innerText = "◖ SONIDO ACTIVO";
        }}

        // Desplazamiento suave hacia la segunda sección
        const target = document.getElementById('seccion-principal');
        if (target) {{
            target.scrollIntoView({{ behavior: 'smooth' }});
        }}
    }}
</script>
"""

st.markdown(welcome_html, unsafe_allow_html=True)

# ----------------------------------------------------
# CONTROL DE AUDIO REAL M1
# ----------------------------------------------------
audio_html = f"""
<audio id="global-audio-m1" loop autoplay muted>
    <source src="{audio_m1_b64}" type="audio/mpeg">
</audio>

<div class="audio-control-container">
    <button class="audio-btn" onclick="toggleAudio()" id="audio-btn-element">
        <span id="audio-btn-text">◖ QUITAR SONIDO</span>
    </button>
</div>

<script>
    function toggleAudio() {{
        const audio = document.getElementById('global-audio-m1');
        const btnText = document.getElementById('audio-btn-text');
        if (!audio) return;
        
        if (audio.muted) {{
            audio.muted = false;
            audio.play().catch(e => console.log("Play interactivo requerido"));
            btnText.innerText = "◖ QUITAR SONIDO";
        }} else {{
            audio.muted = true;
            btnText.innerText = "◖ ACTIVAR SONIDO";
        }}
    }}
</script>
"""
st.markdown(audio_html, unsafe_allow_html=True)

# ----------------------------------------------------
# NAVEGACIÓN PRINCIPAL FIJA
# ----------------------------------------------------
navbar_html = """
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
<div id="seccion-principal" style="height: 20px;"></div>
"""
st.markdown(navbar_html, unsafe_allow_html=True)

# ----------------------------------------------------
# 2. SEGUNDA PARTE — VPINICIO & INTRODUCCIÓN
# ----------------------------------------------------
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

if vpinicio_path and vpinicio_path.exists():
    st.markdown(
        f"""
    <div style="width: 100%; background: #111110; padding: 40px 0; text-align: center;">
        <div style="max-width: 1100px; margin: 0 auto; padding: 0 20px;">
            <video width="100%" autoplay muted loop playsinline style="border-radius: 4px; box-shadow: 0 20px 40px rgba(0,0,0,0.3);">
                <source src="{vpinicio_b64}" type="video/mp4">
                Tu navegador no soporta video HTML5.
            </video>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ----------------------------------------------------
# 3. SECCIÓN: VIDEO CINEMATOGRÁFICO PRINCIPAL
# ----------------------------------------------------
st.markdown(
    """
<section class="editorial-section alt">
    <div style="max-width: 900px; margin: 0 auto; text-align: center; margin-bottom: 40px;">
        <p class="section-subtitle">Documental y Paisaje</p>
        <h2 class="section-title">El latido de la montaña</h2>
        <p class="editorial-text">
            Una mirada cinematográfica a la cotidianidad, los caminos y el pulso apacible de una comunidad que protege su identidad cultural.
        </p>
    </div>
</section>
""",
    unsafe_allow_html=True,
)

if video_intro_path and video_intro_path.exists():
    st.markdown(
        f"""
    <div style="width: 100%; background: #111110; padding: 20px 0 60px 0; text-align: center;">
        <div style="max-width: 1100px; margin: 0 auto; padding: 0 20px;">
            <video width="100%" controls preload="auto" style="border-radius: 4px; box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
                <source src="{video_intro_b64}" type="video/mp4">
                Tu navegador no soporta video HTML5.
            </video>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ----------------------------------------------------
# 4. CASAS DEL AYER
# ----------------------------------------------------
st.markdown(
    """
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
                <p class="editorial-text">
                    Cada fachada conserva la memoria carpintera de antaño, resistiendo al tiempo sin perder la elegancia 
                    de las formas simples y auténticas del paisaje cultural cafetero.
                </p>
            </div>
""",
    unsafe_allow_html=True,
)

# Mostrar F1 o F3 como ilustración de casas del ayer si existen
casa_img = photos_b64.get("F1") or photos_b64.get("F3")
if casa_img:
    st.markdown(
        f"""
            <div>
                <img src="{casa_img}" alt="Casas del ayer" style="width: 100%; height: auto; border-radius: 2px; box-shadow: 0 15px 35px rgba(0,0,0,0.08); object-fit: cover;">
            </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
        </div>
    </div>
</section>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# 5. HISTORIA DE GUERREROS
# ----------------------------------------------------
st.markdown(
    """
<div id="historia-guerreros"></div>
<section class="editorial-section alt">
    <div style="max-width: 1100px; margin: 0 auto;">
        <div style="max-width: 800px; margin-bottom: 50px;">
            <p class="section-subtitle">Raíces y Profundidad</p>
            <h2 class="section-title">Historia de guerreros</h2>
            <p class="editorial-text">
                El nombre de Pijao evoca a la valerosa estirpe indígena que habitó y defendió estos escarpados territorios 
                de la cordillera central. Más allá de las crónicas de conquista, el espíritu de aquellos pobladores originales 
                pervive en la dignidad cotidiana de sus habitantes actuales, en su vínculo indisoluble con la montaña y en su 
                capacidad de resistencia cultural a través de las décadas.
            </p>
        </div>
""",
    unsafe_allow_html=True,
)

# Galería fotográfica histórica utilizando F2, F5, F6, F16, F17
hist_imgs = [
    photos_b64.get(k) for k in ["F2", "F5", "F6", "F16", "F17"] if k in photos_b64
]
if hist_imgs:
    st.markdown(
        """
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-top: 30px;">
    """,
        unsafe_allow_html=True,
    )
    for img_src in hist_imgs[:4]:
        st.markdown(
            f"""
            <div style="overflow: hidden; border-radius: 2px;">
                <img src="{img_src}" style="width: 100%; height: 260px; object-fit: cover; transition: transform 0.5s ease;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
            </div>
        """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    </div>
</section>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# 6. CONOCE PIJAO
# ----------------------------------------------------
st.markdown(
    """
<div id="conoce-pijao"></div>
<section class="editorial-section">
    <div style="max-width: 1100px; margin: 0 auto;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 60px; align-items: center;">
""",
    unsafe_allow_html=True,
)

f13_img = photos_b64.get("F13")
if f13_img:
    st.markdown(
        f"""
            <div>
                <img src="{f13_img}" alt="Pijao" style="width: 100%; height: auto; border-radius: 2px; box-shadow: 0 15px 35px rgba(0,0,0,0.08); object-fit: cover;">
            </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
            <div>
                <p class="section-subtitle">Destino y Filosofía</p>
                <h2 class="section-title">Conoce Pijao</h2>
                <p class="editorial-text">
                    Ubicado al sur del departamento del Quindío, Pijao es reconocido internacionalmente como el primer municipio 
                    de Suramérica en obtener la certificación <em>Cittaslow</em> (Ciudad Sin Prisa). Aquí se promueve un modelo 
                    de turismo responsable y sostenible que valora la tranquilidad, el comercio local, la gastronomía tradicional 
                    y la preservación del patrimonio natural.
                </p>
                <a href="https://www.youtube.com/watch?v=UPRAk3g7YVg" target="_blank" class="editorial-link-btn">CONOCE MÁS</a>
            </div>
        </div>
    </div>
</section>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# 7. EL TERRITORIO, CLIMA Y UBICACIÓN
# ----------------------------------------------------
st.markdown(
    """
<div id="territorio"></div>
<section class="editorial-section alt">
    <div style="max-width: 1100px; margin: 0 auto;">
        <p class="section-subtitle">Geografía y Entorno</p>
        <h2 class="section-title">El territorio</h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px; margin-top: 40px;">
            <div style="background: #FAF8F5; padding: 35px; border: 1px solid #E4E0D8;">
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.1rem; margin-bottom: 15px; color: #1F1E1D;">Región y Montaña</h3>
                <p class="editorial-text" style="font-size: 0.95rem;">
                    Enclavado en la cordillera Central de la región Andina, el municipio se despliega entre empinadas montañas, 
                    frondosos bosques de niebla y profundos valles labrados por el agua. La topografía define una relación 
                    íntima y respetuosa entre la vida cotidiana y la verticalidad del paisaje.
                </p>
            </div>
            
            <div style="background: #FAF8F5; padding: 35px; border: 1px solid #E4E0D8;">
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.1rem; margin-bottom: 15px; color: #1F1E1D;">Clima</h3>
                <p class="editorial-text" style="font-size: 0.95rem;">
                    Las condiciones atmosféricas están marcadas por una precipitación superior a 2400 mm en zonas montañosas 
                    y aproximadamente 1800 mm anuales en otras zonas señaladas. Durante el día, constantes vientos fluyen 
                    desde el valle del río Cauca hacia la imponente montaña.
                </p>
            </div>
            
            <div style="background: #FAF8F5; padding: 35px; border: 1px solid #E4E0D8;">
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.1rem; margin-bottom: 15px; color: #1F1E1D;">Límites Geográficos</h3>
                <p class="editorial-text" style="font-size: 0.95rem;">
                    Limita por el norte con Córdoba, por el este con Tolima, por el sur con Génova, por el oeste con el Valle del Cauca, 
                    y por el noroeste con Buenavista. Un cruce de caminos cordilleranos cargados de historia y biodiversidad.
                </p>
            </div>
        </div>
    </div>
</section>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# 8. HISTORIA — LÍNEA DE TIEMPO
# ----------------------------------------------------
st.markdown(
    """
<section class="editorial-section">
    <div style="max-width: 900px; margin: 0 auto;">
        <p class="section-subtitle">Cronología</p>
        <h2 class="section-title">Hitos históricos</h2>
        
        <div class="timeline-container">
            <div class="timeline-item">
                <div class="timeline-year">1902</div>
                <div class="timeline-desc">Fundación y establecimiento inicial bajo el nombre de San José de Colón.</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">1905</div>
                <div class="timeline-desc">Erección como corregimiento adscrito al municipio de Calarcá.</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">1912</div>
                <div class="timeline-desc">Constitución oficial como parroquia eclesiástica.</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">1926</div>
                <div class="timeline-desc">Elevación a la categoría de municipio, consolidando su autonomía administrativa.</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">1931</div>
                <div class="timeline-desc">Adopción definitiva del nombre de Pijao en honor a los antiguos pobladores indígenas.</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">2014</div>
                <div class="timeline-desc">Reconocimiento internacional como miembro de la red Cittaslow / Ciudad Sin Prisa.</div>
            </div>
        </div>
    </div>
</section>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# 9. DESCUBRE PIJAO — CATEGORÍAS EDITORIALES
# ----------------------------------------------------
st.markdown(
    """
<div id="descubre-pijao"></div>
<section class="editorial-section alt">
    <div style="max-width: 1100px; margin: 0 auto;">
        <p class="section-subtitle">Ejes Temáticos</p>
        <h2 class="section-title">Descubre Pijao</h2>
        <p class="editorial-text">
            Seis dimensiones para comprender la esencia de un territorio que ha decidido conservar su ritmo natural y su dignidad cultural.
        </p>
        
        <div class="category-grid">
            <div class="category-card">
                <h3 class="category-title">Arquitectura</h3>
                <p class="category-text">Balcones tallados, bahareque artesanal y colores vivos que narran la maestría constructiva de la colonización.</p>
            </div>
            <div class="category-card">
                <h3 class="category-title">Naturaleza</h3>
                <p class="category-text">Bosques de niebla, fuentes hídricas prístinas y una biodiversidad cordillerana que abruma por su suntuosidad.</p>
            </div>
            <div class="category-card">
                <h3 class="category-title">Cultura</h3>
                <p class="category-text">Tradiciones orales, saberes campesinos y un profundo sentido de comunidad arraigado en la montaña.</p>
            </div>
            <div class="category-card">
                <h3 class="category-title">Café</h3>
                <p class="category-text">Cultura cafetera auténtica, donde cada grano refleja el cuidado meticuloso de los suelos volcánicos andinos.</p>
            </div>
            <div class="category-card">
                <h3 class="category-title">Patrimonio</h3>
                <p class="category-text">Legado histórico resguardado en cada esquina, en la plaza principal y en la memoria viva de sus habitantes.</p>
            </div>
            <div class="category-card">
                <h3 class="category-title">Rutas y experiencias</h3>
                <p class="category-text">Caminos reales y senderos lentos diseñados para ser recorridos a pie, observando sin prisa.</p>
            </div>
        </div>
    </div>
</section>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# 10. RECORRIDO AUDIOVISUAL (MANUAL)
# ----------------------------------------------------
recorrido_items = [f"F{i}" for i in range(1, 19)]
if vpinicio_path:
    recorrido_items.append("VPINICIO")
if video_intro_path:
    recorrido_items.append("VIDEO")

frases_poeticas = [
    "En Pijao, el tiempo también hace parte del paisaje.",
    "Cada rincón guarda una historia que merece ser recorrida sin prisa.",
    "Aquí la vida conserva el ritmo de las cosas hechas con tiempo.",
    "Entre montañas, memoria y caminos, Pijao invita a mirar de otra manera.",
    "Hay lugares que no se visitan solamente: se viven.",
    "La identidad de un pueblo también vive en sus pequeños momentos.",
    "Pijao es territorio de memoria, paisaje y encuentro.",
    "Caminar despacio también es una forma de conocer.",
    "La quietud de las cumbres abriga la calidez de su gente.",
    "Bajo los aleros de madera se teje la historia cotidiana del Quindío.",
    "El verde profundo de la cordillera abraza las casas de antaño.",
    "Detenerse a observar es el primer paso para descubrir.",
    "Un refugio donde el futuro aún respira al ritmo del pasado.",
    "Las manos que cultivan la tierra también custodian la memoria.",
    "A través de los caminos de herradura pervive el pulso de la historia.",
    "El silencio de las montañas guarda las respuestas más sinceras.",
    "Pijao enseña que la belleza habita en lo esencial y pausado.",
    "Aprender a caminar sin prisa es volver a sintonizar con la tierra.",
]

if "recorrido_idx" not in st.session_state:
    st.session_state.recorrido_idx = 0

total_recorrido = len(recorrido_items)

st.markdown(
    """
<div id="recorrido-audiovisual"></div>
<section class="editorial-section">
    <div style="max-width: 900px; margin: 0 auto;">
        <p class="section-subtitle" style="text-align: center;">Inmersión Visual</p>
        <h2 class="section-title" style="text-align: center;">Recorrido audiovisual</h2>
        <p class="editorial-text" style="text-align: center; margin-bottom: 40px;">
            Explore de manera manual esta selección de registros fotográficos y cinematográficos que capturan la atmósfera inalterable de Pijao.
        </p>
    </div>
""",
    unsafe_allow_html=True,
)

current_item_key = recorrido_items[st.session_state.recorrido_idx]
current_phrase = frases_poeticas[
    st.session_state.recorrido_idx % len(frases_poeticas)
]
current_counter = f"{st.session_state.recorrido_idx + 1:02d} / {total_recorrido:02d}"

st.markdown(
    f"""
<div style="max-width: 900px; margin: 0 auto;" class="recorrido-box">
    <div class="recorrido-counter">{current_counter}</div>
    <div class="recorrido-phrase">"{current_phrase}"</div>
""",
    unsafe_allow_html=True,
)

# Renderizar elemento actual (Foto o Video)
if current_item_key.startswith("F"):
    img_b64 = photos_b64.get(current_item_key)
    if img_b64:
        st.markdown(
            f'<div style="margin: 20px 0;"><img src="{img_b64}" style="width: 100%; max-height: 550px; object-fit: contain; border-radius: 2px;"></div>',
            unsafe_allow_html=True,
        )
    else:
        st.info(f"Recurso {current_item_key} no disponible en la carpeta assets.")
elif current_item_key == "VPINICIO" and vpinicio_b64:
    st.markdown(
        f'<div style="margin: 20px 0;"><video width="100%" controls autoplay muted loop playsinline style="border-radius: 2px;"><source src="{vpinicio_b64}" type="video/mp4"></video></div>',
        unsafe_allow_html=True,
    )
elif current_item_key == "VIDEO" and video_intro_b64:
    st.markdown(
        f'<div style="margin: 20px 0;"><video width="100%" controls preload="auto" style="border-radius: 2px;"><source src="{video_intro_b64}" type="video/mp4"></video></div>',
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# Botones de navegación manual anterior / siguiente
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("← ANTERIOR", use_container_width=True):
        st.session_state.recorrido_idx = (
            st.session_state.recorrido_idx - 1
        ) % total_recorrido
        st.rerun()

with col3:
    if st.button("SIGUIENTE →", use_container_width=True):
        st.session_state.recorrido_idx = (
            st.session_state.recorrido_idx + 1
        ) % total_recorrido
        st.rerun()

st.markdown("</section>", unsafe_allow_html=True)

# ----------------------------------------------------
# 11. VOLVER AL INICIO Y PIE DE PÁGINA
# ----------------------------------------------------
st.markdown(
    """
<section style="padding: 60px 10%; background-color: #1F1E1D; color: #FAF8F5; text-align: center;">
    <div style="max-width: 800px; margin: 0 auto;">
        <h3 style="font-family: 'Cinzel', serif; font-size: 1.5rem; margin-bottom: 20px; letter-spacing: 0.1em;">PIJAO, CIUDAD SIN PRISA</h3>
        <p style="font-size: 0.9rem; color: #B5B0A8; line-height: 1.6; margin-bottom: 30px; font-weight: 300;">
            Proyecto cultural, patrimonial y audiovisual dedicado a preservar la memoria y el ritmo pausado de la montaña quindiana.
        </p>
        <a href="#seccion-principal" class="editorial-link-btn" style="background: #FAF8F5; color: #1F1E1D;">VOLVER AL INICIO</a>
    </div>
</section>
""",
    unsafe_allow_html=True,
)
