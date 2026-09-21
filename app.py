import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flores Amarillas - Modo Amistad",
    page_icon="🌻",
    layout="centered"
)

st.markdown('''
<style>
    .stApp {
        background:
        radial-gradient(circle at 15% 10%, rgba(255,230,74,.35), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(255,194,0,.20), transparent 23%),
        linear-gradient(180deg, #fffef6 0%, #fff7c7 100%);
    }
    .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }
    .hero {
        text-align: center;
        background: rgba(255,255,255,.78);
        border: 2px solid #f1d158;
        border-radius: 28px;
        padding: 24px 20px;
        box-shadow: 0 14px 36px rgba(116, 88, 0, .10);
        margin-bottom: 18px;
    }
    .hero h1 {
        margin: 0;
        color: #6c5600;
        font-size: 2.7rem;
    }
    .hero p {
        color: #6b623d;
        font-size: 1.08rem;
        margin: 10px 0 0 0;
    }
    .tag {
        display:inline-block;
        background:#fff0a3;
        border:1px solid #e1be35;
        color:#6c5600;
        padding:6px 12px;
        border-radius:999px;
        font-weight:700;
        margin-bottom:10px;
    }
    footer, #MainMenu, header {visibility:hidden;}
</style>
''', unsafe_allow_html=True)

st.markdown('''
<div class="hero">
    <div class="tag">🌻 MODO AMIGOS ACTIVADO</div>
    <h1>Un detalle amarillo para ti</h1>
    <p>No es una carta romántica 😄. Es un mini juego para recordarte que una buena amistad también se celebra.</p>
</div>
''', unsafe_allow_html=True)

