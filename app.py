import base64
from pathlib import Path
import mimetypes
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Pijao, Ciudad Sin Prisa",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTS = {".mp4", ".webm", ".mov"}
AUDIO_EXTS = {".mp3", ".wav", ".ogg"}

def find_asset(name):
    if not ASSETS_DIR.exists():
        return None
    for path in ASSETS_DIR.iterdir():
        if (
            path.is_file()
            and path.suffix.lower() in IMAGE_EXTS | VIDEO_EXTS | AUDIO_EXTS
            and path.stem.lower() == name.lower()
        ):
            return path
    return None

def data_uri(path):
    if not path or not path.exists():
        return ""
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"

VIDEO = data_uri(find_asset("VIDEO"))
VPINICIO = data_uri(find_asset("VPINICIO"))
M1 = data_uri(find_asset("M1"))
PHOTOS = [data_uri(find_asset(f"F{i}")) for i in range(1, 19)]

photo_json = "[" + ",".join(repr(x) for x in PHOTOS if x) + "]"

html = r"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pijao, Ciudad Sin Prisa</title>
<style>
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
    margin:0;
    padding:0;
    background:#f5f1e9;
    color:#292825;
    font-family:Arial,Helvetica,sans-serif;
}
button,a{font:inherit}
button{cursor:pointer}
.hidden{display:none!important}

/* ---------- BIENVENIDA: PÁGINA REAL DE INICIO ---------- */
#welcome{
    position:relative;
    width:100%;
    min-height:100vh;
    height:100vh;
    overflow:hidden;
    background:#11110f;
    color:#f8f4ec;
}
#welcome-photo{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    background-size:cover;
    background-position:center;
    opacity:0;
    transition:opacity 2.2s ease;
    z-index:1;
}
#welcome-shade{
    position:absolute;
    inset:0;
    background:
      linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,.25) 42%,rgba(0,0,0,.68)),
      radial-gradient(circle at center,transparent 30%,rgba(0,0,0,.32) 100%);
    z-index:3;
}
#welcome-video{
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    width:min(84vw,1100px);
    height:min(54vh,620px);
    object-fit:cover;
    object-position:center;
    opacity:0;
    transition:opacity 1.8s ease;
    z-index:2;
    box-shadow:0 20px 80px rgba(0,0,0,.42);
    border-radius:2px;
}
.welcome-copy{
    position:absolute;
    inset:0;
    z-index:5;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    text-align:center;
    padding:32px;
    pointer-events:none;
}
#welcome-title{
    margin:0 0 12px;
    font-family:Georgia,"Times New Roman",serif;
    font-weight:400;
    font-size:clamp(2.2rem,5vw,5.1rem);
    letter-spacing:.11em;
    line-height:1.08;
    text-shadow:0 5px 28px rgba(0,0,0,.6);
    opacity:0;
    transform:translateY(16px);
    transition:opacity 1.5s ease,transform 1.5s ease;
}
#welcome-subtitle{
    margin:0;
    max-width:720px;
    color:#e7e1d7;
    font-size:clamp(.95rem,1.6vw,1.2rem);
    letter-spacing:.04em;
    opacity:0;
    transform:translateY(12px);
    transition:opacity 1.5s ease .2s,transform 1.5s ease .2s;
}
#welcome-action{
    position:absolute;
    left:50%;
    bottom:9vh;
    transform:translateX(-50%) translateY(15px);
    z-index:7;
    opacity:0;
    transition:opacity 1.4s ease,transform 1.4s ease;
    pointer-events:auto;
}
#start-button{
    color:#f8f4ec;
    background:rgba(24,25,21,.35);
    border:1px solid rgba(248,244,236,.72);
    padding:14px 32px;
    letter-spacing:.18em;
    font-size:.78rem;
    transition:.35s ease;
    backdrop-filter:blur(6px);
}
#start-button:hover{
    background:#f8f4ec;
    color:#24231f;
}
.fade-in{opacity:1!important;transform:translateY(0)!important}

/* ---------- EXPERIENCIA ---------- */
#journey{
    display:none;
    background:#f5f1e9;
}
#journey.visible{display:block;animation:pageIn 1.2s ease both}
@keyframes pageIn{from{opacity:0}to{opacity:1}}

