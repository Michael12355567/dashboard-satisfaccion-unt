import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="21 de Septiembre 🌻",
    page_icon="🌻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp{
    background:linear-gradient(180deg,#fffdf6 0%,#fff4b7 100%);
}
.block-container{
    max-width:1120px;
    padding-top:.3rem;
    padding-bottom:.3rem;
}
header,footer,#MainMenu{visibility:hidden}
iframe{border-radius:26px}
</style>
""", unsafe_allow_html=True)

html = r"""
<div id="flores21">
<style>
#flores21{
  --ink:#5e4b09;
  --muted:#786b37;
  --line:#dec153;
  --yellow:#ffd225;
  --yellow2:#ffe878;
  --green:#4d9944;
  width:min(1020px,96%);
  margin:0 auto;
  padding:6px 0;
  font-family:Segoe UI,Arial,sans-serif;
  color:var(--ink);
}
#flores21 *{box-sizing:border-box}
.main{
  position:relative;
  overflow:hidden;
  border:1px solid var(--line);
  border-radius:30px;
  padding:17px;
  background:
    radial-gradient(circle at 12% 9%,rgba(255,255,255,.96),transparent 22%),
    radial-gradient(circle at 87% 12%,rgba(255,218,57,.3),transparent 25%),
    linear-gradient(155deg,#fffef8,#fff0a0);
  box-shadow:0 20px 46px rgba(105,73,0,.13);
}
.head{
  text-align:center;
  padding:3px 10px 12px;
}
.date{
  display:inline-block;
  border:1px solid #ddb936;
  background:#fff0a0;
  border-radius:999px;
  padding:6px 12px;
  font-size:12px;
  font-weight:900;
  letter-spacing:.25px;
}
.head h1{
  margin:9px 0 5px;
  font-size:clamp(31px,4.6vw,52px);
  line-height:1;
  color:#675008;
}
.head p{
  max-width:700px;
  margin:0 auto;
  color:var(--muted);
  font-size:15px;
  line-height:1.5;
}
.layout{
  display:grid;
  grid-template-columns:1.55fr .65fr;
  gap:13px;
}
.field{
  position:relative;
  height:540px;
  overflow:hidden;
  border:1px solid #dec66a;
  border-radius:24px;
  background:linear-gradient(180deg,#eaf8ff 0%,#fff8c9 71%,#cee9aa 72%,#8cbe59 100%);
}
.sun{
  position:absolute;
  right:25px;top:22px;
  width:68px;height:68px;
  border-radius:50%;
  background:#ffe259;
  box-shadow:0 0 35px rgba(255,204,0,.4);
}
.cloud{
  position:absolute;
  width:84px;height:25px;
  border-radius:30px;
  background:white;
  opacity:.92;
}
.cloud:before,.cloud:after{
  content:"";
  position:absolute;
  border-radius:50%;
  background:white;
}
.cloud:before{width:35px;height:35px;left:12px;top:-14px}
.cloud:after{width:44px;height:44px;left:37px;top:-20px}
.c1{left:8%;top:52px}
.c2{right:20%;top:88px;transform:scale(.76)}
.tip{
  position:absolute;
  left:50%;top:15px;
  transform:translateX(-50%);
  z-index:20;
  padding:7px 11px;
  border-radius:13px;
  border:1px solid #e4cf7a;
  background:rgba(255,255,255,.9);
  font-size:12px;
  font-weight:900;
  white-space:nowrap;
}
.pick{
  position:absolute;
  border:none;
  background:transparent;
  font-size:49px;
  line-height:1;
  cursor:pointer;
  padding:5px;
  filter:drop-shadow(0 6px 5px rgba(80,55,0,.12));
  animation:float 2.8s ease-in-out infinite alternate;
  transition:transform .15s ease,opacity .2s ease;
  z-index:10;
}
.pick:hover{transform:scale(1.13) rotate(7deg)}
.pick.used{opacity:0;pointer-events:none}
@keyframes float{
  from{translate:0 -5px;rotate:-4deg}
  to{translate:0 7px;rotate:5deg}
}
.p1{left:8%;top:23%;animation-delay:.1s}
.p2{left:36%;top:18%;animation-delay:.8s}
.p3{right:9%;top:28%;animation-delay:1.3s}
.p4{left:15%;top:51%;animation-delay:1.6s}
.p5{right:15%;top:51%;animation-delay:.45s}
.p6{left:45%;top:38%;animation-delay:1s}

.bouquet-zone{
  position:absolute;
  left:50%;bottom:6px;
  transform:translateX(-50%);
  width:410px;height:310px;
  z-index:4;
}
.aura{
  position:absolute;
  left:50%;top:45%;
  transform:translate(-50%,-50%);
  width:300px;height:230px;
  border-radius:50%;
  background:radial-gradient(circle,rgba(255,226,81,.35),transparent 70%);
}
.paper{
  position:absolute;
  left:50%;bottom:0;
  transform:translateX(-50%);
  width:230px;height:160px;
  clip-path:polygon(7% 0,93% 0,72% 100%,28% 100%);
  background:linear-gradient(145deg,#fff9e1,#e5c96e);
  filter:drop-shadow(0 15px 14px rgba(93,63,0,.13));
  z-index:3;
}
.ribbon{
  position:absolute;
  left:50%;bottom:70px;
  transform:translateX(-50%);
  width:105px;height:18px;
  border-radius:20px;
  background:#c69e18;
  z-index:6;
}
.stem{
  position:absolute;
  left:50%;bottom:85px;
  width:6px;height:145px;
  background:linear-gradient(#62aa4c,#377f38);
  border-radius:5px;
  transform-origin:bottom;
  opacity:0;
  transition:.35s ease;
}
.stem.on{opacity:1}
.st1{transform:rotate(-28deg)}
.st2{transform:rotate(-18deg)}
.st3{transform:rotate(-7deg)}
.st4{transform:rotate(8deg)}
.st5{transform:rotate(19deg)}
.st6{transform:rotate(30deg)}

.bf{
  position:absolute;
  left:50%;
  font-size:56px;
  opacity:0;
  transform:translateX(-50%) scale(.15);
  transition:.42s cubic-bezier(.15,.9,.2,1);
  z-index:7;
  filter:drop-shadow(0 7px 5px rgba(80,55,0,.11));
}
.bf.on{opacity:1;transform:translateX(-50%) scale(1)}
.b1{bottom:178px;margin-left:-90px}
.b2{bottom:215px;margin-left:-55px}
.b3{bottom:188px;margin-left:-18px}
.b4{bottom:220px;margin-left:35px}
.b5{bottom:178px;margin-left:82px}
.b6{bottom:245px;margin-left:-5px}

.fly{
  position:absolute;
  z-index:50;
  font-size:50px;
  pointer-events:none;
  transition:left .58s cubic-bezier(.2,.8,.2,1), top .58s cubic-bezier(.2,.8,.2,1), transform .58s ease, opacity .58s ease;
  filter:drop-shadow(0 7px 6px rgba(70,50,0,.15));
}
.panel{
  border:1px solid #dec45d;
  border-radius:24px;
  background:rgba(255,255,255,.68);
  padding:14px;
  display:flex;
  flex-direction:column;
  gap:10px;
  min-width:0;
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
  background:#eee2a9;
  overflow:hidden;
}
.bar{
  width:0%;
  height:100%;
  border-radius:999px;
  background:linear-gradient(90deg,#d9aa00,#ffe16b);
  transition:.3s ease;
}
.msg{
  min-height:180px;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:14px;
  border:1px solid #e0c65a;
  border-radius:17px;
  background:#fff9db;
  text-align:center;
  font-size:14px;
  line-height:1.55;
  color:#655927;
}
.surprise{
  text-align:center;
  padding:13px;
  border:1px dashed #d3b437;
  border-radius:17px;
  background:rgba(255,255,255,.7);
}
.lock{font-size:31px;display:block}
.surprise strong{display:block;margin:4px 0}
.surprise small{color:#827642}
.finalBtn{
  display:none;
  width:100%;
  margin-top:9px;
  padding:11px 12px;
  border:none;
  border-radius:13px;
  background:linear-gradient(90deg,#ffc817,#ffe775);
  color:#584400;
  font-weight:900;
  cursor:pointer;
}
.finalMsg{
  display:none;
  padding:13px;
  border:1px solid #dfc155;
  border-radius:17px;
  background:linear-gradient(160deg,#fffdf3,#fff0a4);
  text-align:center;
  font-size:14px;
  line-height:1.55;
}
.reset{
  border:none;
  background:transparent;
  color:#927818;
  text-decoration:underline;
  cursor:pointer;
  font-size:12px;
  padding:4px;
}
.spark{
  position:absolute;
  top:-25px;
  z-index:80;
  pointer-events:none;
  animation:fall 3s linear forwards;
}
@keyframes fall{
  to{transform:translateY(620px) rotate(500deg);opacity:.1}
}
@media(max-width:780px){
  .layout{grid-template-columns:1fr}
  .field{height:520px}
  .panel{padding:12px}
  .msg{min-height:90px}
  .bouquet-zone{transform:translateX(-50%) scale(.84);transform-origin:bottom center}
  .pick{font-size:44px}
}
@media(prefers-reduced-motion:reduce){
  .pick{animation:none}
  .spark{animation:none}
}
</style>

<section class="main">
  <header class="head">
    <span class="date">🌻 21 DE SEPTIEMBRE</span>
    <h1>Hoy toca flores amarillas</h1>
    <p>
      Y como este detalle también se puede compartir con una buena amistad,
      aquí tienes un ramo que tendrás que descubrir flor por flor.
    </p>
  </header>

  <div class="layout">
    <div class="field" id="field">
      <div class="sun"></div>
      <div class="cloud c1"></div>
      <div class="cloud c2"></div>
      <div class="tip" id="tip">Toca una flor para empezar 🌻</div>

      <button type="button" class="pick p1" data-i="0" aria-label="Flor amarilla 1">🌻</button>
      <button type="button" class="pick p2" data-i="1" aria-label="Flor amarilla 2">🌼</button>
      <button type="button" class="pick p3" data-i="2" aria-label="Flor amarilla 3">🌻</button>
      <button type="button" class="pick p4" data-i="3" aria-label="Flor amarilla 4">🌼</button>
      <button type="button" class="pick p5" data-i="4" aria-label="Flor amarilla 5">🌻</button>
      <button type="button" class="pick p6" data-i="5" aria-label="Flor amarilla 6">🌼</button>

      <div class="bouquet-zone" id="bouquetZone">
        <div class="aura"></div>
        <div class="stem st1"></div><div class="stem st2"></div><div class="stem st3"></div>
        <div class="stem st4"></div><div class="stem st5"></div><div class="stem st6"></div>

        <div class="bf b1">🌻</div>
        <div class="bf b2">🌼</div>
        <div class="bf b3">🌻</div>
        <div class="bf b4">🌼</div>
        <div class="bf b5">🌻</div>
        <div class="bf b6">🌼</div>

        <div class="paper"></div>
        <div class="ribbon"></div>
      </div>
    </div>

    <aside class="panel">
      <div>
        <div class="progress-row">
          <span>Tu ramo amarillo</span>
          <span id="counter">0 / 6</span>
        </div>
        <div class="track"><div class="bar" id="bar"></div></div>
      </div>

      <div class="msg" id="msg" aria-live="polite">
        Cada flor tiene un mensaje distinto. Haz clic en la primera que quieras ✨
      </div>

      <div class="surprise">
        <span class="lock" id="lock">🔒</span>
        <strong id="surpriseTitle">Detalle final</strong>
        <small id="surpriseText">Se desbloquea al completar el ramo.</small>
        <button type="button" class="finalBtn" id="finalBtn">Abrir sorpresa 🌻</button>
      </div>

      <div class="finalMsg" id="finalMsg">
        <b>🌻 Feliz día de las flores amarillas.</b><br><br>
        Te dejo este ramo porque una buena amistad también merece detalles,
        risas y buenos deseos.<br><br>
        Que hoy te sobren motivos para sonreír y que sigan llegando buenos momentos. ✨
      </div>

      <button type="button" class="reset" id="reset">Volver a empezar</button>
    </aside>
  </div>
</section>

<script>
(() => {
  const root = document.getElementById("flores21");
  if (!root || root.dataset.ready === "1") return;
  root.dataset.ready = "1";

  const field = root.querySelector("#field");
  const picks = [...root.querySelectorAll(".pick")];
  const stems = [...root.querySelectorAll(".stem")];
  const built = [...root.querySelectorAll(".bf")];
  const msg = root.querySelector("#msg");
  const counter = root.querySelector("#counter");
  const bar = root.querySelector("#bar");
  const tip = root.querySelector("#tip");
  const lock = root.querySelector("#lock");
  const surpriseText = root.querySelector("#surpriseText");
  const finalBtn = root.querySelector("#finalBtn");
  const finalMsg = root.querySelector("#finalMsg");
  const reset = root.querySelector("#reset");
  const bouquetZone = root.querySelector("#bouquetZone");

  const messages = [
    "🌻 Para que hoy no te falte un poquito de amarillo y buena energía.",
    "🌼 Por esas conversaciones que siempre terminan mejorando el día.",
    "😂 Por las risas espontáneas que hacen más buenos los momentos simples.",
    "🤝 Por la confianza y la buena onda que hacen valiosa una amistad.",
    "✨ Por todos esos planes improvisados que terminan siendo buenas historias.",
    "🌻 Y esta última por todos los buenos momentos que todavía faltan por llegar."
  ];

  let caught = new Set();

  function petals(n=8){
    const icons=["🌻","🌼","✨"];
    for(let i=0;i<n;i++){
      const e=document.createElement("span");
      e.className="spark";
      e.textContent=icons[Math.floor(Math.random()*icons.length)];
      e.style.left=(8+Math.random()*84)+"%";
      e.style.fontSize=(14+Math.random()*13)+"px";
      e.style.animationDelay=(Math.random()*.45)+"s";
      field.appendChild(e);
      setTimeout(()=>e.remove(),3500);
    }
  }

  function flyToBouquet(btn,index){
    const fieldRect=field.getBoundingClientRect();
    const btnRect=btn.getBoundingClientRect();
    const targetRect=bouquetZone.getBoundingClientRect();

    const clone=document.createElement("span");
    clone.className="fly";
    clone.textContent=btn.textContent;
    clone.style.left=(btnRect.left-fieldRect.left)+"px";
    clone.style.top=(btnRect.top-fieldRect.top)+"px";
    field.appendChild(clone);

    requestAnimationFrame(()=>{
      requestAnimationFrame(()=>{
        const tx=(targetRect.left-fieldRect.left)+(targetRect.width/2)-25 + ((index-2.5)*9);
        const ty=(targetRect.top-fieldRect.top)+58+(index%2)*18;
        clone.style.left=tx+"px";
        clone.style.top=ty+"px";
        clone.style.transform="scale(.75) rotate(280deg)";
        clone.style.opacity=".3";
      });
    });

    setTimeout(()=>{
      clone.remove();
      stems[index].classList.add("on");
      built[index].classList.add("on");
    },610);
  }

  function update(){
    const n=caught.size;
    counter.textContent=n+" / 6";
    bar.style.width=(n/6*100)+"%";
    tip.textContent=n===0 ? "Toca una flor para empezar 🌻" :
                    n<6 ? "Sigue armando tu ramo · faltan "+(6-n) :
                    "¡Ramo completo! 🌻";

    if(n===6){
      lock.textContent="🔓";
      surpriseText.textContent="Tu sorpresa ya está lista.";
      finalBtn.style.display="block";
      petals(18);
    }
  }

  picks.forEach(btn=>{
    btn.addEventListener("click",()=>{
      const i=Number(btn.dataset.i);
      if(caught.has(i)) return;
      caught.add(i);
      flyToBouquet(btn,i);
      btn.classList.add("used");
      msg.textContent=messages[i];
      petals(5);
      update();
    });
  });

  finalBtn.addEventListener("click",()=>{
    finalMsg.style.display="block";
    finalBtn.style.display="none";
    petals(28);
  });

  reset.addEventListener("click",()=>{
    caught.clear();
    picks.forEach(p=>p.classList.remove("used"));
    stems.forEach(s=>s.classList.remove("on"));
    built.forEach(b=>b.classList.remove("on"));
    finalBtn.style.display="none";
    finalMsg.style.display="none";
    lock.textContent="🔒";
    surpriseText.textContent="Se desbloquea al completar el ramo.";
    msg.textContent="Cada flor tiene un mensaje distinto. Haz clic en la primera que quieras ✨";
    update();
  });

  update();
})();
</script>
</div>
"""

components.html(html, height=830, scrolling=False)
