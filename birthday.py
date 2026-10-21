import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import html

# ============================================================
#  👇 个性化配置区：只改这里
# ============================================================

FRIEND_NAME = "小美"
SENDER_NAME = "你的名字"

LETTER = """亲爱的朋友：

生日快乐！

认识你是一件很幸运的事情。这一年里，我们一起……

希望新的一岁里，你能每天都开心，想要的都能得到，想去的都能去到。

无论什么时候，需要我的时候，我一直都在。

                                        —— 你的好朋友
"""

THOUGHTS = [
    ("第一次见面", "还记得我们第一次见面的时候吗？那时候我还不知道，后来会和你变成这么好的朋友。"),
    ("谢谢你", "谢谢你在我不开心的时候陪我聊天，谢谢你总是记得我随口说过的话。"),
    ("关于你的好", "你比你自己以为的要好很多很多。别老是否定自己，你真的特别棒。"),
    ("以后", "以后的每一年生日，我都想陪着你过。这是我们之间的约定。"),
]

PHOTO_DIR = Path("photos")
IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
PHOTO_ROTATIONS = [-2.4, 1.8, -1.2, 2.2, -1.8, 1.5, -2.2, 2.5]

# ============================================================
#  👆 配置区结束
# ============================================================

st.set_page_config(
    page_title=f"生日快乐 · {FRIEND_NAME}",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Patrick+Hand&family=Ma+Shan+Zheng&display=swap');

#MainMenu, footer, header {visibility: hidden;}
[data-testid="stToolbar"] {display: none;}
[data-testid="stDecoration"] {display: none;}

.stApp {
    background-color: #fdfbf7 !important;
    background-image:
        radial-gradient(#e5e0d8 1px, transparent 1px),
        radial-gradient(#e5e0d8 1px, transparent 1px) !important;
    background-size: 24px 24px, 24px 24px !important;
    background-position: 0 0, 12px 12px !important;
    color: #2d2d2d !important;
    font-family: 'Patrick Hand', 'Ma Shan Zheng', cursive !important;
}

html, body, p, div, span, label, .stMarkdown, .stText {
    font-family: 'Patrick Hand', 'Ma Shan Zheng', cursive !important;
    color: #2d2d2d;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Kalam', 'Ma Shan Zheng', cursive !important;
    font-weight: 700 !important;
    color: #2d2d2d !important;
}

.block-container {
    max-width: 1100px !important;
    padding-top: 1.5rem !important;
}

/* ---------- Hero ---------- */
.hero { text-align: center; padding: 12px 0 6px; }
.hero-title {
    font-family: 'Kalam', 'Ma Shan Zheng', cursive !important;
    font-size: clamp(2.4rem, 6vw, 4.4rem) !important;
    font-weight: 700 !important;
    margin: 0;
    display: inline-block;
    transform: rotate(-1.5deg);
    line-height: 1.2;
    color: #2d2d2d !important;
}
.hero-title .name { color: #2d5da1; }
.hero-title .accent { color: #ff4d4d; display: inline-block; transform: rotate(1deg); }
.hero-underline { width: 82%; max-width: 440px; margin: -6px auto 0; display: block; }
.hero-sub {
    font-family: 'Patrick Hand', 'Ma Shan Zheng', cursive !important;
    font-size: 1.25rem;
    color: #2d2d2d;
    margin-top: 12px;
    transform: rotate(0.4deg);
    display: inline-block;
    padding: 3px 16px;
    border-bottom: 2px dashed #2d5da1;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 16px !important;
    justify-content: center !important;
    background: transparent !important;
    border-bottom: none !important;
    margin: 14px 0 30px !important;
    flex-wrap: wrap;
    padding: 8px 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Patrick Hand', 'Ma Shan Zheng', cursive !important;
    font-size: 1.12rem !important;
    background: #ffffff !important;
    color: #2d2d2d !important;
    border: 2.5px solid #2d2d2d !important;
    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px !important;
    padding: 10px 24px !important;
    box-shadow: 3px 3px 0px 0px #2d2d2d !important;
    transition: all 0.12s ease !important;
    height: auto !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: #e5e0d8 !important;
    transform: translate(1px, 1px) rotate(-1deg) !important;
    box-shadow: 2px 2px 0px 0px #2d2d2d !important;
}
.stTabs [aria-selected="true"] {
    background: #ff4d4d !important;
    color: #ffffff !important;
    transform: translate(2px, 2px) rotate(-1.5deg) !important;
    box-shadow: 1px 1px 0px 0px #2d2d2d !important;
}
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] div { color: #ffffff !important; }
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 6px; }

/* ---------- Button ---------- */
.stButton > button {
    font-family: 'Patrick Hand', 'Ma Shan Zheng', cursive !important;
    font-size: 1.18rem !important;
    background: #ffffff !important;
    color: #2d2d2d !important;
    border: 3px solid #2d2d2d !important;
    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px !important;
    box-shadow: 4px 4px 0px 0px #2d2d2d !important;
    padding: 12px 28px !important;
    transition: all 0.1s ease !important;
    min-height: 48px;
}
.stButton > button:hover {
    background: #ff4d4d !important;
    color: #ffffff !important;
    border-color: #2d2d2d !important;
    transform: translate(2px, 2px) rotate(-1deg) !important;
    box-shadow: 2px 2px 0px 0px #2d2d2d !important;
}
.stButton > button:active {
    background: #ff4d4d !important;
    color: #ffffff !important;
    transform: translate(4px, 4px) !important;
    box-shadow: 0 0 0 0 #2d2d2d !important;
    border-color: #2d2d2d !important;
}

/* ---------- Section title ---------- */
.section-title {
    text-align: center;
    font-family: 'Kalam', 'Ma Shan Zheng', cursive !important;
    font-size: 1.7rem;
    font-weight: 700;
    color: #2d2d2d;
    margin: 10px 0 12px;
    display: block;
}
.section-title .marker { color: #ff4d4d; }

/* ---------- Letter ---------- */
.letter-wrap { display: flex; justify-content: center; padding: 10px 0 20px; }
.letter-card {
    position: relative;
    background: #ffffff;
    border: 3px solid #2d2d2d;
    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px;
    padding: 48px 52px 40px;
    box-shadow: 6px 6px 0px 0px #2d2d2d;
    transform: rotate(-0.6deg);
    font-family: 'Kalam', 'Ma Shan Zheng', cursive !important;
    font-size: 1.16rem;
    line-height: 2.15;
    color: #2d2d2d;
    white-space: pre-wrap;
    max-width: 720px;
    width: 100%;
    animation: fadeUp 0.6s ease both;
}
.letter-card::before {
    content: '';
    position: absolute;
    top: -16px; left: 50%;
    transform: translateX(-50%) rotate(-2deg);
    width: 130px; height: 30px;
    background: rgba(229, 224, 216, 0.9);
    border: 1px dashed rgba(45, 45, 45, 0.25);
    box-shadow: 0 1px 2px rgba(0,0,0,0.06);
}
@keyframes fadeUp {
    from { opacity: 0; transform: rotate(-0.6deg) translateY(24px); }
    to   { opacity: 1; transform: rotate(-0.6deg) translateY(0); }
}
.envelope-hint {
    font-family: 'Patrick Hand', 'Ma Shan Zheng', cursive !important;
    font-size: 1.15rem;
    color: #2d5da1;
    transform: rotate(-1deg);
    display: inline-block;
    padding: 6px 0;
}

/* ---------- Photo (Polaroid) ---------- */
.photo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 34px;
    padding: 22px 10px 30px;
}
.polaroid {
    background: #ffffff;
    padding: 14px 14px 54px 14px;
    border: 2px solid #2d2d2d;
    box-shadow: 5px 5px 0px 0px #2d2d2d;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    position: relative;
}
.polaroid:hover {
    transform: rotate(0deg) scale(1.04) !important;
    box-shadow: 3px 3px 0px 0px #2d2d2d;
    z-index: 2;
}
.polaroid img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
    border: 1px solid #2d2d2d;
    background: #e5e0d8;
}
.polaroid-caption {
    position: absolute;
    bottom: 14px; left: 0; right: 0;
    font-family: 'Kalam', 'Ma Shan Zheng', cursive !important;
    font-size: 1.1rem;
    text-align: center;
    color: #2d2d2d;
    transform: rotate(-1deg);
    padding: 0 12px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ---------- Thought sticky notes ---------- */
.thought-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 26px;
    max-width: 780px;
    margin: 10px auto 20px;
    padding: 0 8px;
}
.thought-card {
    position: relative;
    background: #fff9c4;
    border: 2.5px solid #2d2d2d;
    border-radius: 15px 225px 15px 255px / 255px 15px 225px 15px;
    padding: 26px 30px 24px;
    box-shadow: 4px 4px 0px 0px #2d2d2d;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    transform: rotate(-0.8deg);
    font-family: 'Patrick Hand', 'Ma Shan Zheng', cursive !important;
    font-size: 1.1rem;
    line-height: 1.85;
    color: #2d2d2d;
}
.thought-card:nth-child(even) {
    transform: rotate(1deg);
    background: #ffffff;
    border-radius: 225px 15px 255px 15px / 15px 255px 15px 225px;
}
.thought-card:hover {
    transform: rotate(0deg) translate(-2px, -2px);
    box-shadow: 6px 6px 0px 0px #2d2d2d;
    z-index: 2;
}
.thought-card::before {
    content: '';
    position: absolute;
    top: -9px; left: 26px;
    width: 18px; height: 18px;
    background: radial-gradient(circle at 32% 30%, #ff8a8a 0%, #ff4d4d 55%, #b82020 100%);
    border-radius: 50%;
    border: 1.5px solid #2d2d2d;
    box-shadow: 0 2px 3px rgba(0,0,0,0.35);
}
.thought-card:nth-child(even)::before {
    left: auto; right: 26px;
    background: radial-gradient(circle at 32% 30%, #6ea3e8 0%, #2d5da1 55%, #163a6d 100%);
}
.thought-title {
    font-family: 'Kalam', 'Ma Shan Zheng', cursive !important;
    font-size: 1.3rem;
    font-weight: 700;
    color: #ff4d4d;
    margin-bottom: 8px;
    display: inline-block;
    border-bottom: 2px dashed rgba(45,45,45,0.25);
    padding-bottom: 2px;
}
.thought-card:nth-child(even) .thought-title { color: #2d5da1; }

/* ---------- iframe ---------- */
iframe { border: none !important; }

/* ---------- Footer ---------- */
.footer-note {
    text-align: center;
    font-family: 'Kalam', 'Ma Shan Zheng', cursive !important;
    font-size: 1.14rem;
    color: #2d2d2d;
    padding: 46px 0 70px;
    transform: rotate(-0.5deg);
    letter-spacing: 1px;
}
.footer-note span {
    border-bottom: 2px dashed #ff4d4d;
    padding-bottom: 2px;
}

/* ---------- st.info ---------- */
.stAlert, [data-testid="stNotification"] {
    background: #fff9c4 !important;
    border: 2px solid #2d2d2d !important;
    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px !important;
    box-shadow: 3px 3px 0px 0px #2d2d2d !important;
    color: #2d2d2d !important;
}

/* ---------- Responsive ---------- */
@media (max-width: 768px) {
    .letter-card { padding: 32px 24px 28px; font-size: 1.08rem; }
    .thought-card { padding: 22px 20px; font-size: 1.03rem; }
    .photo-grid { grid-template-columns: 1fr; gap: 26px; }
    .hero-sub { font-size: 1.1rem; }
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ---------------- 烟花（外包一层手绘相框）----------------
FIREWORKS_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
  html, body {
    margin: 0; padding: 0; overflow: hidden;
    background: transparent;
    font-family: 'Patrick Hand', cursive;
  }
  .frame {
    position: relative;
    width: calc(100% - 26px);
    height: calc(100% - 26px);
    margin: 13px;
    background: linear-gradient(180deg, #1e1b3a 0%, #0d0a20 100%);
    border: 3px solid #2d2d2d;
    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px;
    box-shadow: 6px 6px 0px 0px #2d2d2d;
    overflow: hidden;
    transform: rotate(-0.4deg);
  }
  .frame::before {
    content: '';
    position: absolute;
    top: -16px; left: 50%;
    transform: translateX(-50%) rotate(-2deg);
    width: 140px; height: 30px;
    background: rgba(229, 224, 216, 0.92);
    border: 1px dashed rgba(45, 45, 45, 0.28);
    z-index: 10;
    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
  }
  canvas { display: block; width: 100%; height: 100%; cursor: crosshair; }
</style>
</head>
<body>
<div class="frame">
  <canvas id="fw"></canvas>
</div>
<script>
const canvas = document.getElementById('fw');
const ctx = canvas.getContext('2d');
let W = 1, H = 1;

function resize(){
  const dpr = window.devicePixelRatio || 1;
  W = canvas.clientWidth || 1;
  H = canvas.clientHeight || 1;
  canvas.width  = W * dpr;
  canvas.height = H * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

const particles = [];
const gravity = 0.035;
const friction = 0.985;
const rnd = (a, b) => a + Math.random() * (b - a);

function explode(x, y){
  const hue   = Math.random() * 360;
  const count = 70 + Math.floor(Math.random() * 50);
  const power = rnd(2.2, 5.2);
  for (let i = 0; i < count; i++){
    const angle = Math.random() * Math.PI * 2;
    const speed = power * Math.pow(Math.random(), 0.6);
    particles.push({
      x, y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      life: 1,
      decay: rnd(0.007, 0.018),
      hue: hue + rnd(-25, 25),
      size: rnd(1.2, 2.6)
    });
  }
  for (let i = 0; i < 14; i++){
    const angle = Math.random() * Math.PI * 2;
    particles.push({
      x, y,
      vx: Math.cos(angle) * rnd(0.5, 2),
      vy: Math.sin(angle) * rnd(0.5, 2),
      life: 1, decay: 0.05, hue: hue, size: 2.2
    });
  }
}

function launch(){
  explode(rnd(W * 0.12, W * 0.88), rnd(H * 0.15, H * 0.62));
}

function loop(){
  ctx.globalCompositeOperation = 'source-over';
  ctx.fillStyle = 'rgba(13, 10, 32, 0.16)';
  ctx.fillRect(0, 0, W, H);
  ctx.globalCompositeOperation = 'lighter';

  for (let i = particles.length - 1; i >= 0; i--){
    const p = particles[i];
    p.vx *= friction;
    p.vy = p.vy * friction + gravity;
    p.x += p.vx;
    p.y += p.vy;
    p.life -= p.decay;
    if (p.life <= 0 || p.y > H + 30){ particles.splice(i, 1); continue; }
    ctx.beginPath();
    ctx.fillStyle = 'hsla(' + p.hue + ', 100%, ' + (55 + p.life * 20) + '%, ' + p.life + ')';
    ctx.arc(p.x, p.y, Math.max(p.size * p.life, 0.4), 0, Math.PI * 2);
    ctx.fill();
  }
  requestAnimationFrame(loop);
}

canvas.addEventListener('click', function(e){
  const rect = canvas.getBoundingClientRect();
  explode(e.clientX - rect.left, e.clientY - rect.top);
});
window.addEventListener('resize', resize);
requestAnimationFrame(function(){ resize(); loop(); });
setTimeout(launch, 200);
setInterval(launch, 750);
</script>
</body>
</html>
"""


# ---------------- Hero ----------------
st.markdown(f'''
<div class="hero">
    <h1 class="hero-title">
        <span class="name">{html.escape(FRIEND_NAME)}</span>，<span class="accent">生日快乐</span>
        <span style="display:inline-block;transform:rotate(-14deg);">🎉</span>
    </h1>
    <svg class="hero-underline" viewBox="0 0 420 14" preserveAspectRatio="none">
        <path d="M2,8 Q22,2 42,8 T82,8 T122,8 T162,8 T202,8 T242,8 T282,8 T322,8 T362,8 T402,8"
              stroke="#ff4d4d" stroke-width="3" fill="none" stroke-linecap="round"/>
    </svg>
    <div><span class="hero-sub">愿你所愿皆成真，愿你所得皆欢喜 ✨</span></div>
</div>
''', unsafe_allow_html=True)

# ---------------- 烟花 ----------------
components.html(FIREWORKS_HTML, height=440, scrolling=False)


# ---------------- 照片 base64 渲染 ----------------
def photo_to_html(path, caption, rotation):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    suffix = path.suffix.lower().lstrip(".")
    if suffix == "jpg":
        suffix = "jpeg"
    safe_caption = html.escape(caption)
    return (
        f'<div class="polaroid" style="transform: rotate({rotation}deg);">'
        f'<img src="data:image/{suffix};base64,{data}" alt="{safe_caption}" />'
        f'<div class="polaroid-caption">{safe_caption}</div>'
        f'</div>'
    )


# ---------------- Tabs ----------------
tab1, tab2, tab3 = st.tabs(["✉️  写给你的信", "📸  我们的照片", "💭  一些心里话"])

# --- 信 ---
with tab1:
    st.markdown(
        '<div class="section-title">一封<span class="marker">手写</span>的信</div>',
        unsafe_allow_html=True,
    )
    if "letter_opened" not in st.session_state:
        st.session_state.letter_opened = False

    if not st.session_state.letter_opened:
        st.markdown(
            '<div style="text-align:center;"><span class="envelope-hint">点击下面的按钮，拆开这封信 ✉️</span></div>',
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("✉️  拆开这封信", use_container_width=True):
                st.session_state.letter_opened = True
                st.rerun()
    else:
        letter_text = html.escape(LETTER)
        st.markdown(
            f'<div class="letter-wrap"><div class="letter-card">{letter_text}</div></div>',
            unsafe_allow_html=True,
        )

# --- 照片 ---
with tab2:
    st.markdown(
        '<div class="section-title">我们的<span class="marker">回忆</span></div>',
        unsafe_allow_html=True,
    )
    files = []
    if PHOTO_DIR.exists():
        files = sorted([p for p in PHOTO_DIR.iterdir() if p.suffix.lower() in IMG_EXTS])

    if not files:
        st.info("📁 还没有照片哦～ 在项目里新建一个 `photos` 文件夹，把照片丢进去就行啦。")
    else:
        parts = []
        for i, f in enumerate(files):
            caption = f.stem.replace("_", " ")
            rot = PHOTO_ROTATIONS[i % len(PHOTO_ROTATIONS)]
            parts.append(photo_to_html(f, caption, rot))
        st.markdown(f'<div class="photo-grid">{"".join(parts)}</div>', unsafe_allow_html=True)

# --- 心里话 ---
with tab3:
    st.markdown(
        '<div class="section-title">一些<span class="marker">心里话</span></div>',
        unsafe_allow_html=True,
    )
    parts = []
    for title, body in THOUGHTS:
        parts.append(
            f'<div class="thought-card">'
            f'<div class="thought-title">{html.escape(title)}</div>'
            f'<div>{html.escape(body)}</div>'
            f'</div>'
        )
    st.markdown(f'<div class="thought-grid">{"".join(parts)}</div>', unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown(
    f'<div class="footer-note">—— <span>来自 {html.escape(SENDER_NAME)} 的一点小心意</span> 🎁</div>',
    unsafe_allow_html=True,
)