.nav{
    position:sticky;
    top:0;
    z-index:50;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:24px;
    padding:16px 5%;
    background:rgba(245,241,233,.94);
    border-bottom:1px solid rgba(45,43,39,.1);
    backdrop-filter:blur(14px);
}
.brand{
    color:#292825;
    text-decoration:none;
    font-family:Georgia,"Times New Roman",serif;
    letter-spacing:.12em;
    font-size:1.05rem;
    white-space:nowrap;
}
.navlinks{
    display:flex;
    flex-wrap:wrap;
    justify-content:flex-end;
    gap:20px;
}
.navlinks a{
    color:#59554e;
    text-decoration:none;
    font-size:.78rem;
    letter-spacing:.05em;
}
.navlinks a:hover{color:#20201c}

.audio-control{
    position:fixed;
    right:22px;
    bottom:22px;
    z-index:100;
}
.audio-toggle{
    border:1px solid rgba(248,244,236,.25);
    background:rgba(28,29,25,.92);
    color:#f8f4ec;
    padding:11px 16px;
    font-size:.72rem;
    letter-spacing:.09em;
    box-shadow:0 8px 28px rgba(0,0,0,.18);
}
.audio-toggle:hover{background:#171814}
.audio-status{
    display:none;
    margin-bottom:8px;
    background:rgba(28,29,25,.94);
    color:#eee9df;
    padding:10px 13px;
    font-size:.7rem;
    letter-spacing:.06em;
}
.audio-control.open .audio-status{display:block}

.hero-journey{
    min-height:74vh;
    background:#11110f;
    display:flex;
    align-items:center;
    justify-content:center;
    overflow:hidden;
}
#vpinicio{
    width:100%;
    max-height:78vh;
    object-fit:cover;
    display:block;
}

.section{
    padding:110px 7%;
    border-bottom:1px solid rgba(47,44,39,.1);
}
.section.alt{background:#ebe5da}
.section-inner{max-width:1120px;margin:auto}
.kicker{
    color:#6a715a;
    text-transform:uppercase;
    letter-spacing:.2em;
    font-size:.72rem;
    margin-bottom:14px;
}
h2{
    margin:0 0 22px;
    font-family:Georgia,"Times New Roman",serif;
    font-size:clamp(2rem,4vw,3.5rem);
    font-weight:400;
    line-height:1.1;
}
p{
    line-height:1.85;
    color:#57534d;
    font-size:1rem;
}
.lead{
    max-width:800px;
    font-size:1.08rem;
}
.video-section{
    background:#171713;
    color:#f7f2e9;
}
.video-section h2,.video-section p{color:#f7f2e9}
.main-video-wrap{
    max-width:1100px;
    margin:48px auto 0;
}
#main-video{
    display:block;
    width:100%;
    max-height:72vh;
    object-fit:cover;
    object-position:center;
    background:#000;
}
.caption{
    margin-top:15px;
    font-size:.76rem;
    color:#bdb7ac;
    letter-spacing:.05em;
}

.image-large{
    width:100%;
    display:block;
    max-height:680px;
    object-fit:cover;
}
.split{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:60px;
    align-items:center;
}
.gallery{
    display:grid;
    grid-template-columns:1.2fr .8fr;
    gap:18px;
    margin-top:40px;
}
.gallery img{
    width:100%;
    height:360px;
    object-fit:cover;
    display:block;
}
.gallery img:first-child{
    height:520px;
    grid-row:span 2;
}
.three{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:22px;
    margin-top:40px;
}
.card{
    background:#f8f4ec;
    border:1px solid #ddd5c8;
    padding:28px;
}
.card h3{
    font-family:Georgia,"Times New Roman",serif;
    font-size:1.3rem;
    font-weight:400;
    margin:0 0 10px;
}
.card p{font-size:.9rem;margin:0}
.f13{
    width:100%;
    max-height:720px;
    object-fit:cover;
    display:block;
}
.youtube{
    display:inline-block;
    margin-top:18px;
    padding:13px 25px;
    background:#282823;
    color:#f8f4ec;
    text-decoration:none;
    font-size:.76rem;
    letter-spacing:.12em;
}
.youtube:hover{background:#4d4a42}

.timeline{
    max-width:850px;
    margin:45px auto 0;
    border-left:1px solid #bcb4a6;
    padding-left:30px;
}
.event{
    position:relative;
    margin-bottom:38px;
}
.event:before{
    content:"";
    position:absolute;
    left:-36px;
    top:5px;
    width:10px;
    height:10px;
    border:2px solid #f5f1e9;
    background:#6b725c;
    border-radius:50%;
}
.event-year{
    font-family:Georgia,"Times New Roman",serif;
    font-size:1.35rem;
}
.event-text{
    color:#5c5750;
    margin-top:5px;
    line-height:1.65;
}
.categories{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:20px;
    margin-top:38px;
}
.category{
    min-height:170px;
    padding:30px;
    background:#f8f4ec;
    border:1px solid #ddd5c8;
    transition:transform .3s ease;
}
.category:hover{transform:translateY(-3px)}
.category h3{
    font-family:Georgia,"Times New Roman",serif;
    font-weight:400;
    margin:0 0 12px;
}
.category p{font-size:.88rem;margin:0}

.location-list{
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:12px;
    margin-top:35px;
}
.location-item{
    border-top:1px solid #bcb4a6;
    padding-top:14px;
}
.location-item strong{display:block;font-family:Georgia,serif;font-weight:400;margin-bottom:4px}
.location-item span{font-size:.86rem;color:#625d55}

#recorrido-audiovisual .recorrido{
    max-width:1000px;
    margin:45px auto 0;
    text-align:center;
}
.counter{
    color:#6a715a;
    font-size:.74rem;
    letter-spacing:.2em;
    margin-bottom:18px;
}
#recorrido-media{
    background:#171713;
    min-height:420px;
    display:flex;
    align-items:center;
    justify-content:center;
    margin:25px 0;
}
#recorrido-media img,#recorrido-media video{
    display:block;
    width:100%;
    max-height:650px;
    object-fit:contain;
}
.phrase{
    font-family:Georgia,"Times New Roman",serif;
    font-style:italic;
    font-size:1.35rem;
    line-height:1.5;
    max-width:760px;
    margin:25px auto;
}
.recorrido-controls{
    display:flex;
    justify-content:center;
    gap:14px;
}
.recorrido-controls button{
    padding:12px 22px;
    border:1px solid #bcb4a6;
    background:transparent;
    color:#292825;
    letter-spacing:.08em;
    font-size:.72rem;
}
.recorrido-controls button:hover{background:#292825;color:#f8f4ec}

.back-home{
    display:inline-block;
    margin-top:45px;
    color:#625d55;
    text-decoration:none;
    border-bottom:1px solid #9e9689;
    padding-bottom:5px;
    font-size:.76rem;
    letter-spacing:.1em;
}
.footer{
    padding:70px 7%;
    background:#22221e;
    color:#eee8dc;
    text-align:center;
}
.footer h3{
    font-family:Georgia,"Times New Roman",serif;
    font-weight:400;
    letter-spacing:.1em;
}
.footer p{color:#aaa59b;font-size:.86rem}

@media(max-width:900px){
    .navlinks{display:none}
    .split{grid-template-columns:1fr;gap:35px}
    .three,.categories{grid-template-columns:1fr 1fr}
    .location-list{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:600px){
    #welcome-video{width:92vw;height:42vh}
    #welcome-title{font-size:2.15rem}
    #welcome-action{bottom:6vh}
    .section{padding:80px 6%}
    .three,.categories,.location-list,.gallery{grid-template-columns:1fr}
    .gallery img,.gallery img:first-child{height:330px;grid-row:auto}
    .audio-control{right:12px;bottom:12px}
    .phrase{font-size:1.1rem}
}
</style>
</head>
<body>

<!-- =========================================================
     PÁGINA 1 — INICIO / BIENVENIDA
     ========================================================= -->
<section id="welcome">
    <div id="welcome-photo"></div>

    <video id="welcome-video" autoplay muted playsinline preload="auto">
        __VIDEO_SOURCE__
    </video>

    <div id="welcome-shade"></div>

    <div class="welcome-copy">
        <h1 id="welcome-title">PIJAO, CIUDAD SIN PRISA</h1>
        <p id="welcome-subtitle">Te invitamos a recorrer lento a nuestro municipio</p>
    </div>

    <div id="welcome-action">
        <button id="start-button" type="button">INICIAR TRAVESÍA</button>
    </div>
</section>

<!-- =========================================================
     PÁGINA 2 — TRAVESÍA
     ========================================================= -->
<main id="journey">

    <nav class="nav">
        <a class="brand" href="#top">PIJAO</a>
        <div class="navlinks">
            <a href="#inicio-experiencia">Inicio</a>
            <a href="#casas-ayer">Casas del ayer</a>
            <a href="#historia-guerreros">Historia</a>
            <a href="#conoce-pijao">Conoce Pijao</a>
            <a href="#territorio">Territorio</a>
            <a href="#descubre-pijao">Descubre Pijao</a>
            <a href="#recorrido-audiovisual">Recorrido audiovisual</a>
        </div>
    </nav>

    <div id="top"></div>

    <section class="hero-journey" id="inicio-experiencia">
        <video id="vpinicio" autoplay muted playsinline loop preload="auto">
            __VPINICIO_SOURCE__
        </video>
    </section>

    <audio id="m1" loop preload="auto">
        __M1_SOURCE__
    </audio>

    <div class="audio-control" id="audio-control">
        <div class="audio-status" id="audio-status">SONIDO ACTIVO</div>
        <button class="audio-toggle" id="audio-toggle" type="button">◖ SONIDO</button>
    </div>

    <section class="section">
        <div class="section-inner">
            <div class="kicker">Territorio y memoria</div>
            <h2>Una experiencia sin prisa</h2>
            <p class="lead">
                Pijao invita a cambiar el ritmo: caminar, observar, escuchar y reconocer
                el paisaje, la arquitectura, la memoria y las pequeñas escenas que hacen
                parte de la vida cotidiana.
            </p>
            <a class="back-home" href="#welcome">VOLVER AL INICIO</a>
        </div>
    </section>

    <!-- VIDEO PRINCIPAL -->
    <section class="section video-section" id="video-cinematografico">
        <div class="section-inner">
            <div class="kicker" style="color:#aab095">Registro audiovisual</div>
            <h2>El latido de la montaña</h2>
            <p class="lead">
                Una mirada audiovisual a Pijao y a la atmósfera pausada de su territorio.
            </p>
            <div class="main-video-wrap">
                <video id="main-video" controls playsinline preload="metadata">
                    __VIDEO_SOURCE__
                </video>
                <div class="caption">VIDEO · reproducción completa desde el inicio</div>
            </div>
        </div>
    </section>

    <!-- CASAS DEL AYER -->
    <section class="section" id="casas-ayer">
        <div class="section-inner">
            <div class="split">
                <div>
                    <div class="kicker">Patrimonio arquitectónico</div>
                    <h2>Casas del ayer</h2>
                    <p>
                        La arquitectura tradicional de Pijao conserva el uso de materiales,
                        formas y soluciones constructivas vinculadas al paisaje cafetero.
                        El bahareque, la madera, los balcones y los espacios de transición
                        hacen parte de una identidad que permanece visible en el municipio.
                    </p>
                    <p>
                        Más que una colección de fachadas, estas casas forman parte de una
                        memoria cotidiana: calles, viviendas y detalles que relacionan
                        patrimonio, clima y manera de habitar.
                    </p>
                </div>
                <div>
                    __CASAS_IMAGE__
                </div>
            </div>
        </div>
    </section>

    <!-- HISTORIA DE GUERREROS -->
    <section class="section alt" id="historia-guerreros">
        <div class="section-inner">
            <div class="kicker">Memoria</div>
            <h2>Historia de guerreros</h2>
            <p class="lead">
                Una aproximación humana a la memoria de los territorios de montaña,
                entendida desde sus habitantes, sus caminos y las historias que
                permanecen en el paisaje.
            </p>
            <div class="gallery">
                __HIST_IMAGES__
            </div>
        </div>
    </section>

    <!-- CONOCE PIJAO -->
    <section class="section" id="conoce-pijao">
        <div class="section-inner">
            <div class="split">
                <div>__F13_IMAGE__</div>
                <div>
                    <div class="kicker">Destino y filosofía</div>
                    <h2>Conoce Pijao</h2>
                    <p>
                        Pijao reúne paisaje de montaña, arquitectura tradicional, cultura
                        cafetera, patrimonio e identidad local dentro de una experiencia
                        asociada al concepto de Ciudad Sin Prisa.
                    </p>
                    <p>
                        Conocer el municipio también significa reconocer su territorio y
                        recorrerlo de manera responsable, respetando su patrimonio,
                        sus paisajes y sus formas de vida.
                    </p>
                    <a class="youtube" href="https://www.youtube.com/watch?v=UPRAk3g7YVg" target="_blank" rel="noopener">
                        CONOCE MÁS
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- TERRITORIO -->
    <section class="section alt" id="territorio">
        <div class="section-inner">
            <div class="kicker">Geografía y entorno</div>
            <h2>El territorio</h2>
            <div class="three">
                <article class="card">
                    <h3>Región Andina</h3>
                    <p>
                        Pijao hace parte de la Región Andina y de la Cordillera Central,
                        en un territorio donde montaña, piedemonte y valle configuran
                        el paisaje.
                    </p>
                </article>
                <article class="card">
                    <h3>Clima</h3>
                    <p>
                        En zonas montañosas la precipitación supera los 2400 mm y en otras
                        zonas señaladas se registran aproximadamente 1800 mm anuales.
                        Durante el día se presentan vientos desde el valle del río Cauca
                        hacia la montaña.
                    </p>
                </article>
                <article class="card">
                    <h3>Ubicación</h3>
                    <p>
                        Un territorio de montaña relacionado con distintos municipios y
                        departamentos vecinos del entorno cordillerano.
                    </p>
                </article>
            </div>

            <div class="location-list">
                <div class="location-item"><strong>Norte</strong><span>Córdoba</span></div>
                <div class="location-item"><strong>Este</strong><span>Tolima</span></div>
                <div class="location-item"><strong>Sur</strong><span>Génova</span></div>
                <div class="location-item"><strong>Oeste</strong><span>Valle del Cauca</span></div>
                <div class="location-item"><strong>Noroeste</strong><span>Buenavista</span></div>
            </div>
        </div>
    </section>

    <!-- HISTORIA -->
    <section class="section" id="historia">
        <div class="section-inner">
            <div class="kicker">Cronología</div>
            <h2>Historia</h2>
            <div class="timeline">
                <div class="event">
                    <div class="event-year">1902</div>
                    <div class="event-text">Fundación / nombre inicial: San José de Colón.</div>
                </div>
                <div class="event">
                    <div class="event-year">1905</div>
                    <div class="event-text">Corregimiento de Calarcá.</div>
                </div>
                <div class="event">
                    <div class="event-year">1912</div>
                    <div class="event-text">Parroquia.</div>
                </div>
                <div class="event">
                    <div class="event-year">1926</div>
                    <div class="event-text">Municipio.</div>
                </div>
                <div class="event">
                    <div class="event-year">1931</div>
                    <div class="event-text">Nombre Pijao.</div>
                </div>
                <div class="event">
                    <div class="event-year">2014</div>
                    <div class="event-text">Cittaslow / Ciudad Sin Prisa.</div>
                </div>
            </div>
        </div>
    </section>

    <!-- DESCUBRE -->
    <section class="section alt" id="descubre-pijao">
        <div class="section-inner">
            <div class="kicker">Ejes temáticos</div>
            <h2>Descubre Pijao</h2>
            <p class="lead">
                Seis formas de aproximarse al territorio sin convertirlo en un catálogo:
                arquitectura, naturaleza, cultura, café, patrimonio y experiencias.
            </p>
            <div class="categories">
                <article class="category"><h3>Arquitectura</h3><p>Bahareque, madera, balcones y formas tradicionales de habitar.</p></article>
                <article class="category"><h3>Naturaleza</h3><p>Montaña, paisaje y relación cotidiana con el entorno natural.</p></article>
                <article class="category"><h3>Cultura</h3><p>Memoria, identidad y prácticas que hacen reconocible al territorio.</p></article>
                <article class="category"><h3>Café</h3><p>Una dimensión fundamental del paisaje y de la identidad cafetera.</p></article>
                <article class="category"><h3>Patrimonio</h3><p>Espacios, arquitectura y memoria que forman parte de la historia local.</p></article>
                <article class="category"><h3>Rutas y experiencias</h3><p>Recorrer, caminar, observar y conocer el territorio sin prisa.</p></article>
            </div>
        </div>
    </section>

    <!-- RECORRIDO AUDIOVISUAL -->
    <section class="section" id="recorrido-audiovisual">
        <div class="section-inner">
            <div class="kicker" style="text-align:center">Experiencia manual</div>
            <h2 style="text-align:center">Recorrido audiovisual</h2>
            <p class="lead" style="margin:0 auto;text-align:center">
                Recorre las fotografías y registros audiovisuales a tu propio ritmo.
            </p>
            <div class="recorrido">
                <div class="counter" id="counter">01 / 20</div>
                <div id="recorrido-media"></div>
                <div class="phrase" id="phrase"></div>
                <div class="recorrido-controls">
                    <button id="prev">← ANTERIOR</button>
                    <button id="next">SIGUIENTE →</button>
                </div>
            </div>
            <div style="text-align:center">
                <a class="back-home" href="#welcome">VOLVER AL INICIO</a>
            </div>
        </div>
    </section>

    <footer class="footer">
        <h3>PIJAO, CIUDAD SIN PRISA</h3>
        <p>Territorio, memoria, paisaje y encuentro.</p>
        <a class="back-home" style="color:#eee8dc;border-color:#777268" href="#welcome">VOLVER AL INICIO</a>
    </footer>
</main>

<script>
(function(){
    const photos = __PHOTOS__;
    const welcome = document.getElementById("welcome");
    const title = document.getElementById("welcome-title");
    const subtitle = document.getElementById("welcome-subtitle");
    const welcomeVideo = document.getElementById("welcome-video");
    const welcomePhoto = document.getElementById("welcome-photo");
    const startButton = document.getElementById("start-button");
    const action = document.getElementById("welcome-action");
    const journey = document.getElementById("journey");
    const m1 = document.getElementById("m1");
    const audioControl = document.getElementById("audio-control");
    const audioToggle = document.getElementById("audio-toggle");
    const audioStatus = document.getElementById("audio-status");

    // Secuencia exacta de bienvenida:
    // 1) título, 2) video, 3) botón.
    setTimeout(() => title.classList.add("fade-in"), 450);
    setTimeout(() => subtitle.classList.add("fade-in"), 850);
    setTimeout(() => {
        if (welcomeVideo) {
            welcomeVideo.style.opacity = "1";
            try { welcomeVideo.play(); } catch(e) {}
        }
    }, 1700);
    setTimeout(() => {
        action.classList.add("fade-in");
    }, 3400);

    // Al terminar VIDEO: esperar 1 segundo y empezar fotos aleatorias en fade.
    let slideshowTimer = null;
    let photoIndex = -1;

    function nextRandomPhoto(){
        if (!photos.length) return;
        let next = Math.floor(Math.random() * photos.length);
        if (photos.length > 1 && next === photoIndex) {
            next = (next + 1) % photos.length;
        }
        photoIndex = next;
        welcomePhoto.style.opacity = "0";
        setTimeout(() => {
            welcomePhoto.style.backgroundImage = "url('" + photos[photoIndex] + "')";
            welcomePhoto.style.opacity = "1";
        }, 900);
    }

    function startSlideshow(){
        if (!photos.length) return;
        nextRandomPhoto();
        slideshowTimer = setInterval(nextRandomPhoto, 6500);
    }

    if (welcomeVideo) {
        welcomeVideo.addEventListener("ended", function(){
            setTimeout(startSlideshow, 1000);
        });
    }

    function startJourney(){
        if (slideshowTimer) {
            clearInterval(slideshowTimer);
            slideshowTimer = null;
        }

        // M1 se reproduce dentro de la misma página y después de una
        // interacción directa del usuario: esto satisface la regla de autoplay
        // de la mayoría de navegadores.
        if (m1) {
            m1.muted = false;
            m1.volume = 1.0;
            const playPromise = m1.play();
            if (playPromise && typeof playPromise.catch === "function") {
                playPromise.catch(function(){
                    // Si el navegador aún bloquea la reproducción, el usuario
                    // puede pulsar el control de sonido para iniciar M1.
                    audioStatus.textContent = "PULSA SONIDO PARA INICIAR";
                });
            }
        }

        welcome.style.transition = "opacity 1s ease";
        welcome.style.opacity = "0";

        setTimeout(function(){
            welcome.style.display = "none";
            journey.classList.add("visible");
            window.scrollTo({top:0,behavior:"smooth"});

            // Segundo intento de reproducción, todavía derivado de la
            // interacción del usuario.
            if (m1) {
                const p = m1.play();
                if (p && p.catch) p.catch(function(){});
            }
        }, 950);
    }

    startButton.addEventListener("click", startJourney);

    // Control REAL del elemento HTML5 <audio>.
    audioToggle.addEventListener("click", function(){
        if (!m1) return;

        if (m1.paused) {
            m1.muted = false;
            m1.volume = 1;
            const p = m1.play();
            if (p && p.catch) p.catch(function(){});
        } else if (m1.muted) {
            m1.muted = false;
            m1.volume = 1;
        } else {
            m1.muted = true;
        }

        updateAudioUI();
    });

    function updateAudioUI(){
        if (!m1) return;
        if (m1.paused) {
            audioToggle.textContent = "◖ SONIDO";
            audioStatus.textContent = "PULSA PARA INICIAR";
        } else if (m1.muted) {
            audioToggle.textContent = "◖ ACTIVAR SONIDO";
            audioStatus.textContent = "SONIDO DESACTIVADO";
        } else {
            audioToggle.textContent = "◖ QUITAR SONIDO";
            audioStatus.textContent = "SONIDO ACTIVO";
        }
    }

    audioControl.addEventListener("mouseenter", () => audioControl.classList.add("open"));
    audioControl.addEventListener("mouseleave", () => audioControl.classList.remove("open"));
    audioToggle.addEventListener("focus", () => audioControl.classList.add("open"));

    // Si el navegador deja el audio en pausa, el control lo refleja.
    if (m1) {
        m1.addEventListener("play", updateAudioUI);
        m1.addEventListener("pause", updateAudioUI);
        m1.addEventListener("volumechange", updateAudioUI);
    }

    // ---------- Recorrido audiovisual ----------
    const recorrido = [];
    photos.forEach((src, i) => {
        if (src) recorrido.push({type:"image",src:src,name:"F"+(i+1)});
    });

    const vpinicioSrc = "__VPINICIO_RAW__";
    const videoSrc = "__VIDEO_RAW__";

    if (videoSrc) recorrido.push({type:"video",src:videoSrc,name:"VIDEO"});
    if (vpinicioSrc) recorrido.push({type:"video",src:vpinicioSrc,name:"VPINICIO"});

    const phrases = [
        "En Pijao, el tiempo también hace parte del paisaje.",
        "Cada rincón guarda una historia que merece ser recorrida sin prisa.",
        "Aquí la vida conserva el ritmo de las cosas hechas con tiempo.",
        "Entre montañas, memoria y caminos, Pijao invita a mirar de otra manera.",
        "Hay lugares que no se visitan solamente: se viven.",
        "La identidad de un pueblo también vive en sus pequeños momentos.",
        "Pijao es territorio de memoria, paisaje y encuentro.",
        "Caminar despacio también es una forma de conocer.",
        "La quietud de las montañas también cuenta historias.",
        "Detenerse a observar es otra forma de recorrer.",
        "El paisaje guarda parte de la memoria de quienes lo habitan.",
        "Cada camino puede ser una invitación a mirar con atención.",
        "La montaña, la arquitectura y la memoria forman un mismo paisaje.",
        "Conocer un lugar también es aprender a escuchar su ritmo.",
        "Hay territorios que se comprenden mejor cuando se recorren despacio.",
        "Pijao conserva una relación cercana entre paisaje, memoria y vida cotidiana.",
        "Lo esencial también puede encontrarse en los pequeños momentos.",
        "Recorrer sin prisa permite descubrir otras formas de mirar."
    ];

    let recorridoIndex = 0;
    const media = document.getElementById("recorrido-media");
    const counter = document.getElementById("counter");
    const phrase = document.getElementById("phrase");

    function renderRecorrido(){
        if (!recorrido.length) {
            media.innerHTML = "<p style='color:#ddd'>No hay recursos audiovisuales disponibles.</p>";
            return;
        }

        const item = recorrido[recorridoIndex];
        counter.textContent =
            String(recorridoIndex + 1).padStart(2,"0") + " / " +
            String(recorrido.length).padStart(2,"0");

        phrase.textContent = "“" + phrases[recorridoIndex % phrases.length] + "”";
        media.innerHTML = "";

        if (item.type === "image") {
            const img = document.createElement("img");
            img.src = item.src;
            img.alt = item.name;
            media.appendChild(img);
        } else {
            const video = document.createElement("video");
            video.src = item.src;
            video.controls = true;
            video.playsInline = true;
            video.preload = "metadata";
            media.appendChild(video);
        }
    }

    document.getElementById("prev").addEventListener("click", function(){
        recorridoIndex = (recorridoIndex - 1 + recorrido.length) % recorrido.length;
        renderRecorrido();
    });

    document.getElementById("next").addEventListener("click", function(){
        recorridoIndex = (recorridoIndex + 1) % recorrido.length;
        renderRecorrido();
    });

    renderRecorrido();

    // Todos los enlaces internos vuelven a funcionar dentro de esta única
    // página, sin depender de reruns de Streamlit.
    document.querySelectorAll('a[href^="#"]').forEach(function(link){
        link.addEventListener("click", function(e){
            const targetId = link.getAttribute("href");
            if (targetId === "#welcome") {
                e.preventDefault();
                journey.classList.remove("visible");
                journey.style.display = "none";
                welcome.style.display = "block";
                welcome.style.opacity = "1";
                window.scrollTo({top:0,behavior:"smooth"});
                return;
            }
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({behavior:"smooth",block:"start"});
            }
        });
    });
})();
</script>
</body>
</html>
"""

def source_tag(src, tag):
    if not src:
        return ""
    if tag == "video":
        return f'<source src="{src}" type="video/mp4">'
    return f'<source src="{src}" type="audio/mpeg">'

hist = [PHOTOS[i-1] for i in [2,5,6,16,17] if PHOTOS[i-1]]
hist_html = "".join(
    f'<img src="{src}" alt="Pijao" loading="lazy">'
    for src in hist
)

casas_src = PHOTOS[0] or PHOTOS[2]
casas_html = (
    f'<img class="image-large" src="{casas_src}" alt="Casas del ayer" loading="lazy">'
    if casas_src else
    '<div class="card">La fotografía de esta sección no está disponible.</div>'
)

f13_html = (
    f'<img class="f13" src="{PHOTOS[12]}" alt="Pijao" loading="lazy">'
    if PHOTOS[12] else
    '<div class="card">F13 no está disponible.</div>'
)

html = html.replace("__VIDEO_SOURCE__", source_tag(VIDEO, "video"))
html = html.replace("__VPINICIO_SOURCE__", source_tag(VPINICIO, "video"))
html = html.replace("__M1_SOURCE__", source_tag(M1, "audio"))
html = html.replace("__CASAS_IMAGE__", casas_html)
html = html.replace("__HIST_IMAGES__", hist_html)
html = html.replace("__F13_IMAGE__", f13_html)
html = html.replace("__PHOTOS__", photo_json)
html = html.replace("__VPINICIO_RAW__", VPINICIO.replace('"', '\\"'))
html = html.replace("__VIDEO_RAW__", VIDEO.replace('"', '\\"'))

components.html(html, height=4200, scrolling=True)