interactive_html = r'''
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
*{box-sizing:border-box}
body{
    margin:0;
    font-family:Arial, Helvetica, sans-serif;
    background:transparent;
    color:#4f471f;
}
.panel{
    background:rgba(255,255,255,.92);
    border:2px solid #efd04f;
    border-radius:26px;
    padding:22px;
    box-shadow:0 12px 28px rgba(103,81,0,.10);
    margin-bottom:18px;
}
h2{
    margin:0 0 8px 0;
    text-align:center;
    color:#6a5400;
}
.sub{
    text-align:center;
    margin:0 0 18px 0;
    color:#766b3c;
}
.counter{
    text-align:center;
    font-weight:bold;
    margin:10px 0 16px;
    font-size:18px;
    color:#735c00;
}
.garden{
    position:relative;
    height:300px;
    overflow:hidden;
    border-radius:22px;
    background:linear-gradient(#dff3ff 0%,#fff6b7 70%);
    border:1px solid #e4cc63;
}
.ground{
    position:absolute;
    left:-5%;right:-5%;bottom:-18px;
    height:95px;
    background:linear-gradient(#91cf68,#6baa49);
    border-radius:50% 50% 0 0;
}
.flower{
    position:absolute;
    font-size:58px;
    cursor:pointer;
    user-select:none;
    transition:transform .15s ease, opacity .2s ease;
    filter:drop-shadow(0 5px 5px rgba(0,0,0,.12));
    animation:sway 2.6s ease-in-out infinite alternate;
}
.flower:hover{transform:scale(1.15) rotate(5deg)}
.flower.clicked{
    animation:pop .35s ease forwards;
}
@keyframes sway{from{rotate:-4deg}to{rotate:4deg}}
@keyframes pop{
    0%{transform:scale(1)}
    50%{transform:scale(1.35)}
    100%{transform:scale(.2);opacity:0}
}
.f1{left:7%;bottom:48px}
.f2{left:22%;bottom:78px;animation-delay:.3s}
.f3{left:39%;bottom:42px;animation-delay:.7s}
.f4{left:57%;bottom:88px;animation-delay:1.1s}
.f5{left:74%;bottom:50px;animation-delay:.5s}
.f6{left:87%;bottom:85px;animation-delay:1.5s}
.cloud{
    position:absolute;
    width:90px;height:28px;
    background:white;
    border-radius:30px;
    opacity:.9;
}
.cloud:before,.cloud:after{
    content:"";position:absolute;background:white;border-radius:50%;
}
.cloud:before{width:38px;height:38px;left:12px;top:-17px}
.cloud:after{width:48px;height:48px;left:38px;top:-23px}
.c1{top:48px;left:8%}
.c2{top:70px;right:13%;transform:scale(.8)}
.sun{
    position:absolute;right:32px;top:22px;width:68px;height:68px;
    border-radius:50%;background:#ffe44e;
    box-shadow:0 0 35px rgba(255,206,0,.45);
}
.messagebox{
    margin-top:14px;
    min-height:58px;
    padding:14px;
    border-radius:16px;
    background:#fff7cf;
    text-align:center;
    font-weight:700;
    color:#5f500e;
    border:1px dashed #d1ae25;
}
.cards{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:12px;
}
.card{
    min-height:125px;
    border-radius:18px;
    background:linear-gradient(145deg,#ffe25a,#ffd337);
    border:0;
    padding:14px;
    cursor:pointer;
    font-weight:800;
    color:#5b4700;
    box-shadow:0 8px 16px rgba(102,79,0,.10);
    transition:.2s ease;
}
.card:hover{transform:translateY(-4px)}
.card.open{
    background:#fff8d8;
    font-weight:700;
}
.quiz{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:10px;
}
.choice{
    border:1px solid #dfbf39;
    background:#fffbed;
    padding:13px;
    border-radius:14px;
    cursor:pointer;
    font-weight:700;
    color:#5c511d;
}
.choice:hover{background:#fff1a6}
.result{
    margin-top:12px;
    padding:13px;
    border-radius:14px;
    background:#f7ffd9;
    border:1px solid #b8cf62;
    display:none;
    text-align:center;
    font-weight:700;
}
.bigbtn{
    width:100%;
    padding:16px;
    border:0;
    border-radius:18px;
    cursor:pointer;
    background:linear-gradient(90deg,#ffce22,#ffe66d);
    color:#544000;
    font-size:18px;
    font-weight:800;
    box-shadow:0 10px 20px rgba(117,87,0,.15);
}
.final{
    display:none;
    margin-top:15px;
    text-align:center;
    font-size:19px;
    line-height:1.6;
    background:#fff8d1;
    border-radius:18px;
    padding:18px;
    border:1px solid #e0bd35;
}
.confetti{
    position:fixed;
    top:-20px;
    font-size:22px;
    pointer-events:none;
    animation:fall 2.8s linear forwards;
    z-index:9999;
}
@keyframes fall{
    to{transform:translateY(110vh) rotate(720deg);opacity:.9}
}
@media(max-width:650px){
    .cards{grid-template-columns:1fr}
    .quiz{grid-template-columns:1fr}
    .flower{font-size:48px}
}
</style>
</head>
<body>

<div class="panel">
    <h2>🌻 1. Atrapa las flores</h2>
    <p class="sub">Haz clic en las 6 flores. Cada una guarda una frase de amistad.</p>
    <div class="counter">Flores encontradas: <span id="count">0</span>/6</div>

    <div class="garden">
        <div class="sun"></div>
        <div class="cloud c1"></div>
        <div class="cloud c2"></div>
        <div class="flower f1" data-msg="Amigo de verdad: aparece para sumar, no para complicar 😎">🌻</div>
        <div class="flower f2" data-msg="Gracias por las risas que salen de la nada 😂">🌼</div>
        <div class="flower f3" data-msg="Una buena amistad hace más ligeros los días pesados 💪">🌻</div>
        <div class="flower f4" data-msg="Que nunca falten planes simples que terminan siendo buenos recuerdos 🙌">🌼</div>
        <div class="flower f5" data-msg="Aquí tienes una flor por aguantar mis ocurrencias 😅">🌻</div>
        <div class="flower f6" data-msg="Las amistades sinceras valen más que cualquier regalo 💛">🌼</div>
        <div class="ground"></div>
    </div>
    <div class="messagebox" id="flowerMessage">👇 Toca una flor para descubrir su mensaje.</div>
</div>

<div class="panel">
    <h2>🎁 2. Elige una tarjeta sorpresa</h2>
    <p class="sub">No sabes qué te tocará hasta hacer clic.</p>
    <div class="cards">
        <button class="card" onclick="openCard(this,0)">❓<br><br>ABRIR</button>
        <button class="card" onclick="openCard(this,1)">❓<br><br>ABRIR</button>
        <button class="card" onclick="openCard(this,2)">❓<br><br>ABRIR</button>
    </div>
</div>

<div class="panel">
    <h2>😄 3. Mini reto de amistad</h2>
    <p class="sub">Elige la respuesta que más nos representa.</p>
    <div class="quiz">
        <button class="choice" onclick="quiz('A')">😂 Reírnos por cualquier tontería</button>
        <button class="choice" onclick="quiz('B')">🍟 Comer algo y conversar horas</button>
        <button class="choice" onclick="quiz('C')">📱 Mandarnos memes sin contexto</button>
        <button class="choice" onclick="quiz('D')">🤝 Apoyarnos cuando toca</button>
    </div>
    <div class="result" id="quizResult"></div>
</div>

<div class="panel">
    <h2>✨ 4. Botón final</h2>
    <p class="sub">Después de completar el juego, este botón tiene la conclusión.</p>
    <button class="bigbtn" onclick="finale()">🌻 HACER CLIC AQUÍ</button>
    <div class="final" id="finalMsg">
        <b>Resultado oficial:</b><br><br>
        Tienes una amistad que se aprecia bastante 😎🌻<br>
        Gracias por las risas, las conversaciones, los consejos y los buenos momentos.<br>
        <b>Que sigan viniendo más anécdotas y menos estrés.</b> 🙌
    </div>
</div>

<script>
let count = 0;
const phrases = [
    "Vale por un café y una conversación larga ☕",
    "Cupón oficial para un plan improvisado 😎",
    "Premio: una buena dosis de risas 😂"
];

document.querySelectorAll('.flower').forEach(flower => {
    flower.addEventListener('click', () => {
        if (flower.classList.contains('clicked')) return;
        flower.classList.add('clicked');
        count++;
        document.getElementById('count').textContent = count;
        document.getElementById('flowerMessage').textContent = flower.dataset.msg;

        if (count === 6) {
            setTimeout(() => {
                document.getElementById('flowerMessage').innerHTML =
                "🎉 ¡Completaste las 6! Diagnóstico: <b>amistad de calidad desbloqueada</b>.";
            }, 350);
        }
    });
});

function openCard(btn, i){
    if(btn.classList.contains('open')) return;
    btn.classList.add('open');
    btn.innerHTML = phrases[i];
}

function quiz(opt){
    const r = document.getElementById('quizResult');
    const answers = {
        A:"😂 Buena elección. Si hay risas, ya hay buen plan.",
        B:"🍟 Conversar con algo para picar: clásico infalible.",
        C:"📱 Los memes también son una forma de comunicación oficial entre amigos.",
        D:"🤝 Esta es de las importantes: estar cuando realmente se necesita."
    };
    r.style.display = "block";
    r.textContent = answers[opt];
}

function finale(){
    document.getElementById('finalMsg').style.display = "block";
    const emojis = ["🌻","✨","💛","🌼","🎉"];
    for(let i=0;i<45;i++){
        const c=document.createElement('div');
        c.className='confetti';
        c.textContent=emojis[Math.floor(Math.random()*emojis.length)];
        c.style.left=Math.random()*100+'vw';
        c.style.animationDelay=(Math.random()*0.8)+'s';
        c.style.fontSize=(16+Math.random()*18)+'px';
        document.body.appendChild(c);
        setTimeout(()=>c.remove(),3800);
    }
}
</script>
</body>
</html>
'''

components.html(interactive_html, height=1320, scrolling=True)

st.markdown(
    "<div style='text-align:center;color:#72662f;font-size:.92rem;margin-top:12px;'>🌻 Hecho para una buena amistad, sin cursilerías 😄</div>",
    unsafe_allow_html=True
)
