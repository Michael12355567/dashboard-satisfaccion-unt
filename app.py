import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(
    page_title="Flores Amarillas para una Amistad",
    page_icon="🌻",
    layout="centered"
)

# ---- ESTILOS GENERALES ----
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #fffdf1 0%, #fff7c8 55%, #fff0a6 100%);
    }

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        color: #8a6800;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #6b5a1c;
        font-size: 1.15rem;
        margin-bottom: 1.3rem;
    }

    .card {
        background: rgba(255,255,255,0.82);
        border: 1px solid rgba(230, 190, 30, 0.35);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 12px 35px rgba(112, 86, 0, 0.12);
        text-align: center;
        margin: 18px 0;
    }

    .message {
        font-size: 1.25rem;
        line-height: 1.8;
        color: #4e461f;
    }

    .signature {
        text-align: right;
        margin-top: 18px;
        font-style: italic;
        color: #7a6518;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 18px;
        border: none;
        background: linear-gradient(90deg, #f4c430, #ffd84d);
        color: #554200;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 0.8rem;
        box-shadow: 0 8px 18px rgba(173, 132, 0, 0.18);
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #ffd84d, #ffea86);
        color: #3f3300;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌻 Flores Amarillas 🌻</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Porque las amistades bonitas también merecen flores 💛</div>',
    unsafe_allow_html=True
)

# ---- ANIMACIÓN DE FLORES ----
flower_html = """
<!DOCTYPE html>
<html>
<head>
<style>
html, body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: transparent;
}
.scene {
    position: relative;
    height: 360px;
    width: 100%;
    overflow: hidden;
}
.sun {
    position: absolute;
    width: 95px;
    height: 95px;
    border-radius: 50%;
    background: #ffe168;
    top: 22px;
    right: 32px;
    box-shadow: 0 0 45px rgba(255, 216, 50, 0.55);
}
.ground {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 78px;
    background: linear-gradient(#9ecb65, #78ad45);
    border-radius: 55% 55% 0 0 / 25% 25% 0 0;
}
.flower {
    position: absolute;
    bottom: 58px;
    transform-origin: bottom center;
    animation: sway 3.2s ease-in-out infinite alternate;
}
.stem {
    width: 7px;
    height: 150px;
    background: #4e9a45;
    margin: auto;
    border-radius: 5px;
}
.head {
    position: absolute;
    left: 50%;
    top: -44px;
    transform: translateX(-50%);
    width: 74px;
    height: 74px;
}
.petals span {
    position: absolute;
    width: 30px;
    height: 46px;
    background: #ffd31a;
    border-radius: 50% 50% 45% 45%;
    left: 22px;
    top: 14px;
    transform-origin: 15px 23px;
    box-shadow: 0 2px 3px rgba(0,0,0,.08);
}
.petals span:nth-child(1){transform:rotate(0deg) translateY(-24px);}
.petals span:nth-child(2){transform:rotate(45deg) translateY(-24px);}
.petals span:nth-child(3){transform:rotate(90deg) translateY(-24px);}
.petals span:nth-child(4){transform:rotate(135deg) translateY(-24px);}
.petals span:nth-child(5){transform:rotate(180deg) translateY(-24px);}
.petals span:nth-child(6){transform:rotate(225deg) translateY(-24px);}
.petals span:nth-child(7){transform:rotate(270deg) translateY(-24px);}
.petals span:nth-child(8){transform:rotate(315deg) translateY(-24px);}
.center {
    position: absolute;
    width: 34px;
    height: 34px;
    background: #8b5a17;
    border-radius: 50%;
    left: 20px;
    top: 20px;
    z-index: 5;
}
.leaf {
    position: absolute;
    width: 44px;
    height: 22px;
    background: #5cab4f;
    border-radius: 100% 0 100% 0;
}
.leaf.left { left: -39px; top: 72px; transform: rotate(18deg); }
.leaf.right { right: -39px; top: 102px; transform: scaleX(-1) rotate(18deg); }

.f1 {left: 10%; animation-delay: .1s;}
.f2 {left: 27%; transform: scale(.86); animation-delay: .7s;}
.f3 {left: 47%; transform: scale(1.1); animation-delay: 1.3s;}
.f4 {left: 68%; transform: scale(.9); animation-delay: .4s;}
.f5 {left: 84%; transform: scale(.78); animation-delay: 1s;}

.sparkle {
    position: absolute;
    font-size: 24px;
    animation: float 4s ease-in-out infinite;
}
.s1 {left: 14%; top: 38px; animation-delay: .5s;}
.s2 {left: 38%; top: 62px; animation-delay: 1.4s;}
.s3 {left: 61%; top: 25px; animation-delay: 2s;}
.s4 {left: 78%; top: 90px; animation-delay: .9s;}

@keyframes sway {
    0% { rotate: -3deg; }
    100% { rotate: 4deg; }
}
@keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); opacity: .6; }
    50% { transform: translateY(-18px) rotate(12deg); opacity: 1; }
}
</style>
</head>
<body>
<div class="scene">
    <div class="sun"></div>
    <div class="sparkle s1">✨</div>
    <div class="sparkle s2">💛</div>
    <div class="sparkle s3">✨</div>
    <div class="sparkle s4">💛</div>

    <div class="flower f1">
        <div class="head"><div class="petals">
            <span></span><span></span><span></span><span></span>
            <span></span><span></span><span></span><span></span>
        </div><div class="center"></div></div>
        <div class="stem"><div class="leaf left"></div><div class="leaf right"></div></div>
    </div>

    <div class="flower f2">
        <div class="head"><div class="petals">
            <span></span><span></span><span></span><span></span>
            <span></span><span></span><span></span><span></span>
        </div><div class="center"></div></div>
        <div class="stem"><div class="leaf left"></div><div class="leaf right"></div></div>
    </div>

    <div class="flower f3">
        <div class="head"><div class="petals">
            <span></span><span></span><span></span><span></span>
            <span></span><span></span><span></span><span></span>
        </div><div class="center"></div></div>
        <div class="stem"><div class="leaf left"></div><div class="leaf right"></div></div>
    </div>

    <div class="flower f4">
        <div class="head"><div class="petals">
            <span></span><span></span><span></span><span></span>
            <span></span><span></span><span></span><span></span>
        </div><div class="center"></div></div>
        <div class="stem"><div class="leaf left"></div><div class="leaf right"></div></div>
    </div>

    <div class="flower f5">
        <div class="head"><div class="petals">
            <span></span><span></span><span></span><span></span>
            <span></span><span></span><span></span><span></span>
        </div><div class="center"></div></div>
        <div class="stem"><div class="leaf left"></div><div class="leaf right"></div></div>
    </div>

    <div class="ground"></div>
</div>
</body>
</html>
"""

components.html(flower_html, height=365, scrolling=False)

# ---- MENSAJE ----
st.markdown("""
<div class="card">
    <div class="message">
        Hoy no quería dejar pasar la oportunidad de regalarte
        <b>flores amarillas</b> 🌻💛.<br><br>
        No porque haga falta una fecha especial, sino porque una amistad bonita
        también merece detalles que recuerden lo valiosa que es.<br><br>
        Gracias por las conversaciones, las risas, los consejos y por estar
        presente incluso en los días más simples.<br><br>
        Que estas flores simbolicen mucha alegría, buenos momentos y todo lo
        bonito que todavía nos queda por vivir como amigos.
    </div>
    <div class="signature">Con cariño, para una gran amistad 💛</div>
</div>
""", unsafe_allow_html=True)

frases = [
    "🌻 Que nunca te falten motivos para sonreír.",
    "💛 Las buenas amistades hacen más bonitos los días.",
    "✨ Gracias por estar, incluso sin tener que decir mucho.",
    "🌼 Que siempre encuentres luz, alegría y personas sinceras.",
    "🌞 Una flor amarilla para recordarte lo especial que eres como amistad."
]

if st.button("💛 Regalar flores amarillas"):
    st.balloons()
    st.success(random.choice(frases))

st.markdown(
    "<p style='text-align:center;color:#78651a;margin-top:28px;'>Hecho con cariño 🌻</p>",
    unsafe_allow_html=True
)
