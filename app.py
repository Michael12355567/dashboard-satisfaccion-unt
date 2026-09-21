import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Un detalle amarillo 🌻",
    page_icon="🌻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp{
    background:linear-gradient(180deg,#fffdf5,#fff4b8);
}
.block-container{
    max-width:1050px;
    padding-top:.35rem;
    padding-bottom:.35rem;
}
header,footer,#MainMenu{visibility:hidden}
iframe{border-radius:26px}
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<style>
*{box-sizing:border-box}
body{
  margin:0;
  font-family:Segoe UI,Arial,sans-serif;
  background:transparent;
  color:#534815;
  overflow-x:hidden;
}
.shell{
  width:min(980px,96vw);
  margin:0 auto;
  padding:10px 0 14px;
}
.card{
  position:relative;
  overflow:hidden;
  min-height:760px;
  border-radius:32px;
  background:
    radial-gradient(circle at 18% 13%,rgba(255,255,255,.95),transparent 24%),
    radial-gradient(circle at 84% 20%,rgba(255,224,91,.35),transparent 27%),
    linear-gradient(160deg,#fffef8 0%,#fff4ae 100%);
  border:1px solid #e4c64d;
  box-shadow:0 24px 58px rgba(115,83,0,.16);
}
.spark{
  position:absolute;
  pointer-events:none;
  opacity:.7;
  animation:float 3s ease-in-out infinite alternate;
}
.s1{left:7%;top:9%;font-size:20px}
.s2{right:8%;top:12%;font-size:25px;animation-delay:.8s}
.s3{left:12%;bottom:18%;font-size:18px;animation-delay:1.4s}
.s4{right:12%;bottom:17%;font-size:22px;animation-delay:.4s}
@keyframes float{
  from{transform:translateY(0) rotate(-5deg)}
  to{transform:translateY(-10px) rotate(8deg)}
}

.top{
  text-align:center;
  padding:26px 26px 6px;
}
.badge{
  display:inline-block;
  background:#fff0a0;
  border:1px solid #dfbe39;
  padding:7px 13px;
  border-radius:999px;
  font-size:13px;
  font-weight:800;
  letter-spacing:.2px;
}
h1{
  margin:12px 0 6px;
  font-size:clamp(34px,5vw,58px);
  line-height:1;
  color:#665008;
}
.top p{
  margin:0 auto;
  max-width:700px;
  font-size:16px;
  line-height:1.55;
  color:#776a35;
}

.stage{
  position:relative;
  height:420px;
  margin:4px 20px 0;
  border-radius:28px;
  overflow:hidden;
  background:
    linear-gradient(180deg,#eaf8ff 0%,#fff7c4 68%,#d8ecad 69%,#8fbf5c 100%);
  border:1px solid #dfc65e;
}
.sun{
  position:absolute;right:38px;top:25px;
  width:72px;height:72px;border-radius:50%;
  background:#ffe052;
  box-shadow:0 0 38px rgba(255,203,0,.42);
}
.cloud{
  position:absolute;width:88px;height:27px;background:#fff;border-radius:30px;opacity:.9;
}
.cloud:before,.cloud:after{
  content:"";position:absolute;background:#fff;border-radius:50%;
}
.cloud:before{width:38px;height:38px;left:12px;top:-15px}
.cloud:after{width:48px;height:48px;left:38px;top:-22px}
.c1{left:9%;top:55px}
.c2{right:18%;top:92px;transform:scale(.78)}

.bouquet{
  position:absolute;
  left:50%;bottom:28px;
  width:420px;height:340px;
  transform:translateX(-50%);
}
.paper{
  position:absolute;
  left:50%;bottom:0;
  width:185px;height:140px;
  transform:translateX(-50%);
  clip-path:polygon(7% 0,93% 0,73% 100%,27% 100%);
  background:linear-gradient(145deg,#fff7dc,#e9cf7d);
  box-shadow:0 18px 30px rgba(100,70,0,.14);
  z-index:2;
}
.ribbon{
  position:absolute;left:50%;bottom:58px;
  transform:translateX(-50%);
  width:88px;height:16px;border-radius:20px;
  background:#cba21d;z-index:3;
}
.stem{
  position:absolute;
  bottom:65px;left:50%;
  width:6px;height:190px;border-radius:8px;
  background:linear-gradient(#65ad4c,#397b37);
  transform-origin:bottom center;
}
.st1{transform:rotate(-26deg)}
.st2{transform:rotate(-16deg)}
.st3{transform:rotate(-7deg)}
.st4{transform:rotate(2deg)}
.st5{transform:rotate(12deg)}
.st6{transform:rotate(22deg)}

.flower{
  position:absolute;
  width:92px;height:92px;
  left:50%;top:195px;
  transform:translate(-50%,-50%) scale(.42);
  opacity:0;
  cursor:pointer;
  transition:
    left .75s cubic-bezier(.2,.9,.2,1),
    top .75s cubic-bezier(.2,.9,.2,1),
    transform .75s cubic-bezier(.2,.9,.2,1),
    opacity .45s ease;
  z-index:5;
  filter:drop-shadow(0 8px 8px rgba(84,60,0,.13));
}
.open .f1{left:20%;top:175px;transform:translate(-50%,-50%) scale(1);opacity:1}
.open .f2{left:34%;top:100px;transform:translate(-50%,-50%) scale(.94);opacity:1}
.open .f3{left:49%;top:155px;transform:translate(-50%,-50%) scale(1.06);opacity:1}
.open .f4{left:64%;top:92px;transform:translate(-50%,-50%) scale(.96);opacity:1}
.open .f5{left:79%;top:170px;transform:translate(-50%,-50%) scale(1);opacity:1}
.open .f6{left:50%;top:58px;transform:translate(-50%,-50%) scale(.9);opacity:1}

.pet{
  position:absolute;
  left:31px;top:13px;
  width:30px;height:43px;
  background:linear-gradient(#ffe875,#ffc918);
  border-radius:55% 55% 48% 48%;
  transform-origin:15px 33px;
}
.p1{transform:rotate(0deg) translateY(-12px)}
.p2{transform:rotate(45deg) translateY(-12px)}
.p3{transform:rotate(90deg) translateY(-12px)}
.p4{transform:rotate(135deg) translateY(-12px)}
.p5{transform:rotate(180deg) translateY(-12px)}
.p6{transform:rotate(225deg) translateY(-12px)}
.p7{transform:rotate(270deg) translateY(-12px)}
.p8{transform:rotate(315deg) translateY(-12px)}
.center{
  position:absolute;
  left:30px;top:30px;
  width:32px;height:32px;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#a56e17,#6e430c 72%);
  z-index:4;
}
.flower:hover{filter:drop-shadow(0 10px 12px rgba(84,60,0,.2))}
.flower:active{scale:.96}

.open-btn{
  position:absolute;
  left:50%;bottom:18px;
  transform:translateX(-50%);
  z-index:10;
  border:none;
  padding:13px 19px;
  border-radius:17px;
  background:linear-gradient(90deg,#ffca19,#ffe56d);
  color:#594500;
  font-weight:900;
  cursor:pointer;
  box-shadow:0 10px 22px rgba(116,82,0,.2);
  transition:.2s ease;
}
.open-btn:hover{transform:translateX(-50%) translateY(-2px)}
.open-btn.hide{opacity:0;pointer-events:none}

.bottom{
  display:grid;
  grid-template-columns:1.25fr .75fr;
  gap:12px;
  padding:12px 20px 20px;
}
.message{
  min-height:110px;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  padding:18px;
  border-radius:20px;
  background:rgba(255,255,255,.8);
  border:1px solid #e3c759;
  line-height:1.6;
  font-size:16px;
  transition:.25s ease;
}
.final{
  min-height:110px;
  border-radius:20px;
  border:1px solid #e3c759;
  background:linear-gradient(145deg,#fff8ce,#fffdf0);
  padding:14px;
  display:flex;
  flex-direction:column;
  justify-content:center;
  text-align:center;
}
.final button{
  border:none;
  padding:12px 14px;
  border-radius:15px;
  background:#f2c82a;
  color:#574300;
  font-weight:900;
  cursor:pointer;
}
.finalText{
  display:none;
  margin-top:10px;
  font-size:14px;
  line-height:1.5;
  color:#6a5d2a;
}
.confetti{
  position:fixed;
  top:-30px;
  z-index:999;
  pointer-events:none;
  animation:drop 3.5s linear forwards;
}
@keyframes drop{
  to{transform:translateY(110vh) rotate(520deg);opacity:.2}
}

@media(max-width:760px){
  .card{min-height:820px}
  .stage{height:440px;margin:4px 10px 0}
  .bouquet{width:340px;transform:translateX(-50%) scale(.9);transform-origin:bottom center}
  .bottom{grid-template-columns:1fr;padding:10px}
  .top{padding:22px 14px 6px}
  .top p{font-size:15px}
}
</style>
</head>
<body>
<div class="shell">
  <div class="card">
    <div class="spark s1">✨</div>
    <div class="spark s2">🌼</div>
    <div class="spark s3">✨</div>
    <div class="spark s4">🌻</div>

    <div class="top">
      <div class="badge">🌻 UN DETALLE DE AMISTAD</div>
      <h1>Un poquito de amarillo para ti</h1>
      <p>
        Solo porque sí. Porque las buenas amistades también merecen detalles que alegren el día.
      </p>
    </div>

    <div class="stage">
      <div class="sun"></div>
      <div class="cloud c1"></div>
      <div class="cloud c2"></div>

      <div class="bouquet" id="bouquet">
        <div class="stem st1"></div><div class="stem st2"></div><div class="stem st3"></div>
        <div class="stem st4"></div><div class="stem st5"></div><div class="stem st6"></div>

        <div class="flower f1" data-msg="🌻 Gracias por esas conversaciones que hacen el día más ligero.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>
        <div class="flower f2" data-msg="😂 Por todas esas risas que salen de la nada y terminan siendo lo mejor del momento.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>
        <div class="flower f3" data-msg="☕ Por esos ratos simples que, sin planearlos, terminan siendo buenos recuerdos.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>
        <div class="flower f4" data-msg="🤝 Porque una buena amistad se nota en la confianza y en saber que se puede contar con alguien.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>
        <div class="flower f5" data-msg="✨ Por esos mensajes o ocurrencias que llegan justo cuando hacía falta distraerse un rato.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>
        <div class="flower f6" data-msg="🌼 Y por todos los buenos momentos que todavía faltan por venir.">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </div>

        <div class="paper"></div>
        <div class="ribbon"></div>
      </div>

      <button class="open-btn" id="openBtn" onclick="openBouquet()">🌻 Abrir detalle</button>
    </div>

    <div class="bottom">
      <div class="message" id="messageBox">
        Primero abre el ramo. Luego toca cualquiera de las flores ✨
      </div>

      <div class="final">
        <button onclick="showFinal()">Ver último detalle 💛</button>
        <div class="finalText" id="finalText">
          Gracias por tu amistad, por la buena onda y por tantos momentos simples que se disfrutan un montón. 🌻
        </div>
      </div>
    </div>
  </div>
</div>

<script>
function petals(n){
  const items=["🌻","🌼","✨"];
  for(let i=0;i<n;i++){
    const e=document.createElement("div");
    e.className="confetti";
    e.textContent=items[Math.floor(Math.random()*items.length)];
    e.style.left=Math.random()*100+"vw";
    e.style.fontSize=(15+Math.random()*16)+"px";
    e.style.animationDelay=(Math.random()*.6)+"s";
    e.style.animationDuration=(2.8+Math.random()*1.7)+"s";
    document.body.appendChild(e);
    setTimeout(()=>e.remove(),5000);
  }
}

function openBouquet(){
  document.getElementById("bouquet").classList.add("open");
  document.getElementById("openBtn").classList.add("hide");
  document.getElementById("messageBox").innerHTML="🌻 Ahora toca una flor y descubre su mensaje.";
  petals(14);
}

document.querySelectorAll(".flower").forEach(f=>{
  f.addEventListener("click",()=>{
    const box=document.getElementById("messageBox");
    box.style.opacity="0";
    setTimeout(()=>{
      box.textContent=f.dataset.msg;
      box.style.opacity="1";
    },120);
    petals(5);
  });
});

function showFinal(){
  const t=document.getElementById("finalText");
  t.style.display="block";
  petals(25);
}
</script>
</body>
</html>
"""

components.html(html, height=860, scrolling=False)
