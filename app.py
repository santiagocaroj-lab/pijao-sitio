import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Pijao, Ciudad Sin Prisa",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# BUSCADOR DE RECURSOS ROBUSTO
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

def find_asset(name):
    """Localiza el archivo ignorando mayúsculas/minúsculas y su extensión."""
    if not ASSETS_DIR.exists():
        return None
    for f in ASSETS_DIR.iterdir():
        if f.is_file() and f.stem.lower() == name.lower():
            return str(f)
    return None

# ==========================================
# ESTILOS CSS GLOBALES (ESTÉTICA EDITORIAL)
# ==========================================
st.markdown("""
<style>
    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
        background-color: #f7f5f0;
    }
    
    /* Tipografía y colores de la paleta */
    html, body, .stApp {
        background-color: #f7f5f0;
        color: #2c3e2e;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        scroll-behavior: smooth;
    }
    h1, h2, h3, h4, h5 {
        font-family: 'Georgia', serif;
        color: #3b2f2f;
        font-weight: normal;
    }
    p {
        line-height: 1.8;
        font-size: 1.1rem;
        color: #3e3a35;
    }
    
    /* Animaciones CSS de Bienvenida */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .title-fade { animation: fadeIn 2s ease forwards; opacity: 0; animation-delay: 0.5s; }
    .subtitle-fade { animation: fadeIn 2s ease forwards; opacity: 0; animation-delay: 1.5s; }
    .btn-fade { animation: fadeIn 2s ease forwards; opacity: 0; animation-delay: 4.5s; }
    
    /* Navbar Fija */
    #main-nav {
        position: sticky;
        top: 0;
        width: 100%;
        background: rgba(247, 245, 240, 0.95);
        z-index: 100;
        padding: 20px 0;
        border-bottom: 1px solid #e3dec9;
        display: flex;
        justify-content: center;
        gap: 30px;
        flex-wrap: wrap;
        backdrop-filter: blur(5px);
    }
    #main-nav a {
        text-decoration: none;
        color: #3b2f2f;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: color 0.3s;
    }
    #main-nav a:hover {
        color: #4a6741;
    }

    /* Secciones editoriales */
    .editorial-section {
        max-width: 900px;
        margin: 0 auto;
        padding: 80px 20px;
        text-align: center;
    }
    
    /* Botón flotante de audio */
    #audio-control {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: #3b2f2f;
        color: #f7f5f0;
        padding: 12px 20px;
        border-radius: 50px;
        cursor: pointer;
        z-index: 1000;
        font-family: sans-serif;
        font-size: 0.85rem;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 10px;
        transition: transform 0.3s ease, background 0.3s ease;
    }
    #audio-control:hover {
        transform: scale(1.05);
        background: #4a6741;
    }
    
    /* Botón YT y general */
    .btn-outline {
        display: inline-block;
        margin-top: 20px;
        padding: 12px 25px;
        border: 1px solid #3b2f2f;
        color: #3b2f2f !important;
        text-decoration: none;
        font-family: sans-serif;
        letter-spacing: 1px;
        transition: all 0.3s;
    }
    .btn-outline:hover {
        background: #3b2f2f;
        color: #f7f5f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. CARGA INVISIBLE DE RECURSOS PARA JS
# ==========================================
st.markdown('<div id="hidden-loaders" style="display:none;">', unsafe_allow_html=True)
for i in range(1, 19):
    p = find_asset(f"F{i}")
    if p: st.image(p)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div id="audio-container" style="display:none;">', unsafe_allow_html=True)
m1 = find_asset("M1")
if m1: st.audio(m1, format="audio/mp3")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div id="video-loader" style="display:none;">', unsafe_allow_html=True)
vid = find_asset("VIDEO")
if vid: st.video(vid)
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 2. PANTALLA DE BIENVENIDA (Fase 1)
# ==========================================
st.markdown('''
<div id="welcome-screen" style="position: relative; height: 100vh; width: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background: #000; overflow: hidden; color: #f7f5f0;">
    <div id="welcome-background" style="position: absolute; top:0; left:0; width:100%; height:100%; z-index:1; opacity: 0; transition: opacity 2s ease;"></div>
    <div id="welcome-overlay" style="position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); z-index:2;"></div>
    <div id="welcome-content" style="z-index:3; text-align: center; padding: 20px;">
        <h1 class="title-fade" style="font-size: clamp(2.5rem, 5vw, 4.5rem); letter-spacing: 4px; margin-bottom: 10px; color: #f7f5f0;">PIJAO, CIUDAD SIN PRISA</h1>
        <h3 class="subtitle-fade" style="font-size: clamp(1rem, 2vw, 1.5rem); font-weight: 300; font-family: sans-serif; letter-spacing: 1px; margin-bottom: 50px; color: #e3dec9;">Te invitamos a recorrer lento a nuestro municipio</h3>
        <button id="btn-iniciar-travesia" class="btn-fade" style="background: transparent; border: 1px solid #f7f5f0; color: #f7f5f0; padding: 15px 35px; font-size: 1rem; cursor: pointer; transition: all 0.4s; font-family: sans-serif; letter-spacing: 2px;">INICIAR TRAVESÍA</button>
    </div>
</div>
''', unsafe_allow_html=True)

# ==========================================
# 3. NAVEGACIÓN Y CONTROLES
# ==========================================
st.markdown('''
<div id="audio-control">
    <span class="icon">🔊</span> <span class="text">QUITAR SONIDO</span>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div id="seccion-travesia"></div>
<nav id="main-nav">
    <a href="#inicio">Inicio</a>
    <a href="#casas-del-ayer">Casas del ayer</a>
    <a href="#historia-guerreros">Historia</a>
    <a href="#conoce-pijao">Conoce Pijao</a>
    <a href="#territorio">Territorio</a>
    <a href="#descubre-pijao">Descubre Pijao</a>
    <a href="#recorrido-audiovisual">Recorrido Audiovisual</a>
</nav>
''', unsafe_allow_html=True)

# ==========================================
# 4. CONTENIDO - TRAVESÍA
# ==========================================
st.markdown('<div id="inicio"></div>', unsafe_allow_html=True)
st.markdown('<div class="editorial-section">', unsafe_allow_html=True)
vp_path = find_asset("VPINICIO")
if vp_path:
    st.markdown('<div id="vp-container" style="box-shadow: 0 20px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
    st.video(vp_path)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Casas del ayer ---
st.markdown('<div id="casas-del-ayer"></div>', unsafe_allow_html=True)
st.markdown('<div class="editorial-section"><h2>Casas del Ayer</h2>', unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="large")
with col1:
    f3 = find_asset("F3")
    if f3: st.image(f3, use_column_width=True)
    st.markdown("<p style='text-align: left; font-size: 0.9rem; font-style: italic;'>La arquitectura tradicional del Paisaje Cultural Cafetero es un testimonio de adaptación al clima y conservación.</p>", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style='text-align: left;'>
    <p>La identidad arquitectónica de Pijao reposa en sus técnicas constructivas ancestrales. El bahareque y la madera se levantan formando paredes que respiran, permitiendo la adaptación al clima de la montaña.</p>
    <p>Los balcones, pintados de colores y adornados con flores, no son solo elementos decorativos, sino miradores hacia la vida cotidiana y el paisaje cafetero que nos rodea. Es un patrimonio vivo que refleja el espíritu de conservación de nuestra comunidad.</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown('<div style="text-align:center; margin-top:20px;"><a href="#welcome-screen" style="font-family:sans-serif; color:#4a6741; font-size:0.8rem; text-decoration:none;">VOLVER AL INICIO</a></div></div>', unsafe_allow_html=True)

# --- Historia de guerreros ---
st.markdown('<div id="historia-guerreros"></div>', unsafe_allow_html=True)
st.markdown('<div class="editorial-section"><h2>Historia de Guerreros</h2><p>Una narrativa humana y documental de quienes forjaron estas montañas.</p>', unsafe_allow_html=True)
cols_h = st.columns(3)
h_assets = [find_asset(x) for x in ["F2", "F5", "F6", "F16", "F17"]]
h_assets = [x for x in h_assets if x]
for idx, path in enumerate(h_assets):
    with cols_h[idx % 3]:
        st.image(path, use_column_width=True)
st.markdown('<div style="text-align:center; margin-top:20px;"><a href="#welcome-screen" style="font-family:sans-serif; color:#4a6741; font-size:0.8rem; text-decoration:none;">VOLVER AL INICIO</a></div></div>', unsafe_allow_html=True)

# --- Conoce Pijao ---
st.markdown('<div id="conoce-pijao"></div>', unsafe_allow_html=True)
st.markdown('<div class="editorial-section"><h2>Conoce Pijao</h2>', unsafe_allow_html=True)
f13 = find_asset("F13")
if f13: st.image(f13, use_column_width=True)
st.markdown("""
<p style="margin-top: 30px;">Pijao es un refugio donde el paisaje, la arquitectura y la cultura del café se entrelazan. Su identidad se fundamenta en el patrimonio y en su filosofía como <strong>Ciudad Sin Prisa (Cittaslow)</strong>, promoviendo un turismo responsable que invita a contemplar el entorno de manera pausada y consciente.</p>
<a href="https://www.youtube.com/watch?v=UPRAk3g7YVg" target="_blank" class="btn-outline">CONOCE MÁS</a>
<div style="text-align:center; margin-top:40px;"><a href="#welcome-screen" style="font-family:sans-serif; color:#4a6741; font-size:0.8rem; text-decoration:none;">VOLVER AL INICIO</a></div>
</div>
""", unsafe_allow_html=True)

# --- Territorio, Clima, Ubicación, Historia ---
st.markdown('<div id="territorio"></div>', unsafe_allow_html=True)
st.markdown('<div class="editorial-section" style="background-color: #efebe2; padding: 60px 40px; border-radius: 4px;">', unsafe_allow_html=True)

st.markdown('<h3>El Territorio</h3>', unsafe_allow_html=True)
st.markdown('<p>Ubicado en la Región Andina sobre la majestuosa Cordillera Central, el paisaje pijaense se define por la transición armónica entre la montaña, el piedemonte y el valle, configurando una relación profunda entre sus habitantes y el paisaje natural.</p>', unsafe_allow_html=True)

st.markdown('<h3 style="margin-top: 40px;">Clima</h3>', unsafe_allow_html=True)
st.markdown('<p>Las precipitaciones superan los 2400 mm en las zonas montañosas, mientras que en otras áreas señaladas promedian aproximadamente los 1800 mm anuales. Durante el día, se presentan vientos constantes que ascienden desde el valle del río Cauca hacia la montaña.</p>', unsafe_allow_html=True)

st.markdown('<h3 style="margin-top: 40px;">Ubicación</h3>', unsafe_allow_html=True)
st.markdown('<p>Pijao limita al Norte con Córdoba, al Este con el departamento del Tolima, al Sur con Génova, al Oeste con el Valle del Cauca y al Noroeste con Buenavista.</p>', unsafe_allow_html=True)

st.markdown('<h3 style="margin-top: 40px;">Línea de Tiempo Histórica</h3>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: left; max-width: 400px; margin: 0 auto;">
    <p><strong>1902</strong> — Fundación / nombre inicial San José de Colón</p>
    <p><strong>1905</strong> — Corregimiento de Calarcá</p>
    <p><strong>1912</strong> — Parroquia</p>
    <p><strong>1926</strong> — Municipio</p>
    <p><strong>1931</strong> — Adopción del nombre Pijao</p>
    <p><strong>2014</strong> — Ingreso a la red Cittaslow / Ciudad Sin Prisa</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center; margin-top:40px;"><a href="#welcome-screen" style="font-family:sans-serif; color:#4a6741; font-size:0.8rem; text-decoration:none;">VOLVER AL INICIO</a></div></div>', unsafe_allow_html=True)

# --- Descubre Pijao ---
st.markdown('<div id="descubre-pijao"></div>', unsafe_allow_html=True)
st.markdown('<div class="editorial-section"><h2>Descubre Pijao</h2>', unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: center; gap: 40px; flex-wrap: wrap; margin-top: 40px; font-family: serif; font-size: 1.3rem; color: #4a6741;">
    <span>ARQUITECTURA</span> <span>•</span> 
    <span>NATURALEZA</span> <span>•</span> 
    <span>CULTURA</span> <span>•</span> 
    <span>CAFÉ</span> <span>•</span> 
    <span>PATRIMONIO</span> <span>•</span> 
    <span>RUTAS Y EXPERIENCIAS</span>
</div>
<div style="text-align:center; margin-top:60px;"><a href="#welcome-screen" style="font-family:sans-serif; color:#4a6741; font-size:0.8rem; text-decoration:none;">VOLVER AL INICIO</a></div>
</div>
""", unsafe_allow_html=True)

