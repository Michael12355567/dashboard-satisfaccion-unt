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
    background:linear-gradient(180deg,#fffdf6 0%,#fff5ba 100%);
}
.block-container{
    max-width:1100px;
    padding-top:.35rem;
    padding-bottom:.35rem;
}
header,footer,#MainMenu{visibility:hidden}
iframe{border-radius:24px}
</style>
""", unsafe_allow_html=True)

html = r"""
<div id="yellow-friend-app">
  <style>
    #yellow-friend-app{
      --ink:#5d4c0a;
      --muted:#7d7040;
      --line:#dfc457;
      --soft:#fff9d7;
      --yellow:#ffd32a;
      --yellow2:#ffe87a;
      --green:#4f9a46;
      font-family:Segoe UI,Arial,sans-serif;
      color:var(--ink);
      width:min(980px,96%);
      margin:0 auto;
      padding:8px 0;
    }
    #yellow-friend-app *{box-sizing:border-box}
    .scene{
      position:relative;
      overflow:hidden;
      border:1px solid var(--line);
      border-radius:30px;
      background:
        radial-gradient(circle at 12% 10%,rgba(255,255,255,.95),transparent 22%),
        radial-gradient(circle at 88% 18%,rgba(255,220,70,.34),transparent 25%),
        linear-gradient(155deg,#fffef8 0%,#fff1a3 100%);
      box-shadow:0 20px 48px rgba(102,72,0,.13);
      padding:18px;
    }
    .intro{
      text-align:center;
      position:relative;
      z-index:4;
      padding:4px 10px 10px;
    }
    .badge{
      display:inline-block;
      padding:6px 11px;
      border-radius:999px;
      border:1px solid #dfbd34;
      background:#fff3aa;
      font-size:12px;
      font-weight:900;
      letter-spacing:.2px;
    }
    .intro h1{
      margin:9px 0 5px;
      font-size:clamp(30px,4.7vw,52px);
      line-height:1;
      color:#675108;
    }
    .intro p{
      margin:0 auto;
      max-width:680px;
      color:var(--muted);
      line-height:1.5;
      font-size:15px;
    }
    .game{
      display:grid;
      grid-template-columns:1.35fr .65fr;
      gap:14px;
      margin-top:8px;
    }
    .field,.side{
      border:1px solid rgba(218,187,67,.72);
      border-radius:24px;
      background:rgba(255,255,255,.62);
      min-width:0;
    }
    .field{
      position:relative;
      height:500px;
      overflow:hidden;
      background:
        linear-gradient(180deg,#eaf8ff 0%,#fff8cb 72%,#cee9aa 73%,#8cc05a 100%);
    }
    .sun{
      position:absolute;
      width:66px;height:66px;
      border-radius:50%;
      right:24px;top:22px;
      background:#ffe15a;
      box-shadow:0 0 35px rgba(255,202,0,.38);
    }
    .cloud{
      position:absolute;
      width:82px;height:25px;
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
    .cloud:before{width:34px;height:34px;left:12px;top:-13px}
    .cloud:after{width:43px;height:43px;left:36px;top:-19px}
    .c1{left:8%;top:54px}
    .c2{right:20%;top:86px;transform:scale(.75)}
    .hint{
      position:absolute;
      left:50%;top:16px;
      transform:translateX(-50%);
      z-index:8;
      background:rgba(255,255,255,.88);
      border:1px solid #e5ce78;
      border-radius:14px;
      padding:8px 12px;
      font-size:13px;
      font-weight:800;
      white-space:nowrap;
    }
    .floating{
      position:absolute;
      border:none;
      background:transparent;
      cursor:pointer;
      font-size:48px;
      line-height:1;
      padding:4px;
      filter:drop-shadow(0 6px 5px rgba(90,65,0,.12));
      animation:drift 3.2s ease-in-out infinite alternate;
      transition:transform .18s ease,opacity .25s ease;
      touch-action:manipulation;
    }
    .floating:hover{transform:scale(1.14) rotate(7deg)}
    .floating.caught{
      animation:pop .34s ease forwards;
      pointer-events:none;
    }
    @keyframes drift{
      from{translate:0 -4px;rotate:-4deg}
      to{translate:0 7px;rotate:5deg}
    }
    @keyframes pop{
      0%{transform:scale(1)}
      50%{transform:scale(1.35) rotate(12deg)}
      100%{transform:scale(.15);opacity:0}
    }
    .fl1{left:9%;top:24%;animation-delay:.2s}
    .fl2{left:35%;top:18%;animation-delay:.8s}
    .fl3{right:12%;top:31%;animation-delay:1.3s}
    .fl4{left:18%;top:53%;animation-delay:1.7s}
    .fl5{left:50%;top:46%;animation-delay:.5s}
    .fl6{right:17%;top:62%;animation-delay:1s}

    .basket{
      position:absolute;
      left:50%;bottom:18px;
      transform:translateX(-50%);
      width:210px;height:122px;
      z-index:3;
    }
    .paper{
      position:absolute;
      left:50%;bottom:0;
      transform:translateX(-50%);
      width:150px;height:98px;
      clip-path:polygon(8% 0,92% 0,72% 100%,28% 100%);
      background:linear-gradient(145deg,#fff8dc,#e7cd75);
      border-radius:12px;
    }
    .stem{
      position:absolute;
      bottom:60px;
      left:50%;
      width:5px;height:68px;
      border-radius:4px;
      background:#4c9443;
      transform-origin:bottom;
      opacity:0;
      transition:.35s ease;
    }
    .stem.show{opacity:1}
    .st1{transform:rotate(-30deg)}
    .st2{transform:rotate(-18deg)}
    .st3{transform:rotate(-6deg)}
    .st4{transform:rotate(7deg)}
    .st5{transform:rotate(19deg)}
    .st6{transform:rotate(31deg)}
    .bouquet-flower{
      position:absolute;
      bottom:112px;
      left:50%;
      font-size:34px;
      opacity:0;
      transform:translateX(-50%) scale(.2);
      transition:.35s cubic-bezier(.2,.9,.2,1);
      z-index:4;
    }
    .bouquet-flower.show{opacity:1;transform:translateX(-50%) scale(1)}
    .bf1{margin-left:-55px;margin-bottom:-2px}
    .bf2{margin-left:-32px;margin-bottom:25px}
    .bf3{margin-left:-8px;margin-bottom:8px}
    .bf4{margin-left:18px;margin-bottom:28px}
    .bf5{margin-left:45px;margin-bottom:5px}
    .bf6{margin-left:4px;margin-bottom:43px}

    .side{
      padding:16px;
      display:flex;
      flex-direction:column;
      gap:11px;
    }
    .progress-label{
      font-size:13px;
      font-weight:900;
      color:#7a650d;
      display:flex;
      justify-content:space-between;
      gap:8px;
    }
    .track{
      height:10px;
      background:#f0e7b7;
      border-radius:999px;
      overflow:hidden;
    }
    .bar{
      width:0%;
      height:100%;
      background:linear-gradient(90deg,#e9b900,#ffe36a);
      border-radius:999px;
      transition:width .35s ease;
    }
    .message{
      min-height:146px;
      border:1px solid #e1c75b;
      border-radius:18px;
      background:#fff9dd;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      padding:14px;
      line-height:1.55;
      font-size:14px;
      color:#665a2c;
    }
    .unlock{
      border:1px dashed #d4b436;
      border-radius:18px;
      background:rgba(255,255,255,.7);
      padding:14px;
      text-align:center;
    }
    .unlock .lock{
      font-size:33px;
      display:block;
      margin-bottom:4px;
    }
    .unlock strong{display:block;margin-bottom:4px}
    .unlock small{color:#827442}
    .final-btn{
      display:none;
      width:100%;
      border:none;
      padding:12px 14px;
      border-radius:14px;
      background:linear-gradient(90deg,#ffc819,#ffe675);
      color:#594500;
      font-weight:900;
      cursor:pointer;
      margin-top:8px;
    }
    .final-card{
      display:none;
      border:1px solid #dfc155;
      border-radius:18px;
      background:linear-gradient(160deg,#fffdf4,#fff1a5);
      padding:14px;
      text-align:center;
      font-size:14px;
      line-height:1.55;
      color:#615426;
    }
    .reset{
      border:none;
      background:transparent;
      color:#9a811d;
      font-size:12px;
      text-decoration:underline;
      cursor:pointer;
      padding:5px;
    }
    .spark{
      position:absolute;
      pointer-events:none;
      z-index:40;
      animation:fall 3s linear forwards;
    }
    @keyframes fall{
      to{transform:translateY(620px) rotate(480deg);opacity:.1}
    }
    @media(max-width:760px){
      .game{grid-template-columns:1fr}
      .field{height:430px}
      .side{padding:13px}
      .message{min-height:88px}
      .floating{font-size:43px}
    }
    @media(prefers-reduced-motion:reduce){
      .floating{animation:none}
      .spark{animation:none}
      *{scroll-behavior:auto!important}
    }
  </style>

  <section class="scene">
    <div class="intro">
      <span class="badge">🌻 DETALLE DE AMISTAD</span>
      <h1>Arma tu ramo amarillo</h1>
      <p>Atrapa las flores que aparecen en el jardín. Cada una guarda un detalle diferente.</p>
    </div>

    <div class="game">
      <div class="field" id="field">
        <div class="sun"></div>
        <div class="cloud c1"></div>
        <div class="cloud c2"></div>
        <div class="hint" id="hint">Toca una flor 🌻</div>

        <button type="button" class="floating fl1" data-i="0" aria-label="Flor amarilla 1">🌻</button>
        <button type="button" class="floating fl2" data-i="1" aria-label="Flor amarilla 2">🌼</button>
        <button type="button" class="floating fl3" data-i="2" aria-label="Flor amarilla 3">🌻</button>
        <button type="button" class="floating fl4" data-i="3" aria-label="Flor amarilla 4">🌼</button>
        <button type="button" class="floating fl5" data-i="4" aria-label="Flor amarilla 5">🌻</button>
        <button type="button" class="floating fl6" data-i="5" aria-label="Flor amarilla 6">🌼</button>

        <div class="basket" aria-label="Ramo que se va formando">
          <div class="stem st1"></div><div class="stem st2"></div><div class="stem st3"></div>
          <div class="stem st4"></div><div class="stem st5"></div><div class="stem st6"></div>
          <div class="bouquet-flower bf1">🌻</div>
          <div class="bouquet-flower bf2">🌼</div>
          <div class="bouquet-flower bf3">🌻</div>
          <div class="bouquet-flower bf4">🌼</div>
          <div class="bouquet-flower bf5">🌻</div>
          <div class="bouquet-flower bf6">🌼</div>
          <div class="paper"></div>
        </div>
      </div>

      <aside class="side">
        <div>
          <div class="progress-label">
            <span>Tu ramo</span>
            <span id="count">0 / 6</span>
          </div>
          <div class="track"><div class="bar" id="bar"></div></div>
        </div>

        <div class="message" id="message" aria-live="polite">
          Empieza atrapando una flor. Cada clic irá armando el ramo 🌻
        </div>

        <div class="unlock">
          <span class="lock" id="lock">🔒</span>
          <strong id="unlockTitle">Detalle final bloqueado</strong>
          <small id="unlockText">Se abre cuando completes el ramo.</small>
          <button type="button" class="final-btn" id="finalBtn">Abrir sorpresa ✨</button>
        </div>

        <div class="final-card" id="finalCard">
          <b>🌻 ¡Ramo completo!</b><br><br>
          Esto es simplemente para agradecer tu amistad, la buena onda, las risas y esos momentos simples que terminan siendo los mejores.<br><br>
          <b>Que nunca falten buenos planes y buenas historias.</b>
        </div>

        <button type="button" class="reset" id="resetBtn">Volver a empezar</button>
      </aside>
    </div>
  </section>

  <script>
  (() => {
    const root = document.getElementById("yellow-friend-app");
    if (!root || root.dataset.ready === "1") return;
    root.dataset.ready = "1";

    const messages = [
      "🌻 Una flor por esas conversaciones que terminan alegrando el día.",
      "😂 Otra por las risas que aparecen sin avisar.",
      "☕ Una más por los ratos simples que se vuelven buenos recuerdos.",
      "🤝 Esta es por la confianza y la buena onda.",
      "✨ Otra por esos mensajes inesperados que llegan justo a tiempo.",
      "🌼 Y esta por todos los buenos momentos que todavía faltan."
    ];

    const flowers = [...root.querySelectorAll(".floating")];
    const stems = [...root.querySelectorAll(".stem")];
    const bouquetFlowers = [...root.querySelectorAll(".bouquet-flower")];
    const bar = root.querySelector("#bar");
    const count = root.querySelector("#count");
    const message = root.querySelector("#message");
    const hint = root.querySelector("#hint");
    const lock = root.querySelector("#lock");
    const unlockTitle = root.querySelector("#unlockTitle");
    const unlockText = root.querySelector("#unlockText");
    const finalBtn = root.querySelector("#finalBtn");
    const finalCard = root.querySelector("#finalCard");
    const resetBtn = root.querySelector("#resetBtn");
    const field = root.querySelector("#field");

    let caught = new Set();

    function sparkle(n=8){
      const icons=["✨","🌻","🌼"];
      const rect=field.getBoundingClientRect();
      for(let i=0;i<n;i++){
        const el=document.createElement("span");
        el.className="spark";
        el.textContent=icons[Math.floor(Math.random()*icons.length)];
        el.style.left=(10+Math.random()*80)+"%";
        el.style.top=(5+Math.random()*25)+"px";
        el.style.fontSize=(14+Math.random()*12)+"px";
        el.style.animationDelay=(Math.random()*.4)+"s";
        field.appendChild(el);
        setTimeout(()=>el.remove(),3600);
      }
    }

    function update(){
      const n=caught.size;
      count.textContent=n+" / 6";
      bar.style.width=(n/6*100)+"%";
      hint.textContent=n===0 ? "Toca una flor 🌻" : n<6 ? "Sigue, faltan "+(6-n)+" ✨" : "¡Ramo completo! 🌻";
      if(n===6){
        lock.textContent="🔓";
        unlockTitle.textContent="Sorpresa desbloqueada";
        unlockText.textContent="Ya puedes abrir el último detalle.";
        finalBtn.style.display="block";
        sparkle(16);
      }
    }

    flowers.forEach(btn=>{
      btn.addEventListener("click",()=>{
        const i=Number(btn.dataset.i);
        if(caught.has(i)) return;
        caught.add(i);
        btn.classList.add("caught");
        stems[i].classList.add("show");
        bouquetFlowers[i].classList.add("show");
        message.textContent=messages[i];
        sparkle(5);
        update();
      });
    });

    finalBtn.addEventListener("click",()=>{
      finalCard.style.display="block";
      finalBtn.style.display="none";
      sparkle(24);
    });

    resetBtn.addEventListener("click",()=>{
      caught.clear();
      flowers.forEach(f=>f.classList.remove("caught"));
      stems.forEach(s=>s.classList.remove("show"));
      bouquetFlowers.forEach(f=>f.classList.remove("show"));
      finalCard.style.display="none";
      finalBtn.style.display="none";
      lock.textContent="🔒";
      unlockTitle.textContent="Detalle final bloqueado";
      unlockText.textContent="Se abre cuando completes el ramo.";
      message.textContent="Empieza atrapando una flor. Cada clic irá armando el ramo 🌻";
      update();
    });

    update();
  })();
  </script>
</div>
"""

components.html(html, height=790, scrolling=False)
