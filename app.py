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
    background:linear-gradient(180deg,#fffdf7 0%,#fff3ad 100%);
}
.block-container{
    max-width:1120px;
    padding-top:.25rem;
    padding-bottom:.25rem;
}
header,footer,#MainMenu{visibility:hidden}
iframe{border-radius:26px}
</style>
""", unsafe_allow_html=True)

html = r"""
<div id="flowers-quiz-personal">
<style>
#flowers-quiz-personal{
  --ink:#5d4a08;
  --muted:#766936;
  --line:#dec052;
  width:min(1020px,97%);
  margin:0 auto;
  padding:5px 0;
  font-family:Segoe UI,Arial,sans-serif;
  color:var(--ink);
}
#flowers-quiz-personal *{box-sizing:border-box}

.wrap{
  overflow:hidden;
  border:1px solid var(--line);
  border-radius:30px;
  background:
    radial-gradient(circle at 12% 8%,rgba(255,255,255,.96),transparent 22%),
    radial-gradient(circle at 88% 15%,rgba(255,218,60,.28),transparent 25%),
    linear-gradient(155deg,#fffef9,#fff0a2);
  box-shadow:0 20px 48px rgba(99,69,0,.13);
  padding:14px;
}
.top{text-align:center;padding:3px 10px 10px}
.date{
  display:inline-block;padding:6px 12px;border:1px solid #deb93a;
  border-radius:999px;background:#fff0a0;font-size:12px;font-weight:900
}
.top h1{margin:8px 0 4px;font-size:clamp(31px,4.5vw,51px);line-height:1;color:#665008}
.top p{margin:0 auto;max-width:720px;font-size:14px;line-height:1.48;color:var(--muted)}

.hero{display:grid;grid-template-columns:1.35fr .65fr;gap:12px}
.visual{
  position:relative;height:480px;overflow:hidden;border:1px solid #dec66a;border-radius:24px;
  background:linear-gradient(180deg,#eaf8ff 0%,#fff7c5 70%,#d1e9aa 71%,#8ebe5c 100%)
}
.sun{
  position:absolute;right:27px;top:23px;width:65px;height:65px;border-radius:50%;
  background:#ffe15a;box-shadow:0 0 34px rgba(255,202,0,.38)
}
.cloud{position:absolute;width:82px;height:25px;border-radius:30px;background:#fff;opacity:.92}
.cloud:before,.cloud:after{content:"";position:absolute;border-radius:50%;background:#fff}
.cloud:before{width:34px;height:34px;left:12px;top:-13px}
.cloud:after{width:43px;height:43px;left:36px;top:-19px}
.c1{left:8%;top:54px}.c2{right:20%;top:86px;transform:scale(.76)}

.bouquet{position:absolute;left:50%;bottom:6px;transform:translateX(-50%);width:560px;height:420px}
.glow{
  position:absolute;left:50%;top:46%;transform:translate(-50%,-50%);
  width:450px;height:340px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,227,84,.34),transparent 70%)
}
.paper{
  position:absolute;left:50%;bottom:0;transform:translateX(-50%);
  width:280px;height:185px;clip-path:polygon(7% 0,93% 0,72% 100%,28% 100%);
  background:linear-gradient(145deg,#fff9e1,#e5c768);filter:drop-shadow(0 16px 14px rgba(90,62,0,.13));z-index:2
}
.ribbon{
  position:absolute;left:50%;bottom:80px;transform:translateX(-50%);
  width:118px;height:19px;border-radius:20px;background:#c79d18;z-index:8
}
.stem{
  position:absolute;left:50%;bottom:96px;width:7px;height:195px;border-radius:6px;
  background:linear-gradient(#63ad4c,#367b36);transform-origin:bottom
}
.s1{transform:rotate(-34deg)} .s2{transform:rotate(-25deg)}
.s3{transform:rotate(-15deg)} .s4{transform:rotate(-7deg)}
.s5{transform:rotate(2deg)} .s6{transform:rotate(11deg)}
.s7{transform:rotate(21deg)} .s8{transform:rotate(31deg)}

.flower{
  position:absolute;width:112px;height:112px;filter:drop-shadow(0 8px 7px rgba(76,52,0,.13));
  animation:sway 3s ease-in-out infinite alternate
}
@keyframes sway{from{rotate:-3deg}to{rotate:3deg}}
.pet{
  position:absolute;left:39px;top:16px;width:34px;height:50px;
  border-radius:58% 58% 48% 48%;background:linear-gradient(#ffec7a,#ffc817);
  transform-origin:17px 37px
}
.p1{transform:rotate(0deg) translateY(-14px)} .p2{transform:rotate(45deg) translateY(-14px)}
.p3{transform:rotate(90deg) translateY(-14px)} .p4{transform:rotate(135deg) translateY(-14px)}
.p5{transform:rotate(180deg) translateY(-14px)} .p6{transform:rotate(225deg) translateY(-14px)}
.p7{transform:rotate(270deg) translateY(-14px)} .p8{transform:rotate(315deg) translateY(-14px)}
.center{
  position:absolute;left:38px;top:38px;width:37px;height:37px;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#a46e18,#69400c 72%);z-index:5
}
.f1{left:24px;top:190px}.f2{left:84px;top:86px}
.f3{left:176px;top:22px}.f4{left:250px;top:136px}
.f5{left:330px;top:40px}.f6{left:410px;top:113px}
.f7{left:418px;top:218px}.f8{left:142px;top:209px}

.intro-card{
  border:1px solid #dec45d;border-radius:24px;background:rgba(255,255,255,.7);
  padding:15px;display:flex;flex-direction:column;justify-content:center;gap:12px;text-align:center
}
.intro-card .big{font-size:45px}
.intro-card h2{margin:0;font-size:22px;color:#665108}
.intro-card p{margin:0;font-size:14px;line-height:1.55;color:#726631}
.startBtn{
  border:none;padding:12px 14px;border-radius:14px;background:linear-gradient(90deg,#ffc817,#ffe774);
  color:#594500;font-weight:900;cursor:pointer
}

.quiz{
  margin-top:12px;border:1px solid #dec45d;border-radius:24px;background:rgba(255,255,255,.72);
  padding:16px;display:none
}
.quiz.show{display:block}
.quiz-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:11px}
.quiz-head h2{margin:0;font-size:21px;color:#665108}
.counter{font-size:12px;font-weight:900;color:#8b741a}
.track{height:8px;border-radius:999px;background:#eee2aa;overflow:hidden;margin-bottom:14px}
.bar{width:0%;height:100%;background:linear-gradient(90deg,#d9aa00,#ffe36f);transition:.3s ease}
.question{font-size:17px;font-weight:800;margin-bottom:12px;text-align:center;color:#5f4e12}
.options{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.option{
  border:1px solid #e1c75e;background:#fffdf1;color:#62562a;padding:13px;border-radius:15px;
  cursor:pointer;font-size:14px;font-weight:700;text-align:left;min-height:52px;transition:.18s ease
}
.option:hover{background:#fff6c4;transform:translateY(-2px)}
.option.selected{background:#fff0a1;border-color:#cfa619;box-shadow:0 0 0 2px rgba(207,166,25,.12)}
.feedback{
  margin-top:10px;min-height:58px;display:flex;align-items:center;justify-content:center;text-align:center;
  border:1px dashed #dac05b;border-radius:14px;background:#fff9dd;padding:10px;
  font-size:13px;line-height:1.45;color:#695d2c
}
.nextBtn{
  display:none;width:100%;margin-top:10px;border:none;padding:11px 13px;border-radius:14px;
  background:linear-gradient(90deg,#ffc817,#ffe774);color:#584400;font-weight:900;cursor:pointer
}

.final{
  display:none;margin-top:12px;border:1px solid #dec45d;border-radius:24px;
  background:linear-gradient(160deg,#fffef3,#fff0a4);padding:18px;text-align:center
}
.final h2{margin:0 0 7px;color:#665108}
.final p{margin:0;line-height:1.65;color:#665a2b}
.final-profile{
  margin:12px auto 0;max-width:720px;padding:14px;border-radius:16px;
  border:1px solid #dfc359;background:rgba(255,255,255,.72);
  line-height:1.6;color:#625627
}
.restart{
  margin-top:12px;border:none;background:transparent;text-decoration:underline;
  color:#927718;cursor:pointer;font-size:12px
}
.spark{
  position:absolute;top:-25px;pointer-events:none;z-index:100;animation:fall 3s linear forwards
}
@keyframes fall{to{transform:translateY(560px) rotate(500deg);opacity:.1}}

@media(max-width:780px){
  .hero{grid-template-columns:1fr}
  .visual{height:450px}
  .bouquet{transform:translateX(-50%) scale(.82);transform-origin:bottom center}
  .options{grid-template-columns:1fr}
}
@media(prefers-reduced-motion:reduce){.flower,.spark{animation:none}}
</style>

<section class="wrap">
  <header class="top">
    <span class="date">🌻 21 DE SEPTIEMBRE</span>
    <h1>Flores amarillas para ti</h1>
    <p>
      Un detalle por el día de las flores amarillas. Mira tu ramo y responde unas preguntas;
      cada opción que marques tendrá su propio mensaje.
    </p>
  </header>

  <div class="hero">
    <div class="visual" id="visual">
      <div class="sun"></div>
      <div class="cloud c1"></div>
      <div class="cloud c2"></div>

      <div class="bouquet">
        <div class="glow"></div>
        <div class="stem s1"></div><div class="stem s2"></div><div class="stem s3"></div><div class="stem s4"></div>
        <div class="stem s5"></div><div class="stem s6"></div><div class="stem s7"></div><div class="stem s8"></div>

        <div class="flower f1"><span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span><span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span></div>
        <div class="flower f2"><span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span><span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span></div>
        <div class="flower f3"><span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span><span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span></div>
        <div class="flower f4"><span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span><span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span></div>
        <div class="flower f5"><span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span><span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span></div>
        <div class="flower f6"><span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span><span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span></div>
        <div class="flower f7"><span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span><span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span></div>
        <div class="flower f8"><span class="pet p1"></span><span class="pet p2"></span><span class="pet p3"></span><span class="pet p4"></span><span class="pet p5"></span><span class="pet p6"></span><span class="pet p7"></span><span class="pet p8"></span><span class="center"></span></div>

        <div class="paper"></div>
        <div class="ribbon"></div>
      </div>
    </div>

    <aside class="intro-card" id="introCard">
      <div class="big">🌻</div>
      <h2>Antes del mensaje final...</h2>
      <p>Marca tus respuestas. Cada opción te devolverá un mensaje distinto y al final tendrás un cierre según lo que elegiste.</p>
      <button type="button" class="startBtn" id="startBtn">Empezar ✨</button>
    </aside>
  </div>

  <section class="quiz" id="quiz">
    <div class="quiz-head">
      <h2>Unas preguntas rápidas</h2>
      <span class="counter" id="counter">1 / 4</span>
    </div>
    <div class="track"><div class="bar" id="bar"></div></div>
    <div class="question" id="question"></div>
    <div class="options" id="options"></div>
    <div class="feedback" id="feedback">Elige una opción 😊</div>
    <button type="button" class="nextBtn" id="nextBtn">Siguiente →</button>
  </section>

  <section class="final" id="final">
    <h2>🌻 Y ahora sí...</h2>
    <p>
      <b>Feliz día de las flores amarillas.</b><br><br>
      Te dejo este ramo como un detalle de amistad y buena onda.
    </p>
    <div class="final-profile" id="finalProfile"></div>
    <button type="button" class="restart" id="restart">Volver a responder</button>
  </section>
</section>

<script>
(() => {
  const root=document.getElementById("flowers-quiz-personal");
  if(!root || root.dataset.ready==="1") return;
  root.dataset.ready="1";

  const startBtn=root.querySelector("#startBtn");
  const introCard=root.querySelector("#introCard");
  const quiz=root.querySelector("#quiz");
  const questionEl=root.querySelector("#question");
  const optionsEl=root.querySelector("#options");
  const feedback=root.querySelector("#feedback");
  const nextBtn=root.querySelector("#nextBtn");
  const counter=root.querySelector("#counter");
  const bar=root.querySelector("#bar");
  const final=root.querySelector("#final");
  const finalProfile=root.querySelector("#finalProfile");
  const restart=root.querySelector("#restart");
  const visual=root.querySelector("#visual");

  const questions=[
    {
      q:"¿Qué hace especial una buena amistad?",
      opts:[
        "😂 Reírse por cualquier cosa",
        "🤝 Poder contar con alguien",
        "☕ Conversar de todo",
        "✨ Todas las anteriores"
      ],
      fb:[
        "😂 Entonces contigo nunca deberían faltar las risas. A veces eso basta para arreglar un día pesado.",
        "🤝 Eso dice mucho: valoras la presencia de alguien cuando realmente importa.",
        "☕ Eres de quienes disfrutan una buena conversación sin mirar el reloj.",
        "✨ Esa respuesta lo resume bien: confianza, conversación y muchas risas."
      ],
      tags:["risa","apoyo","conversacion","completo"]
    },
    {
      q:"¿Qué plan simple nunca falla?",
      opts:[
        "☕ Café y conversación",
        "🍟 Comer algo y hablar",
        "🚶 Salir a caminar",
        "😂 Cualquier plan con buena compañía"
      ],
      fb:[
        "☕ Plan tranquilo, conversación larga y cero apuro. Buena elección.",
        "🍟 Comer algo mientras se habla de todo siempre termina siendo buen plan.",
        "🚶 Caminar y conversar tiene algo simple que hace que todo fluya.",
        "😂 Correcto: al final importa menos el plan y más con quién estás."
      ],
      tags:["tranquilo","comida","paseo","compania"]
    },
    {
      q:"¿Qué detalle se recuerda más?",
      opts:[
        "📱 Un mensaje inesperado",
        "😂 Una risa en mal momento",
        "🤝 Estar cuando hace falta",
        "🌻 Un detalle sin motivo"
      ],
      fb:[
        "📱 Esos mensajes llegan sin aviso y a veces cambian completamente el día.",
        "😂 Poder sacar una sonrisa justo cuando hace falta vale muchísimo.",
        "🤝 Esta respuesta habla de una amistad que se demuestra con hechos.",
        "🌻 Justamente como hoy: un detalle sencillo, sin necesidad de tanta explicación."
      ],
      tags:["mensaje","humor","presencia","detalle"]
    },
    {
      q:"Para terminar: ¿qué deseas que nunca falte?",
      opts:[
        "✨ Buenos momentos",
        "😂 Muchas risas",
        "🤝 Buena amistad",
        "🌻 Todo eso y más"
      ],
      fb:[
        "✨ Entonces que sigan llegando momentos que valga la pena recordar.",
        "😂 Que nunca falten razones para reírse hasta de las cosas más simples.",
        "🤝 Que siempre existan personas con quienes se pueda contar de verdad.",
        "🌻 Esa respuesta merece el ramo completo: buenos momentos, risas y amistad."
      ],
      tags:["momentos","risa","amistad","todo"]
    }
  ];

  let index=0;
  let answered=false;
  let answers=[];

  function confetti(n=18){
    const icons=["🌻","🌼","✨"];
    for(let i=0;i<n;i++){
      const e=document.createElement("span");
      e.className="spark";
      e.textContent=icons[Math.floor(Math.random()*icons.length)];
      e.style.left=(8+Math.random()*84)+"%";
      e.style.fontSize=(14+Math.random()*14)+"px";
      e.style.animationDelay=(Math.random()*.4)+"s";
      visual.appendChild(e);
      setTimeout(()=>e.remove(),3500);
    }
  }

  function render(){
    answered=false;
    const item=questions[index];
    counter.textContent=(index+1)+" / "+questions.length;
    bar.style.width=(index/questions.length*100)+"%";
    questionEl.textContent=item.q;
    feedback.textContent="Elige una opción 😊";
    nextBtn.style.display="none";
    optionsEl.innerHTML="";

    item.opts.forEach((txt,i)=>{
      const b=document.createElement("button");
      b.type="button";
      b.className="option";
      b.textContent=txt;
      b.addEventListener("click",()=>{
        [...optionsEl.children].forEach(x=>x.classList.remove("selected"));
        b.classList.add("selected");
        feedback.textContent=item.fb[i];
        answers[index]={choice:i, tag:item.tags[i]};
        answered=true;
        nextBtn.style.display="block";
      });
      optionsEl.appendChild(b);
    });

    nextBtn.textContent=index===questions.length-1 ? "Ver mensaje final 🌻" : "Siguiente →";
  }

  function buildFinal(){
    const tags=answers.map(a=>a.tag);
    let lines=[];

    if(tags.includes("risa") || tags.includes("humor")){
      lines.push("😂 Se nota que para ti una amistad también se disfruta riéndose hasta de las cosas más simples.");
    }
    if(tags.includes("apoyo") || tags.includes("presencia") || tags.includes("amistad")){
      lines.push("🤝 También valoras mucho saber que hay alguien presente cuando realmente hace falta.");
    }
    if(tags.includes("conversacion") || tags.includes("tranquilo")){
      lines.push("☕ Y eres de quienes disfrutan esas conversaciones largas que terminan haciendo bien.");
    }
    if(tags.includes("detalle") || tags.includes("mensaje")){
      lines.push("🌻 Los pequeños detalles también cuentan, especialmente cuando llegan sin esperarlos.");
    }
    if(tags.includes("compania") || tags.includes("todo") || tags.includes("completo")){
      lines.push("✨ Al final, para ti lo importante es compartir buenos momentos con personas que suman.");
    }
    if(lines.length<2){
      lines.push("🌼 Tus respuestas muestran que valoras los momentos simples, la buena onda y una amistad sincera.");
    }

    finalProfile.innerHTML =
      "<b>Según lo que marcaste:</b><br><br>" +
      lines.join("<br><br>") +
      "<br><br><b>Así que este ramo amarillo va perfecto para ti hoy. 🌻</b>";
  }

  startBtn.addEventListener("click",()=>{
    quiz.classList.add("show");
    introCard.innerHTML="<div class='big'>🌼</div><h2>Tu ramo ya está listo</h2><p>Ahora marca tus respuestas. Cada una te dará un mensaje diferente.</p>";
    render();
    quiz.scrollIntoView({behavior:"smooth",block:"start"});
  });

  nextBtn.addEventListener("click",()=>{
    if(!answered) return;
    if(index<questions.length-1){
      index++;
      render();
    }else{
      bar.style.width="100%";
      quiz.style.display="none";
      buildFinal();
      final.style.display="block";
      confetti(34);
      final.scrollIntoView({behavior:"smooth",block:"center"});
    }
  });

  restart.addEventListener("click",()=>{
    index=0;
    answered=false;
    answers=[];
    final.style.display="none";
    quiz.style.display="block";
    quiz.classList.add("show");
    render();
    quiz.scrollIntoView({behavior:"smooth",block:"start"});
  });
})();
</script>
</div>
"""

components.html(html, height=1080, scrolling=True)