# --- Recorrido Audiovisual ---
st.markdown('<div id="recorrido-audiovisual"></div>', unsafe_allow_html=True)
st.markdown('''
<div style="background: #1a1a1a; padding: 80px 20px; text-align: center; color: #f7f5f0;">
    <h2 style="margin-bottom: 40px; color: #f7f5f0;">Recorrido Audiovisual</h2>
    <div id="gallery-container" style="position: relative; max-width: 1000px; height: 65vh; margin: 0 auto; display: flex; align-items: center; justify-content: center; background: #0a0a0a; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <img id="gallery-img" style="width: 100%; height: 100%; object-fit: contain; display: none;" />
        <video id="gallery-vid" controls style="width: 100%; height: 100%; object-fit: contain; display: none;"></video>
    </div>
    <p id="gallery-caption" style="margin-top: 30px; font-family: 'Georgia', serif; font-size: 1.3rem; font-style: italic; color: #dcd7c9;"></p>
    
    <div style="margin-top: 40px; display: flex; justify-content: center; align-items: center; gap: 30px;">
        <button id="gal-prev" style="background: transparent; border: 1px solid #dcd7c9; color: #dcd7c9; padding: 12px 25px; cursor: pointer; font-family: sans-serif; letter-spacing: 1px; transition: 0.3s;">← ANTERIOR</button>
        <span id="gal-counter" style="font-family: sans-serif; font-weight: 300; font-size: 1.1rem; color: #dcd7c9;">01 / XX</span>
        <button id="gal-next" style="background: transparent; border: 1px solid #dcd7c9; color: #dcd7c9; padding: 12px 25px; cursor: pointer; font-family: sans-serif; letter-spacing: 1px; transition: 0.3s;">SIGUIENTE →</button>
    </div>
    <div style="text-align:center; margin-top:60px;"><a href="#welcome-screen" style="font-family:sans-serif; color:#888; font-size:0.8rem; text-decoration:none;">VOLVER AL INICIO</a></div>
</div>
''', unsafe_allow_html=True)


