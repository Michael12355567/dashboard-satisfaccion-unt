import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flores Amarillas 🌻",
    page_icon="🌻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp{
    background:linear-gradient(180deg,#fffdf7 0%,#fff2aa 100%);
}
.block-container{
    max-width:1100px;
    padding-top:.25rem;
    padding-bottom:.25rem;
}
header,footer,#MainMenu{visibility:hidden}
iframe{border-radius:26px}
</style>
""", unsafe_allow_html=True)

html = r"""
<div id="ramo-app">
<style>
#ramo-app{
  --ink:#5d4a08;
  --muted:#776936;
  --line:#dec153;
  width:min(1020px,97%);
  margin:0 auto;
  padding:5px 0;
  font-family:Segoe UI,Arial,sans-serif;
  color:var(--ink);
}
#ramo-app *{box-sizing:border-box}
.wrap{
  position:relative;
  overflow:hidden;
  border:1px solid var(--line);
  border-radius:30px;
  background:
    radial-gradient(circle at 12% 10%,rgba(255,255,255,.95),transparent 23%),
    radial-gradient(circle at 88% 15%,rgba(255,218,58,.30),transparent 25%),
    linear-gradient(155deg,#fffef8,#fff0a1);
  box-shadow:0 20px 48px rgba(100,70,0,.13);
  padding:14px;
}
.top{
  text-align:center;
  padding:3px 10px 8px;
}
.date{
  display:inline-block;
  border:1px solid #ddb938;
  background:#fff0a0;
  border-radius:999px;
  padding:6px 12px;
  font-size:12px;
  font-weight:900;
}
.top h1{
  margin:8px 0 4px;
  font-size:clamp(30px,4.5vw,50px);
  line-height:1;
  color:#675008;
}
.top p{
  margin:0 auto;
  max-width:720px;
  color:var(--muted);
  font-size:14px;
  line-height:1.45;
}
.content{
  display:grid;
  grid-template-columns:1.5fr .6fr;
  gap:12px;
  margin-top:6px;
}
.visual{
  position:relative;
  height:610px;
  border:1px solid #dec66a;
  border-radius:24px;
  overflow:hidden;
  background:
    linear-gradient(180deg,#edf9ff 0%,#fff8c8 70%,#d2eaaa 71%,#8ebe5a 100%);
}
.sun{
  position:absolute;
  right:28px;top:24px;
  width:68px;height:68px;
  border-radius:50%;
  background:#ffe15b;
  box-shadow:0 0 36px rgba(255,202,0,.4);
}
.cloud{
  position:absolute;
  width:86px;height:26px;
  border-radius:30px;
  background:#fff;
  opacity:.92;
}
.cloud:before,.cloud:after{
  content:"";
  position:absolute;
  background:#fff;
  border-radius:50%;
}
.cloud:before{width:36px;height:36px;left:12px;top:-14px}
.cloud:after{width:45px;height:45px;left:38px;top:-20px}
.c1{left:8%;top:56px}
.c2{right:20%;top:95px;transform:scale(.76)}
.tip{
  position:absolute;
  left:50%;top:15px;
  transform:translateX(-50%);
  z-index:30;
  background:rgba(255,255,255,.9);
  border:1px solid #e4ce78;
  border-radius:14px;
  padding:7px 11px;
  font-size:12px;
  font-weight:900;
  white-space:nowrap;
}
.bouquet{
  position:absolute;
  left:50%;bottom:8px;
  transform:translateX(-50%);
  width:590px;height:515px;
}
.glow{
  position:absolute;
  left:50%;top:45%;
  transform:translate(-50%,-50%);
  width:470px;height:390px;
  border-radius:50%;
  background:radial-gradient(circle,rgba(255,226,82,.34),transparent 69%);
}
.paper{
  position:absolute;
  left:50%;bottom:0;
  transform:translateX(-50%);
  width:300px;height:210px;
  clip-path:polygon(6% 0,94% 0,72% 100%,28% 100%);
  background:linear-gradient(145deg,#fff8dc,#e5c66a);
  filter:drop-shadow(0 17px 16px rgba(90,62,0,.14));
  z-index:2;
}
.ribbon{
  position:absolute;
  left:50%;bottom:90px;
  transform:translateX(-50%);
  width:125px;height:20px;
  border-radius:20px;
  background:#c79d18;
  z-index:8;
}
.stem{
  position:absolute;
  left:50%;bottom:110px;
  width:7px;height:230px;
  border-radius:6px;
  background:linear-gradient(#63ad4c,#367b36);
  transform-origin:bottom;
  z-index:1;
}
.s1{transform:rotate(-33deg)}
.s2{transform:rotate(-24deg)}
.s3{transform:rotate(-15deg)}
.s4{transform:rotate(-7deg)}
.s5{transform:rotate(1deg)}
.s6{transform:rotate(10deg)}
.s7{transform:rotate(20deg)}
.s8{transform:rotate(30deg)}

.flower{
  position:absolute;
  width:118px;height:118px;
  border:none;
  background:transparent;
  cursor:pointer;
  z-index:10;
  padding:0;
  filter:drop-shadow(0 8px 7px rgba(76,52,0,.14));
  transition:transform .2s ease,filter .2s ease;
}
.flower:hover{transform:scale(1.07)}
.flower.marked{
  filter:drop-shadow(0 0 16px rgba(255,193,0,.8));
}
.flower.marked:after{
  content:"✓";
  position:absolute;
  right:-2px;top:-2px;
  width:29px;height:29px;
  display:grid;
  place-items:center;
  border-radius:50%;
  background:#fff8cc;
  border:2px solid #d8ac12;
  color:#7d6300;
  font-weight:1000;
  font-size:17px;
  z-index:20;
}
.flower.pop{animation:pop .35s ease}
@keyframes pop{
  0%{transform:scale(1)}
  50%{transform:scale(1.18) rotate(5deg)}
  100%{transform:scale(1)}
}
.pet{
  position:absolute;
  left:41px;top:17px;
  width:36px;height:53px;
  border-radius:58% 58% 48% 48%;
  background:linear-gradient(#ffeb77,#ffc817);
  transform-origin:18px 39px;
  box-shadow:0 2px 5px rgba(0,0,0,.04);
}
.p1{transform:rotate(0deg) translateY(-15px)}
.p2{transform:rotate(45deg) translateY(-15px)}
.p3{transform:rotate(90deg) translateY(-15px)}
.p4{transform:rotate(135deg) translateY(-15px)}
.p5{transform:rotate(180deg) translateY(-15px)}
.p6{transform:rotate(225deg) translateY(-15px)}
.p7{transform:rotate(270deg) translateY(-15px)}
.p8{transform:rotate(315deg) translateY(-15px)}
.center{
  position:absolute;
  left:40px;top:40px;
  width:38px;height:38px;
  border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#a36d18,#69400c 72%);
  z-index:5;
}
.f1{left:36px;top:220px}
.f2{left:95px;top:110px}
.f3{left:185px;top:38px}
.f4{left:255px;top:154px}
.f5{left:330px;top:54px}
.f6{left:414px;top:135px}
.f7{left:438px;top:245px}
.f8{left:160px;top:230px}

.panel{
  border:1px solid #dec45d;
  border-radius:24px;
  padding:14px;
  background:rgba(255,255,255,.69);
  display:flex;
  flex-direction:column;
  gap:10px;
}
.progress-row{
  display:flex;
  justify-content:space-between;
  font-size:12px;
  font-weight:900;
}
.track{
  height:9px;
  border-radius:999px;
  background:#eee1a7;
  overflow:hidden;
}
.bar{
  width:0%;
  height:100%;
  background:linear-gradient(90deg,#d9aa00,#ffe36f);
  transition:.3s ease;
}
.message{
  min-height:230px;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  padding:15px;
  border:1px solid #dfc55b;
  border-radius:17px;
  background:#fff9db;
  color:#645827;
  font-size:14px;
  line-height:1.58;
}
.finalBox{
  padding:13px;
  text-align:center;
  border:1px dashed #d2b337;
  border-radius:17px;
  background:rgba(255,255,255,.72);
}
.finalBox .lock{
  display:block;
  font-size:31px;
}
.finalBtn{
  display:none;
  width:100%;
  border:none;
  margin-top:8px;
  padding:11px;
  border-radius:13px;
  cursor:pointer;
  background:linear-gradient(90deg,#ffc817,#ffe777);
  color:#584400;
  font-weight:900;
}
.finalMsg{
  display:none;
  margin-top:9px;
  padding:12px;
  border-radius:14px;
  background:linear-gradient(160deg,#fffdf3,#fff0a5);
  border:1px solid #dfc055;
  font-size:13px;
  line-height:1.5;
}
.reset{
  border:none;
  background:transparent;
  text-decoration:underline;
  color:#927718;
  font-size:12px;
  cursor:pointer;
}
.spark{
  position:absolute;
  top:-25px;
  pointer-events:none;
  z-index:100;
  animation:fall 3s linear forwards;
}
@keyframes fall{
  to{transform:translateY(650px) rotate(500deg);opacity:.1}
}

@media(max-width:780px){
  .content{grid-template-columns:1fr}
  .visual{height:570px}
  .bouquet{
    transform:translateX(-50%) scale(.84);
    transform-origin:bottom center;
  }
  .message{min-height:95px}
}
@media(prefers-reduced-motion:reduce){
  .spark{animation:none}
}
</style>

<section class="wrap">
  <header class="top">
    <span class="date">🌻 21 DE SEPTIEMBRE</span>
    <h1>Flores amarillas para ti</h1>
    <p>
      Hoy toca flores amarillas. Haz clic directamente en cada flor del ramo;
      cada una guarda un mensaje distinto.
    </p>
  </header>

  <div class="content">
    <div class="visual" id="visual">
      <div class="sun"></div>
      <div class="cloud c1"></div>
      <div class="cloud c2"></div>
      <div class="tip" id="tip">Toca cualquier flor del ramo 🌻</div>

      <div class="bouquet">
        <div class="glow"></div>

        <div class="stem s1"></div><div class="stem s2"></div><div class="stem s3"></div><div class="stem s4"></div>
        <div class="stem s5"></div><div class="stem s6"></div><div class="stem s7"></div><div class="stem s8"></div>

        <button type="button" class="flower f1" data-i="0" aria-label="Flor 1">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </button>
        <button type="button" class="flower f2" data-i="1" aria-label="Flor 2">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </button>
        <button type="button" class="flower f3" data-i="2" aria-label="Flor 3">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </button>
        <button type="button" class="flower f4" data-i="3" aria-label="Flor 4">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </button>
        <button type="button" class="flower f5" data-i="4" aria-label="Flor 5">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </button>
        <button type="button" class="flower f6" data-i="5" aria-label="Flor 6">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </button>
        <button type="button" class="flower f7" data-i="6" aria-label="Flor 7">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </button>
        <button type="button" class="flower f8" data-i="7" aria-label="Flor 8">
          <span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span>
          <span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span>
        </button>

        <div class="paper"></div>
        <div class="ribbon"></div>
      </div>
    </div>

    <aside class="panel">
      <div>
        <div class="progress-row">
          <span>Flores descubiertas</span>
          <span id="counter">0 / 8</span>
        </div>
        <div class="track"><div class="bar" id="bar"></div></div>
      </div>

      <div class="message" id="message" aria-live="polite">
        🌻 Elige cualquier flor. Al tocarla quedará marcada y aparecerá su mensaje.
      </div>

      <div class="finalBox">
        <span class="lock" id="lock">🔒</span>
        <strong id="finalTitle">Mensaje final</strong><br>
        <small id="finalHint">Se desbloquea al descubrir las 8 flores.</small>
        <button type="button" class="finalBtn" id="finalBtn">Abrir mensaje final ✨</button>

        <div class="finalMsg" id="finalMsg">
          <b>🌻 Feliz día de las flores amarillas.</b><br><br>
          Te dejo este ramo como un detalle de buena amistad:
          por las risas, las conversaciones, la confianza y todos esos momentos
          simples que terminan siendo buenos recuerdos.<br><br>
          <b>Que hoy te sobren motivos para sonreír. ✨</b>
        </div>
      </div>

      <button type="button" class="reset" id="reset">Volver a descubrir las flores</button>
    </aside>
  </div>
</section>

<script>
(() => {
  const root=document.getElementById("ramo-app");
  if(!root || root.dataset.ready==="1") return;
  root.dataset.ready="1";

  const flowers=[...root.querySelectorAll(".flower")];
  const message=root.querySelector("#message");
  const counter=root.querySelector("#counter");
  const bar=root.querySelector("#bar");
  const tip=root.querySelector("#tip");
  const lock=root.querySelector("#lock");
  const finalHint=root.querySelector("#finalHint");
  const finalBtn=root.querySelector("#finalBtn");
  const finalMsg=root.querySelector("#finalMsg");
  const reset=root.querySelector("#reset");
  const visual=root.querySelector("#visual");

  const messages=[
    "🌻 Una flor para empezar el día con buena energía.",
    "✨ Una por esas conversaciones que siempre terminan alegrando el momento.",
    "😂 Otra por las risas que salen de la nada y se quedan como recuerdo.",
    "🤝 Esta es por la confianza y la buena onda de una amistad sincera.",
    "☀️ Una más para que hoy te sobren motivos para sonreír.",
    "🌼 Esta va por todos los planes simples que terminan siendo los mejores.",
    "💛 Otra por estar presente de una forma sencilla, pero valiosa.",
    "🌻 Y la última, por todos los buenos momentos que todavía faltan por llegar."
  ];

  const selected=new Set();

  function sparkle(n=8){
    const icons=["✨","🌻","🌼"];
    for(let i=0;i<n;i++){
      const e=document.createElement("span");
      e.className="spark";
      e.textContent=icons[Math.floor(Math.random()*icons.length)];
      e.style.left=(8+Math.random()*84)+"%";
      e.style.fontSize=(14+Math.random()*14)+"px";
      e.style.animationDelay=(Math.random()*.45)+"s";
      visual.appendChild(e);
      setTimeout(()=>e.remove(),3500);
    }
  }

  function update(){
    const n=selected.size;
    counter.textContent=n+" / 8";
    bar.style.width=(n/8*100)+"%";
    tip.textContent=n===0 ? "Toca cualquier flor del ramo 🌻" :
                    n<8 ? "Muy bien · faltan "+(8-n)+" flores" :
                    "¡Descubriste todo el ramo! 🌻";

    if(n===8){
      lock.textContent="🔓";
      finalHint.textContent="Ya puedes abrirlo.";
      finalBtn.style.display="block";
      sparkle(18);
    }
  }

  flowers.forEach(btn=>{
    btn.addEventListener("click",()=>{
      const i=Number(btn.dataset.i);
      if(!selected.has(i)){
        selected.add(i);
        btn.classList.add("marked");
      }
      btn.classList.remove("pop");
      void btn.offsetWidth;
      btn.classList.add("pop");
      message.textContent=messages[i];
      sparkle(5);
      update();
    });
  });

  finalBtn.addEventListener("click",()=>{
    finalMsg.style.display="block";
    finalBtn.style.display="none";
    sparkle(28);
  });

  reset.addEventListener("click",()=>{
    selected.clear();
    flowers.forEach(f=>f.classList.remove("marked","pop"));
    message.textContent="🌻 Elige cualquier flor. Al tocarla quedará marcada y aparecerá su mensaje.";
    lock.textContent="🔒";
    finalHint.textContent="Se desbloquea al descubrir las 8 flores.";
    finalBtn.style.display="none";
    finalMsg.style.display="none";
    update();
  });

  update();
})();
</script>
</div>
"""

components.html(html, height=870, scrolling=False)
