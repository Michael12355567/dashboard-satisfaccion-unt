import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flores Amarillas 🌻",
    page_icon="🌻",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown('''
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", Arial, sans-serif;
}
.stApp {
    background: linear-gradient(180deg,#fffdf5 0%,#fff8cf 50%,#fff6da 100%);
}
.block-container {
    max-width: 1200px;
    padding-top: .5rem;
    padding-bottom: 1rem;
}
header, footer, #MainMenu {visibility:hidden;}
iframe {border-radius: 24px;}
</style>
''', unsafe_allow_html=True)

page = r'''
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<style>
:root{
  --yellow:#ffd633;
  --yellow2:#ffe978;
  --gold:#d8a900;
  --brown:#6c5310;
  --cream:#fffaf0;
  --green:#5ea74c;
  --green2:#387f39;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;
  color:#4f4725;
  background:
    radial-gradient(circle at 10% 12%,rgba(255,221,76,.24),transparent 25%),
    radial-gradient(circle at 90% 15%,rgba(255,205,41,.18),transparent 25%),
    linear-gradient(180deg,#fffef8 0%,#fff8ce 45%,#fff7dc 100%);
  overflow-x:hidden;
  font-family:"Segoe UI",Arial,sans-serif;
}
.petal{
  position:fixed;
  top:-40px;
  pointer-events:none;
  z-index:20;
  opacity:.9;
  animation:fall linear forwards;
  filter:drop-shadow(0 4px 5px rgba(0,0,0,.08));
}
@keyframes fall{
  0%{transform:translateY(-20px) rotate(0deg) translateX(0)}
  50%{transform:translateY(52vh) rotate(180deg) translateX(30px)}
  100%{transform:translateY(110vh) rotate(420deg) translateX(-25px);opacity:.2}
}
.hero{
  min-height:92vh;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:40px 28px 55px;
  position:relative;
}
.hero:before{
  content:"";
  position:absolute;
  inset:0;
  background-image:
    radial-gradient(circle at 20% 20%, rgba(255,255,255,.95) 0 2px, transparent 3px),
    radial-gradient(circle at 75% 28%, rgba(255,255,255,.9) 0 2px, transparent 3px),
    radial-gradient(circle at 60% 72%, rgba(255,255,255,.8) 0 2px, transparent 3px);
  background-size:170px 170px, 220px 220px, 190px 190px;
  opacity:.6;
  pointer-events:none;
}
.hero-card{
  width:min(1080px,96vw);
  display:grid;
  grid-template-columns:1.05fr .95fr;
  gap:28px;
  align-items:center;
  padding:34px;
  border-radius:36px;
  background:rgba(255,255,255,.72);
  border:1px solid rgba(222,187,44,.45);
  box-shadow:0 30px 70px rgba(127,91,0,.15), inset 0 1px 0 rgba(255,255,255,.9);
  backdrop-filter:blur(18px);
  position:relative;
  overflow:hidden;
}
.hero-card:after{
  content:"";
  position:absolute;
  width:240px;height:240px;
  right:-70px;top:-80px;
  border-radius:50%;
  background:radial-gradient(circle,rgba(255,221,72,.35),transparent 70%);
  pointer-events:none;
}
.kicker{
  display:inline-flex;
  gap:8px;
  align-items:center;
  padding:8px 13px;
  background:#fff3ab;
  border:1px solid #e3c656;
  border-radius:999px;
  font-weight:800;
  color:#6d5808;
  font-size:14px;
  letter-spacing:.3px;
}
h1{
  margin:16px 0 12px;
  font-size:clamp(42px,6vw,76px);
  line-height:.98;
  color:#65500b;
  letter-spacing:-2px;
}
.highlight{
  display:inline-block;
  background:linear-gradient(90deg,#d4a900,#ffcf2a,#b98d00);
  -webkit-background-clip:text;
  background-clip:text;
  color:transparent;
}
.hero-text{
  font-size:19px;
  line-height:1.7;
  color:#706638;
  max-width:590px;
}
.hero-btn{
  margin-top:20px;
  display:inline-flex;
  align-items:center;
  gap:10px;
  border:none;
  cursor:pointer;
  border-radius:18px;
  padding:14px 20px;
  font-size:16px;
  font-weight:800;
  color:#594500;
  background:linear-gradient(90deg,#ffd027,#ffe878);
  box-shadow:0 10px 26px rgba(159,119,0,.22);
  transition:.25s ease;
}
.hero-btn:hover{transform:translateY(-3px) scale(1.01)}
.scroll-note{
  margin-top:13px;
  font-size:13px;
  color:#91834a;
}
.bouquet-wrap{
  min-height:500px;
  display:flex;
  align-items:center;
  justify-content:center;
  position:relative;
}
.glow{
  position:absolute;
  width:360px;height:360px;
  border-radius:50%;
  background:radial-gradient(circle,rgba(255,220,54,.42),rgba(255,236,138,.12) 55%,transparent 72%);
  filter:blur(8px);
  animation:pulse 3s ease-in-out infinite alternate;
}
@keyframes pulse{from{transform:scale(.95)}to{transform:scale(1.08)}}
.bouquet{
  position:relative;
  width:430px;
  height:470px;
  z-index:2;
}
.stem{
  position:absolute;
  width:7px;
  height:245px;
  background:linear-gradient(var(--green),var(--green2));
  bottom:70px;
  left:50%;
  transform-origin:bottom center;
  border-radius:8px;
}
.s1{transform:rotate(-18deg);left:44%}
.s2{transform:rotate(-8deg);left:48%}
.s3{transform:rotate(0deg);left:51%}
.s4{transform:rotate(9deg);left:54%}
.s5{transform:rotate(18deg);left:57%}
.s6{transform:rotate(-28deg);left:42%;height:220px}
.s7{transform:rotate(28deg);left:59%;height:220px}
.wrap-paper{
  position:absolute;
  left:50%;
  bottom:15px;
  width:210px;
  height:170px;
  transform:translateX(-50%);
  background:linear-gradient(145deg,#fff6d6,#f0d889);
  clip-path:polygon(8% 0,92% 0,72% 100%,28% 100%);
  border-radius:18px;
  box-shadow:0 20px 35px rgba(91,66,0,.18);
}
.ribbon{
  position:absolute;
  left:50%;
  bottom:78px;
  transform:translateX(-50%);
  width:95px;height:18px;
  border-radius:20px;
  background:#d2aa20;
  box-shadow:0 4px 8px rgba(0,0,0,.08);
}
.flower{
  position:absolute;
  width:104px;height:104px;
  cursor:pointer;
  transition:.28s ease;
  filter:drop-shadow(0 8px 8px rgba(90,66,0,.15));
}
.flower:hover{transform:scale(1.08) rotate(3deg)}
.flower.bloom{animation:bloom .55s ease}
@keyframes bloom{
  0%{transform:scale(.75) rotate(-8deg)}
  60%{transform:scale(1.18) rotate(5deg)}
  100%{transform:scale(1)}
}
.center{
  position:absolute;
  width:40px;height:40px;
  left:32px;top:32px;
  background:radial-gradient(circle at 35% 30%,#9d6c1a,#6f430d 70%);
  border-radius:50%;
  z-index:5;
  box-shadow:inset 0 0 0 3px rgba(255,255,255,.08);
}
.pet{
  position:absolute;
  left:35px;top:18px;
  width:34px;height:48px;
  border-radius:55% 55% 50% 50%;
  background:linear-gradient(180deg,#ffe76c,#ffc91e);
  transform-origin:17px 34px;
  box-shadow:0 2px 5px rgba(0,0,0,.05);
}
.p1{transform:rotate(0deg) translateY(-14px)}
.p2{transform:rotate(45deg) translateY(-14px)}
.p3{transform:rotate(90deg) translateY(-14px)}
.p4{transform:rotate(135deg) translateY(-14px)}
.p5{transform:rotate(180deg) translateY(-14px)}
.p6{transform:rotate(225deg) translateY(-14px)}
.p7{transform:rotate(270deg) translateY(-14px)}
.p8{transform:rotate(315deg) translateY(-14px)}
.f1{left:54px;top:150px}
.f2{left:135px;top:72px}
.f3{left:230px;top:120px}
.f4{left:166px;top:180px}
.f5{left:272px;top:50px}
.f6{left:45px;top:46px}
.f7{left:286px;top:190px}
.section{
  width:min(1050px,92vw);
  margin:0 auto 28px;
  padding:30px;
  border-radius:30px;
  background:rgba(255,255,255,.78);
  border:1px solid rgba(223,190,58,.45);
  box-shadow:0 18px 42px rgba(113,80,0,.10);
  backdrop-filter:blur(12px);
}
.section h2{
  margin:0 0 8px;
  text-align:center;
  color:#66520c;
  font-size:32px;
}
.section .sub{
  margin:0 auto 24px;
  text-align:center;
  color:#7a7044;
  max-width:700px;
  line-height:1.6;
}
.message-box{
  min-height:92px;
  border-radius:22px;
  padding:20px;
  background:linear-gradient(180deg,#fffbea,#fff5bd);
  border:1px solid #e4c95f;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  line-height:1.65;
  font-size:17px;
  color:#5d5122;
  box-shadow:inset 0 1px 0 white;
  transition:.25s ease;
}
.cards{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:16px;
}
.card{
  position:relative;
  min-height:190px;
  overflow:hidden;
  border-radius:24px;
  padding:20px;
  background:linear-gradient(160deg,rgba(255,255,255,.96),rgba(255,247,205,.9));
  border:1px solid #e7ce6b;
  cursor:pointer;
  transition:.25s ease;
  box-shadow:0 12px 28px rgba(108,79,0,.09);
}
.card:hover{transform:translateY(-6px)}
.card .icon{font-size:36px;margin-bottom:14px}
.card h3{margin:0 0 8px;color:#66520b}
.card p{margin:0;line-height:1.55;color:#7b7146}
.card .more{margin-top:14px;font-size:13px;font-weight:800;color:#a07800}
.card-reveal{
  position:absolute;
  inset:0;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:22px;
  text-align:center;
  line-height:1.65;
  background:linear-gradient(145deg,#fff4aa,#fff9dc);
  transform:translateY(102%);
  transition:.35s ease;
}
.card.open .card-reveal{transform:translateY(0)}
.quote{
  font-family:Georgia,serif;
  font-size:26px;
  line-height:1.55;
  text-align:center;
  color:#655615;
  max-width:820px;
  margin:0 auto;
}
.final-btn{
  display:block;
  width:min(420px,100%);
  margin:22px auto 0;
  border:none;
  border-radius:20px;
  padding:16px 22px;
  cursor:pointer;
  font-size:17px;
  font-weight:900;
  color:#5d4800;
  background:linear-gradient(90deg,#ffc91e,#ffe67a);
  box-shadow:0 12px 28px rgba(145,103,0,.22);
  transition:.25s ease;
}
.final-btn:hover{transform:translateY(-3px) scale(1.02)}
.final-message{
  display:none;
  margin-top:20px;
  padding:25px;
  border-radius:22px;
  background:linear-gradient(180deg,#fffdf3,#fff1a9);
  border:1px solid #e2c45b;
  text-align:center;
  font-size:18px;
  line-height:1.7;
  color:#5d5124;
}
.signature{
  margin-top:12px;
  text-align:center;
  color:#8a7a3f;
  font-size:13px;
}
@media(max-width:850px){
  .hero-card{grid-template-columns:1fr;padding:24px}
  .bouquet-wrap{min-height:430px;transform:scale(.88)}
  .cards{grid-template-columns:1fr}
  h1{text-align:center}
  .hero-text,.hero-left{text-align:center}
  .kicker{margin:auto}
}
</style>
</head>
<body>

<section class="hero">
  <div class="hero-card">
    <div class="hero-left">
      <div class="kicker">🌻 PARA UNA BUENA AMISTAD</div>
      <h1>Hoy te dejo un poco de <span class="highlight">amarillo</span></h1>
      <div class="hero-text">
        Porque hay amistades que hacen los días más ligeros, las conversaciones más entretenidas
        y los momentos simples mucho mejores.
      </div>
      <button class="hero-btn" onclick="document.getElementById('detalle').scrollIntoView({behavior:'smooth'})">
        Ver el detalle ✨
      </button>
      <div class="scroll-note">Tip: toca también las flores del ramo 🌻</div>
    </div>

    <div class="bouquet-wrap">
      <div class="glow"></div>
      <div class="bouquet">
        <div class="stem s1"></div><div class="stem s2"></div><div class="stem s3"></div>
        <div class="stem s4"></div><div class="stem s5"></div><div class="stem s6"></div><div class="stem s7"></div>

        <div class="flower f1" data-msg="Una flor por cada conversación que terminó siendo mejor de lo esperado.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>
        <div class="flower f2" data-msg="Por las risas que aparecen justo cuando más hacen falta.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>
        <div class="flower f3" data-msg="Por esos planes sencillos que terminan siendo buenos recuerdos.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>
        <div class="flower f4" data-msg="Por la confianza de poder hablar sin tener que explicar demasiado.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>
        <div class="flower f5" data-msg="Por esos mensajes inesperados que terminan alegrando el día.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>
        <div class="flower f6" data-msg="Por estar presente de una forma sencilla, pero valiosa.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>
        <div class="flower f7" data-msg="Y por todos los buenos momentos que todavía faltan por llegar.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>

        <div class="wrap-paper"></div>
        <div class="ribbon"></div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="detalle">
  <h2>Un ramo con pequeños mensajes</h2>
  <p class="sub">Toca cualquier flor del ramo de arriba y aquí aparecerá lo que guarda.</p>
  <div class="message-box" id="flowerMessage">
    🌻 Cada flor tiene algo distinto que decir.
  </div>
</section>

<section class="section">
  <h2>Cosas simples que hacen grande una amistad</h2>
  <p class="sub">Haz clic en cada tarjeta para descubrir el mensaje completo.</p>
  <div class="cards">
    <div class="card" onclick="this.classList.toggle('open')">
      <div class="icon">😂</div>
      <h3>Las risas</h3>
      <p>Porque a veces una tontería basta para cambiar por completo el día.</p>
      <div class="more">Toca para abrir</div>
      <div class="card-reveal">Las mejores risas suelen aparecer sin planearlas. Y cuando hay confianza, cualquier momento sencillo se vuelve una anécdota.</div>
    </div>
    <div class="card" onclick="this.classList.toggle('open')">
      <div class="icon">☕</div>
      <h3>Las conversaciones</h3>
      <p>Esas que empiezan con “te cuento algo” y terminan hablando de todo.</p>
      <div class="more">Toca para abrir</div>
      <div class="card-reveal">Una buena conversación no necesita un lugar especial. A veces basta tiempo, confianza y ganas de compartir lo que uno piensa.</div>
    </div>
    <div class="card" onclick="this.classList.toggle('open')">
      <div class="icon">🤝</div>
      <h3>La buena onda</h3>
      <p>Estar, apoyar y sumar sin hacer demasiado ruido.</p>
      <div class="more">Toca para abrir</div>
      <div class="card-reveal">Las amistades que valen no siempre están en grandes momentos; muchas veces se notan en los detalles pequeños y constantes.</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="quote">
    “No hace falta una fecha especial para tener un detalle con alguien cuya amistad realmente se aprecia.”
  </div>
  <button class="final-btn" onclick="showFinal()">🌻 Abrir el último detalle</button>
  <div class="final-message" id="finalMessage">
    <b>Esto es simplemente para ti.</b><br><br>
    Gracias por las conversaciones, las risas, la confianza y por esos momentos que,
    sin planearlos demasiado, terminan siendo los mejores.<br><br>
    Que nunca falten buenas historias, buenos planes y razones para seguir sonriendo. 🌻✨
  </div>
  <div class="signature">Un detalle sencillo para una amistad que se valora.</div>
</section>

<script>
function spawnPetals(amount=18){
  const symbols=["🌻","🌼","✨","💛"];
  for(let i=0;i<amount;i++){
    const el=document.createElement("div");
    el.className="petal";
    el.textContent=symbols[Math.floor(Math.random()*symbols.length)];
    el.style.left=(Math.random()*100)+"vw";
    el.style.fontSize=(14+Math.random()*18)+"px";
    el.style.animationDuration=(3.4+Math.random()*2.8)+"s";
    el.style.animationDelay=(Math.random()*.7)+"s";
    document.body.appendChild(el);
    setTimeout(()=>el.remove(),7000);
  }
}
spawnPetals(10);

document.querySelectorAll(".flower").forEach(f=>{
  f.addEventListener("click",()=>{
    f.classList.remove("bloom");
    void f.offsetWidth;
    f.classList.add("bloom");
    const box=document.getElementById("flowerMessage");
    box.style.opacity="0";
    setTimeout(()=>{
      box.innerHTML="🌻 "+f.dataset.msg;
      box.style.opacity="1";
    },140);
    spawnPetals(7);
  });
});

function showFinal(){
  document.getElementById("finalMessage").style.display="block";
  spawnPetals(40);
  setTimeout(()=>{
    document.getElementById("finalMessage").scrollIntoView({behavior:"smooth",block:"center"});
  },120);
}
</script>
</body>
</html>
'''

components.html(page, height=2200, scrolling=True)