# ==========================================
# LÓGICA DE NEGOCIO Y DOM (JAVASCRIPT)
# ==========================================
js_logic = """
<script>
    const doc = window.parent.document;
    let initialized = false;

    // Esperar a que Streamlit renderice los elementos
    const initTimer = setInterval(() => {
        const loaders = doc.getElementById('hidden-loaders');
        const welcomeBg = doc.getElementById('welcome-background');
        const videoLoader = doc.getElementById('video-loader');
        const welcomeVideo = videoLoader ? videoLoader.querySelector('video') : null;
        const audioContainer = doc.getElementById('audio-container');
        const mainAudio = audioContainer ? audioContainer.querySelector('audio') : null;

        if (loaders && welcomeBg && welcomeVideo && mainAudio && !initialized) {
            initialized = true;
            clearInterval(initTimer);
            initializeApp(welcomeVideo, mainAudio);
        }
    }, 500);

    function initializeApp(welcomeVideo, mainAudio) {
        
        // --- 1. LÓGICA DEL VIDEO INICIAL Y SLIDESHOW ---
        const bgContainer = doc.getElementById('welcome-background');
        const widget = welcomeVideo.closest('.stVideo');
        
        if (widget) {
            bgContainer.appendChild(widget);
            widget.style.width = '100%';
            widget.style.height = '100%';
            welcomeVideo.style.objectFit = 'cover';
            welcomeVideo.style.width = '100%';
            welcomeVideo.style.height = '100%';
            
            // FASE 2: Fade-in del video
            setTimeout(() => { bgContainer.style.opacity = '1'; }, 2000);
            
            welcomeVideo.muted = true;
            welcomeVideo.currentTime = 0;
            welcomeVideo.play().catch(e => console.log("Auto-play requirió interacción:", e));

            // Cuando termine VIDEO
            welcomeVideo.onended = () => {
                setTimeout(() => {
                    widget.style.transition = "opacity 1s ease";
                    widget.style.opacity = '0';
                    setTimeout(() => { 
                        widget.style.display = 'none'; 
                        startSlideshow();
                    }, 1000);
                }, 1000); // 1 segundo de espera exigido
            };
        }

        function startSlideshow() {
            const loaders = doc.getElementById('hidden-loaders');
            const imgs = Array.from(loaders.querySelectorAll('img'));
            if(imgs.length === 0) return;
            
            // Clonar e insertar en el fondo
            const clones = [];
            imgs.forEach(img => {
                const clone = img.cloneNode();
                clone.style.position = 'absolute';
                clone.style.top = '0';
                clone.style.left = '0';
                clone.style.width = '100%';
                clone.style.height = '100%';
                clone.style.objectFit = 'cover';
                clone.style.opacity = '0';
                clone.style.transition = 'opacity 2s ease-in-out';
                bgContainer.appendChild(clone);
                clones.push(clone);
            });

            // Orden aleatorio
            for (let i = clones.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [clones[i], clones[j]] = [clones[j], clones[i]];
            }

            let cur = 0;
            clones[cur].style.opacity = '1';

            setInterval(() => {
                clones[cur].style.opacity = '0';
                cur = (cur + 1) % clones.length;
                clones[cur].style.opacity = '1';
            }, 5000);
        }

        // --- 2. LÓGICA DEL REPRODUCTOR DE AUDIO (M1) ---
        const audioControl = doc.getElementById('audio-control');
        
        audioControl.onclick = () => {
            if (mainAudio.muted || mainAudio.paused) {
                mainAudio.muted = false;
                mainAudio.play().catch(e => console.log(e));
                audioControl.innerHTML = '<span class="icon">🔊</span> <span class="text">QUITAR SONIDO</span>';
            } else {
                mainAudio.muted = true;
                audioControl.innerHTML = '<span class="icon">🔇</span> <span class="text">ACTIVAR SONIDO</span>';
            }
        };

        // --- 3. BOTÓN INICIAR TRAVESÍA ---
        const startBtn = doc.getElementById('btn-iniciar-travesia');
        startBtn.onclick = () => {
            doc.getElementById('seccion-travesia').scrollIntoView({behavior: 'smooth'});
            // Iniciar M1 automáticamente al interactuar
            mainAudio.muted = false;
            mainAudio.play().catch(e => console.log(e));
            audioControl.innerHTML = '<span class="icon">🔊</span> <span class="text">QUITAR SONIDO</span>';
        };

        // --- 4. GALERÍA AUDIOVISUAL MANUAL ---
        const galImgs = Array.from(doc.querySelectorAll('#hidden-loaders img')).map(img => img.src);
        const vid1 = welcomeVideo ? welcomeVideo.src : null;
        const vpContainer = doc.getElementById('vp-container');
        const vid2 = vpContainer ? vpContainer.querySelector('video').src : null;

        let items = [];
        galImgs.forEach(src => items.push({type: 'img', src: src}));
        if (vid1) items.push({type: 'video', src: vid1});
        if (vid2) items.push({type: 'video', src: vid2});

        const poeticCaptions = [
            "En Pijao, el tiempo también hace parte del paisaje.",
            "Cada rincón guarda una historia que merece ser recorrida sin prisa.",
            "Aquí la vida conserva el ritmo de las cosas hechas con tiempo.",
            "Entre montañas, memoria y caminos, Pijao invita a mirar de otra manera.",
            "Hay lugares que no se visitan solamente: se viven.",
            "La identidad de un pueblo también vive en sus pequeños momentos.",
            "Pijao es territorio de memoria, paisaje y encuentro.",
            "Caminar despacio también es una forma de conocer."
        ];

        let curGal = 0;
        const gImg = doc.getElementById('gallery-img');
        const gVid = doc.getElementById('gallery-vid');
        const gCap = doc.getElementById('gallery-caption');
        const gCount = doc.getElementById('gal-counter');
        const btnPrev = doc.getElementById('gal-prev');
        const btnNext = doc.getElementById('gal-next');

        function updateGallery() {
            if(items.length === 0) return;
            const item = items[curGal];
            gCount.innerText = String(curGal + 1).padStart(2, '0') + " / " + items.length;
            gCap.innerText = poeticCaptions[curGal % poeticCaptions.length];

            if(item.type === 'img') {
                gVid.style.display = 'none';
                gVid.pause();
                gImg.src = item.src;
                gImg.style.display = 'block';
            } else {
                gImg.style.display = 'none';
                gVid.src = item.src;
                gVid.style.display = 'block';
            }
        }

        btnPrev.onclick = () => { curGal = (curGal - 1 + items.length) % items.length; updateGallery(); };
        btnNext.onclick = () => { curGal = (curGal + 1) % items.length; updateGallery(); };
        
        updateGallery(); // Inicializar galería
    }
</script>
"""
components.html(js_logic, height=0)
