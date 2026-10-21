import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# ============================================================
#  👇👇👇  个性化配置区：你只需要改这一块  👇👇👇
# ============================================================

FRIEND_NAME = "小美"          # 朋友的名字
SENDER_NAME = "你的名字"       # 你的名字

# ---- 信的内容（随便换行，想写多长写多长）----
LETTER = """亲爱的朋友：

生日快乐！

认识你是一件很幸运的事情。这一年里，我们一起……

希望新的一岁里，你能每天都开心，想要的都能得到，想去的都能去到。

无论什么时候，需要我的时候，我一直都在。

                                                       —— 你的好朋友
"""

# ---- 「心里话」卡片，每一条是一段，可以用 <b>加粗</b> 和 <br> 换行 ----
THOUGHTS = [
    "<b>第一次见面</b><br>还记得我们第一次见面的时候吗？那时候我还不知道，后来会和你变成这么好的朋友。",
    "<b>谢谢你</b><br>谢谢你在我不开心的时候陪我聊天，谢谢你总是记得我随口说过的话。",
    "<b>关于你的好</b><br>你比你自己以为的要好很多很多。别老是否定自己，你真的特别棒。",
    "<b>以后</b><br>以后的每一年生日，我都想陪着你过。这是我们之间的约定。",
]

PHOTO_DIR = Path("photos")     # 照片文件夹
IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}

# ============================================================
#  👆👆👆  配置区结束，下面是代码，基本不用动  👆👆👆
# ============================================================

st.set_page_config(
    page_title=f"生日快乐 · {FRIEND_NAME}",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- 全局样式 ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background: radial-gradient(circle at 20% 8%, #2b1055 0%, #0d0221 45%, #04010d 100%);
}
html, body, [class*="css"] {
    color: #f0e9ff;
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
}

/* 顶部大标题 */
.hero { text-align: center; padding: 8px 0 0 0; }
.hero h1 {
    font-size: clamp(2rem, 5.5vw, 3.6rem);
    margin: 0;
    font-weight: 800;
    letter-spacing: 3px;
    background: linear-gradient(90deg, #ffd86f, #fc6262, #ff6bcb, #7f7fd5, #ffd86f);
    background-size: 300% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: shine 6s linear infinite;
}
@keyframes shine {
    0%   { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}
.hero p {
    color: #cbbde0;
    font-size: 1.05rem;
    margin-top: 10px;
    letter-spacing: 1px;
}

/* 区块小标题 */
.section-title {
    text-align: center;
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffd86f;
    margin: 10px 0 22px 0;
    letter-spacing: 2px;
}

/* 信纸 */
.letter-card {
    background: linear-gradient(180deg, #fffdf7 0%, #fbf1e0 100%);
    color: #3a2b1f;
    border-radius: 18px;
    padding: 38px 42px;
    line-height: 2.1;
    font-size: 1.05rem;
    white-space: pre-wrap;
    box-shadow: 0 20px 55px rgba(0,0,0,0.55);
    border: 1px solid #e8d9c0;
    font-family: "Georgia", "Songti SC", "STSong", serif;
    animation: fadeUp 0.9s ease both;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* 心里话卡片 */
.thought-card {
    background: rgba(255,255,255,0.06);
    border-left: 4px solid #ff6bcb;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 18px;
    line-height: 1.95;
    font-size: 1.02rem;
    color: #efe7ff;
    box-shadow: 0 8px 26px rgba(0,0,0,0.28);
    animation: fadeUp 0.8s ease both;
}
.thought-card b { color: #ffd86f; }

/* 底部落款 */
.footer-note {
    text-align: center;
    color: #9b8ec2;
    font-size: 0.95rem;
    padding: 40px 0 60px 0;
    letter-spacing: 2px;
}

/* 图片圆角 + 阴影 */
img { border-radius: 16px; }

/* Tab 样式 */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    justify-content: center;
    margin-bottom: 18px;
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.07);
    border-radius: 999px;
    padding: 9px 24px;
    color: #d9cff0;
    font-size: 1rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #ff6bcb, #7f7fd5) !important;
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- 烟花组件 ----------------
FIREWORKS_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
  html, body { margin:0; padding:0; overflow:hidden; background:transparent; }
  canvas { display:block; width:100%; height:100%; cursor:crosshair; }
</style>
</head>
<body>
<canvas id="fw"></canvas>
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
const gravity  = 0.035;
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
  ctx.fillStyle = 'rgba(5, 2, 20, 0.16)';
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


# ================= 页面内容 =================

# 1. 标题
st.markdown(f"""
<div class="hero">
  <h1>🎂 {FRIEND_NAME}，生日快乐 🎂</h1>
  <p>愿你所愿皆成真，愿你所得皆欢喜 ✨</p>
</div>
""", unsafe_allow_html=True)

# 2. 烟花
components.html(FIREWORKS_HTML, height=420, scrolling=False)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# 3. 三个模块
tab1, tab2, tab3 = st.tabs(["💌  写给你的信", "📸  我们的照片", "💭  一些心里话"])

# ---------- 信 ----------
with tab1:
    st.markdown('<div class="section-title">💌 有一封信想给你</div>', unsafe_allow_html=True)

    if "letter_opened" not in st.session_state:
        st.session_state.letter_opened = False

    left, mid, right = st.columns([1, 2, 1])
    with mid:
        if not st.session_state.letter_opened:
            if st.button("💌  点我拆开这封信", use_container_width=True):
                st.session_state.letter_opened = True
                st.rerun()
        else:
            st.markdown(f'<div class="letter-card">{LETTER}</div>', unsafe_allow_html=True)

# ---------- 照片 ----------
with tab2:
    st.markdown('<div class="section-title">📸 我们的回忆</div>', unsafe_allow_html=True)

    files = []
    if PHOTO_DIR.exists():
        files = sorted(
            [p for p in PHOTO_DIR.iterdir() if p.suffix.lower() in IMG_EXTS]
        )

    if not files:
        st.info("📁 还没有照片哦～ 在项目里新建一个 `photos` 文件夹，把照片丢进去就行啦。")
    else:
        cols = st.columns(2)
        for i, f in enumerate(files):
            with cols[i % 2]:
                caption = f.stem.replace("_", " ")
                try:
                    st.image(str(f), use_container_width=True, caption=caption)
                except TypeError:
                    st.image(str(f), use_column_width=True, caption=caption)
                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# ---------- 心里话 ----------
with tab3:
    st.markdown('<div class="section-title">💭 一些平时说不出口的话</div>', unsafe_allow_html=True)

    left, mid, right = st.columns([1, 3, 1])
    with mid:
        for item in THOUGHTS:
            st.markdown(f'<div class="thought-card">{item}</div>', unsafe_allow_html=True)

# 4. 底部
st.markdown(f"""
<div class="footer-note">
    —— 来自 {SENDER_NAME} 的一点小心意 🎁
</div>
""", unsafe_allow_html=True)
