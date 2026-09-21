import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flores Amarillas para una Amistad",
    page_icon="🌻",
    layout="centered"
)

st.markdown('''
<style>
.stApp{
    background:
      radial-gradient(circle at top left, rgba(255,230,110,.30), transparent 28%),
      radial-gradient(circle at bottom right, rgba(255,208,70,.22), transparent 25%),
      linear-gradient(180deg,#fffdf6 0%,#fff8dd 100%);
}
.block-container{
    max-width:900px;
    padding-top:1.2rem;
    padding-bottom:2rem;
}
footer,#MainMenu,header{visibility:hidden;}
</style>
''', unsafe_allow_html=True)

html = r'''
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<style>
*{box-sizing:border-box}
body{
    margin:0;
    font-family:Arial, Helvetica, sans-serif;
    color:#514a28;
    background:transparent;
}
.wrapper{padding:4px}
.hero{
    text-align:center;
    padding:30px 18px 20px;
}
.badge{
    display:inline-block;
    padding:7px 13px;
    border-radius:999px;
    background:#fff3a8;
    border:1px solid #e4c84d;
    font-size:14px;
    font-weight:700;
    color:#705d10;
    margin-bottom:12px;
}
h1{
    margin:0;
    font-size:44px;
    color:#6a570d;
    line-height:1.08;
}
.lead{
    max-width:680px;
    margin:14px auto 0;
    font-size:18px;
    line-height:1.6;
    color:#746a3e;
}
.section{
    background:rgba(255,255,255,.86);
    border:1px solid rgba(224,190,58,.55);
    border-radius:28px;
    padding:24px;
    margin:18px 0;
    box-shadow:0 14px 34px rgba(107,83,0,.08);
}
.section h2{
    text-align:center;
    margin:0 0 7px;
    color:#6b570d;
    font-size:25px;
}
.section p.note{
    text-align:center;
    margin:0 0 18px;
    color:#807647;
}
.garden{
    position:relative;
    min-height:360px;
    border-radius:24px;
    overflow:hidden;
    background:linear-gradient(#eaf7ff 0%,#fff8d1 68%,#d9efbc 69%,#9bc76c 100%);
    border:1px solid #e8d27a;
}
.sun{
    position:absolute;
    width:74px;height:74px;
    right:30px;top:25px;
    border-radius:50%;
    background:#ffe46c;
    box-shadow:0 0 40px rgba(255,205,50,.45);
}
.cloud{
    position:absolute;
    width:96px;height:30px;
    background:white;
    border-radius:30px;
    opacity:.92;
}
.cloud:before,.cloud:after{
    content:"";
    position:absolute;
    background:white;
    border-radius:50%;
}
.cloud:before{width:42px;height:42px;left:15px;top:-17px}
.cloud:after{width:52px;height:52px;left:42px;top:-26px}
.c1{left:9%;top:56px}
.c2{right:18%;top:92px;transform:scale(.78)}
.flower{
    position:absolute;
    bottom:54px;
    cursor:pointer;
    user-select:none;
    transition:transform .25s ease, filter .25s ease;
    animation:sway 3.2s ease-in-out infinite alternate;
}
.flower:hover{
    transform:translateY(-6px) scale(1.06);
    filter:drop-shadow(0 8px 8px rgba(0,0,0,.12));
}
.flower .emoji{
    font-size:66px;
    display:block;
}
.f1{left:8%;animation-delay:.1s}
.f2{left:25%;bottom:82px;animation-delay:.8s}
.f3{left:44%;bottom:54px;animation-delay:1.4s}
.f4{left:63%;bottom:88px;animation-delay:.5s}
.f5{left:81%;bottom:58px;animation-delay:1.1s}
@keyframes sway{
    from{rotate:-3deg}
    to{rotate:3deg}
}
.reveal{
    margin-top:16px;
    background:#fff9dc;
    border:1px solid #e2c85b;
    border-radius:18px;
    padding:16px 18px;
    min-height:64px;
    text-align:center;
    display:flex;
    align-items:center;
    justify-content:center;
    line-height:1.55;
    color:#5e521f;
    transition:.3s ease;
}
.details{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:12px;
}
.detail{
    border:1px solid #e4c85f;
    background:#fffdf2;
    border-radius:18px;
    padding:18px 14px;
    cursor:pointer;
    text-align:center;
    transition:.2s ease;
}
.detail:hover{transform:translateY(-3px);background:#fff8d4}
.detail .icon{font-size:29px;margin-bottom:8px}
.detail strong{display:block;color:#6a570d;margin-bottom:6px}
.detail span{font-size:14px;color:#776c3d}
.hidden-text{
    display:none;
    margin-top:14px;
    padding:17px;
    border-radius:16px;
    background:#fff7cf;
    border:1px solid #dec25c;
    text-align:center;
    line-height:1.6;
}
.final-btn{
    width:100%;
    border:none;
    padding:16px 20px;
    border-radius:18px;
    background:linear-gradient(90deg,#f5c928,#ffe26d);
    color:#5c4900;
    font-size:17px;
    font-weight:800;
    cursor:pointer;
    transition:.2s ease;
}
.final-btn:hover{transform:translateY(-2px)}
.final{
    display:none;
    margin-top:16px;
    padding:22px;
    border-radius:20px;
    background:linear-gradient(180deg,#fffbea,#fff4b9);
    border:1px solid #dfc153;
    text-align:center;
    font-size:18px;
    line-height:1.7;
}
.petals{
    position:fixed;
    top:-30px;
    pointer-events:none;
    z-index:9999;
    animation:fall 4s linear forwards;
}
@keyframes fall{
    to{transform:translateY(110vh) rotate(540deg);opacity:.85}
}
.small{
    text-align:center;
    margin-top:16px;
    color:#8a7d48;
    font-size:13px;
}
@media(max-width:700px){
    h1{font-size:34px}
    .details{grid-template-columns:1fr}
    .flower .emoji{font-size:54px}
    .f1{left:4%}.f2{left:23%}.f3{left:43%}.f4{left:63%}.f5{left:82%}
}
</style>
</head>
<body>
<div class="wrapper">

<section class="hero">
    <div class="badge">🌻 Para una buena amistad</div>
    <h1>Un detalle amarillo para alegrarte el día</h1>
    <p class="lead">
        No hace falta una fecha especial para recordar que hay personas cuya amistad se valora de verdad.
        Así que estas flores son simplemente para sacarte una sonrisa.
    </p>
</section>

<section class="section">
    <h2>Haz clic en las flores</h2>
    <p class="note">Cada una guarda un pequeño detalle.</p>

    <div class="garden">
        <div class="sun"></div>
        <div class="cloud c1"></div>
        <div class="cloud c2"></div>

        <div class="flower f1" data-msg="🌻 Gracias por esas conversaciones que empiezan con cualquier cosa y terminan arreglando el día.">
            <span class="emoji">🌻</span>
        </div>
        <div class="flower f2" data-msg="🌼 Una buena amistad se nota en la confianza, en las risas y también en los momentos simples.">
            <span class="emoji">🌼</span>
        </div>
        <div class="flower f3" data-msg="🌻 Gracias por sumar buenas energías, buenos consejos y muchas anécdotas.">
            <span class="emoji">🌻</span>
        </div>
        <div class="flower f4" data-msg="🌼 Hay amistades que no necesitan grandes discursos; simplemente se sienten sinceras.">
            <span class="emoji">🌼</span>
        </div>
        <div class="flower f5" data-msg="🌻 Que nunca falten motivos para reír, conversar y seguir creando buenos recuerdos.">
            <span class="emoji">🌻</span>
        </div>
    </div>

    <div class="reveal" id="flowerText">
        Toca una flor y aparecerá su mensaje aquí ✨
    </div>
</section>

<section class="section">
    <h2>Pequeños detalles que valen bastante</h2>
    <p class="note">Puedes abrirlos uno por uno.</p>

    <div class="details">
        <div class="detail" onclick="toggleDetail('d1')">
            <div class="icon">😂</div>
            <strong>Las risas</strong>
            <span>Haz clic para abrir</span>
        </div>
        <div class="detail" onclick="toggleDetail('d2')">
            <div class="icon">☕</div>
            <strong>Las conversaciones</strong>
            <span>Haz clic para abrir</span>
        </div>
        <div class="detail" onclick="toggleDetail('d3')">
            <div class="icon">🤝</div>
            <strong>La confianza</strong>
            <span>Haz clic para abrir</span>
        </div>
    </div>

    <div class="hidden-text" id="d1">
        Hay días normales que terminan siendo buenos recuerdos solo porque hubo una risa en el momento justo.
    </div>
    <div class="hidden-text" id="d2">
        A veces una buena conversación vale más que cualquier plan elaborado.
    </div>
    <div class="hidden-text" id="d3">
        La mejor parte de una buena amistad es poder ser uno mismo sin tener que explicar demasiado.
    </div>
</section>

<section class="section">
    <h2>Y para cerrar...</h2>
    <p class="note">Hay un último detalle.</p>
    <button class="final-btn" onclick="showFinal()">🌻 Ver mensaje final</button>

    <div class="final" id="finalMessage">
        <b>Solo quería dejarte este detalle porque tu amistad se aprecia.</b><br><br>
        Gracias por los buenos momentos, las conversaciones, las ocurrencias y por estar presente de una forma sencilla pero valiosa.<br><br>
        Que sigan viniendo más días tranquilos, más risas y más buenos recuerdos. 🌻
    </div>
</section>

<div class="small">Hecho con buena onda y sin cursilerías 😄</div>
</div>

<script>
document.querySelectorAll('.flower').forEach(f => {
    f.addEventListener('click', () => {
        const box = document.getElementById('flowerText');
        box.style.opacity = "0";
        setTimeout(() => {
            box.innerHTML = f.dataset.msg;
            box.style.opacity = "1";
        }, 140);
    });
});

function toggleDetail(id){
    const all = document.querySelectorAll('.hidden-text');
    all.forEach(x => {
        if(x.id !== id) x.style.display = "none";
    });
    const el = document.getElementById(id);
    el.style.display = el.style.display === "block" ? "none" : "block";
}

function showFinal(){
    const box = document.getElementById('finalMessage');
    box.style.display = "block";

    const symbols = ["🌻","🌼","✨"];
    for(let i=0;i<26;i++){
        const p = document.createElement('div');
        p.className = 'petals';
        p.textContent = symbols[Math.floor(Math.random()*symbols.length)];
        p.style.left = Math.random()*100 + 'vw';
        p.style.fontSize = (16 + Math.random()*13) + 'px';
        p.style.animationDelay = (Math.random()*0.7) + 's';
        document.body.appendChild(p);
        setTimeout(()=>p.remove(),4800);
    }
}
</script>
</body>
</html>
'''

components.html(html, height=1380, scrolling=True)
