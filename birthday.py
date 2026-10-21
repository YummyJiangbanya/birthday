import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import html
import re
import pandas as pd

# ============================================================
#  👇 个性化配置区：只改这里
# ============================================================

FRIEND_NAME = "薛女士"
SENDER_NAME = "贾女士"
SUB_TITLE = "祝你轻盈地迈入一个又一个春天"

LETTER = """亲爱的薛女士：

生日快乐！

认识你是一件很幸运的事情。这一年里，我们一起……

希望你新的一岁里，每天都开心，想要的都能得到，想去的都能去到。

无论什么时候，需要我的时候，我一直都在。

                                        —— 贾女士
"""

THOUGHTS = [
    ("第一次见面", "还记得我们第一次见面的时候吗？那时候我还不知道，后来会和你变成这么好的朋友。"),
    ("谢谢你", "谢谢你在我不开心的时候陪我聊天，谢谢你总是记得我随口说过的话。"),
    ("关于你的好", "你比你自己以为的要好很多很多。别老是否定自己，你真的特别棒。"),
    ("以后", "以后的每一年生日，我都想陪着你过。这是我们之间的约定。"),
]

IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
PHOTO_ROTATIONS = [-2.2, 1.6, -1.1, 2.0, -1.6, 1.3, -2.0, 2.3]

TIMELINE_XLSX = Path("时间轴照片.xlsx")
TIMELINE_IMG_DIR = Path("photos/timeline")  # 所有图片平铺放在这个文件夹里

# ============================================================
#  👆 配置区结束
# ============================================================

st.set_page_config(
    page_title=f"生日快乐 · {FRIEND_NAME}",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"


# ============================================================
#  🎆 全屏开场烟花
# ============================================================
OPENING_HTML = """<!DOCTYPE html>
<html><head><style>html,body{margin:0;padding:0;overflow:hidden;}</style></head>
<body>
<script>
(function(){
  const parentDoc = window.parent.document;
  const old = parentDoc.getElementById('bday-opening');
  if (old) old.remove();
  const overlay = parentDoc.createElement('div');
  overlay.id = 'bday-opening';
  overlay.style.cssText = 'position:fixed;inset:0;z-index:2147483647;background:radial-gradient(circle at center,#1e1b3a 0%,#0d0a20 100%);display:flex;align-items:center;justify-content:center;opacity:1;transition:opacity 1.1s ease;overflow:hidden';
  const canvas = parentDoc.createElement('canvas');
  canvas.style.cssText = 'width:100%;height:100%;display:block;';
  overlay.appendChild(canvas);
  parentDoc.body.appendChild(overlay);
  const ctx = canvas.getContext('2d');
  let W = parentDoc.documentElement.clientWidth;
  let H = parentDoc.documentElement.clientHeight;
  function resize(){
    const dpr = window.devicePixelRatio || 1;
    W = parentDoc.documentElement.clientWidth;
    H = parentDoc.documentElement.clientHeight;
    canvas.width = W * dpr; canvas.height = H * dpr;
    ctx.setTransform(dpr,0,0,dpr,0,0);
  }
  resize(); window.addEventListener('resize', resize);
  function getTextPoints(text){
    const off = parentDoc.createElement('canvas');
    off.width = W; off.height = H;
    const octx = off.getContext('2d');
    const fontSize = Math.min(W*0.26, H*0.42);
    octx.fillStyle = '#fff';
    octx.font = '900 ' + fontSize + "px 'ZCOOL KuaiLe','PingFang SC','Microsoft YaHei',sans-serif";
    octx.textAlign = 'center'; octx.textBaseline = 'middle';
    octx.fillText(text, W/2, H/2);
    const data = octx.getImageData(0,0,W,H).data;
    const pts = [];
    const gap = 3;
    for (let y=0; y<H; y+=gap){
      for (let x=0; x<W; x+=gap){
        if (data[(y*W+x)*4+3] > 128) pts.push({x,y});
      }
    }
    const maxPts = 1100;
    if (pts.length > maxPts){
      const step = pts.length/maxPts;
      const out = [];
      for (let i=0;i<pts.length;i+=step) out.push(pts[Math.floor(i)]);
      return out;
    }
    return pts;
  }
  const particles = [];
  const textParticles = [];
  const gravity = 0.045;
  const friction = 0.982;
  const rnd = (a,b) => a + Math.random()*(b-a);
  function explode(x,y){
    const hue = Math.random()*360;
    const count = 80 + Math.floor(Math.random()*60);
    const power = rnd(3.2,6.8);
    for (let i=0;i<count;i++){
      const a = Math.random()*Math.PI*2;
      const s = power*Math.pow(Math.random(),0.55);
      particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:1,decay:rnd(0.008,0.02),hue:hue+rnd(-30,30),size:rnd(1.4,2.8)});
    }
  }
  const startTs = performance.now();
  let textSpawned = false, fadeStarted = false, lastBurst = 0;
  function loop(now){
    const t = (now - startTs)/1000;
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = 'rgba(13,10,32,0.20)';
    ctx.fillRect(0,0,W,H);
    ctx.globalCompositeOperation = 'lighter';
    if (t < 1.6 && (!lastBurst || now - lastBurst > 320)){
      explode(rnd(W*0.25, W*0.75), rnd(H*0.25, H*0.45));
      lastBurst = now;
    }
    if (!textSpawned && t >= 0.9){
      textSpawned = true;
      const pts = getTextPoints('20岁');
      for (const p of pts){
        const angle = Math.random()*Math.PI*2;
        const dist = rnd(0,120);
        textParticles.push({x:W/2+Math.cos(angle)*dist,y:H/2+Math.sin(angle)*dist,vx:Math.cos(angle)*rnd(2,6),vy:Math.sin(angle)*rnd(2,6),tx:p.x,ty:p.y,hue:rnd(180,340),size:rnd(1.6,2.6)});
      }
    }
    for (const p of textParticles){
      p.vx += (p.tx - p.x)*0.045;
      p.vy += (p.ty - p.y)*0.045;
      p.vx *= 0.90; p.vy *= 0.90;
      p.x += p.vx; p.y += p.vy;
      const flicker = 0.85 + Math.random()*0.15;
      ctx.beginPath();
      ctx.fillStyle = 'hsla(' + p.hue + ',100%,75%,' + (0.9*flicker) + ')';
      ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
      ctx.fill();
    }
    if (t > 2.2 && t < 4.8 && now - lastBurst > 600){
      explode(rnd(W*0.15, W*0.85), rnd(H*0.15, H*0.35));
      lastBurst = now;
    }
    for (let i=particles.length-1;i>=0;i--){
      const p = particles[i];
      p.vx *= friction;
      p.vy = p.vy*friction + gravity;
      p.x += p.vx; p.y += p.vy;
      p.life -= p.decay;
      if (p.life <= 0 || p.y > H+40){ particles.splice(i,1); continue; }
      ctx.beginPath();
      ctx.fillStyle = 'hsla(' + p.hue + ',100%,' + (55+p.life*25) + '%,' + p.life + ')';
      ctx.arc(p.x, p.y, Math.max(p.size*p.life, 0.5), 0, Math.PI*2);
      ctx.fill();
    }
    if (!fadeStarted && t >= 5.2){
      fadeStarted = true;
      overlay.style.opacity = '0';
      setTimeout(function(){ if (overlay && overlay.parentNode) overlay.remove(); }, 1300);
    }
    if (fadeStarted && t >= 7.0){
      if (overlay && overlay.parentNode) overlay.remove();
      return;
    }
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
})();
</script>
</body></html>"""

if "opening_played" not in st.session_state:
    st.session_state.opening_played = False
if not st.session_state.opening_played:
    components.html(OPENING_HTML, height=0)
    st.session_state.opening_played = True


# ============================================================
#  🎨 全局样式
# ============================================================
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Patrick+Hand&family=Ma+Shan+Zheng&family=ZCOOL+KuaiLe&display=swap');

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
.block-container { max-width: 1100px !important; padding-top: 1rem !important; }

/* 顶部导航 */
.nav-row { display:flex; justify-content:center; gap:14px; margin:0 0 26px 0; flex-wrap:wrap; }
.stButton > button {
    font-family: 'Patrick Hand','Ma Shan Zheng',cursive !important;
    font-size: 1.08rem !important;
    background: #ffffff !important;
    color: #2d2d2d !important;
    border: 2.5px solid #2d2d2d !important;
    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px !important;
    box-shadow: 4px 4px 0px 0px #2d2d2d !important;
    padding: 10px 18px !important;
    transition: all 0.1s ease !important;
    min-height: 46px;
}
.stButton > button:hover {
    background: #e8f4fb !important;
    transform: translate(2px,2px) rotate(-1deg) !important;
    box-shadow: 2px 2px 0px 0px #2d2d2d !important;
}
.stButton > button:active {
    background: #4ea8de !important;
    color: #fff !important;
    transform: translate(4px,4px) !important;
    box-shadow: 0 0 0 0 #2d2d2d !important;
}
.stButton > button[kind="primary"] {
    background: #4ea8de !important;
    color: #fff !important;
    box-shadow: 2px 2px 0px 0px #2d2d2d !important;
}

/* Hero */
.hero { text-align:center; padding:24px 0 10px; }
.hero-title {
    font-family: 'ZCOOL KuaiLe','Ma Shan Zheng',cursive !important;
    font-size: clamp(2.6rem,6.4vw,4.6rem) !important;
    font-weight: 700 !important;
    margin: 0; display: inline-block;
    transform: rotate(-1.5deg);
    line-height: 1.25;
    color: #4ea8de !important;
}
.hero-title .name, .hero-title .accent { color:#4ea8de !important; }
.hero-underline { width:82%; max-width:440px; margin:-4px auto 0; display:block; }
.hero-sub {
    font-family: 'Patrick Hand','Ma Shan Zheng',cursive !important;
    font-size: 1.25rem;
    color: #2d2d2d;
    margin-top:14px;
    transform: rotate(0.4deg);
    display: inline-block;
    padding: 3px 16px;
    border-bottom: 2px dashed #4ea8de;
}

/* Section Title */
.section-title {
    text-align:center;
    font-family: 'Kalam','Ma Shan Zheng',cursive !important;
    font-size: 1.7rem; font-weight: 700;
    color: #2d2d2d;
    margin: 14px 0 20px;
    display: block;
}
.section-title .marker { color:#4ea8de; }

/* 信件 */
.letter-wrap { display:flex; justify-content:center; padding:10px 0 20px; }
.letter-card {
    position: relative;
    background: #ffffff;
    border: 3px solid #2d2d2d;
    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px;
    padding: 48px 52px 40px;
    box-shadow: 6px 6px 0px 0px #2d2d2d;
    transform: rotate(-0.6deg);
    font-family: 'Kalam','Ma Shan Zheng',cursive !important;
    font-size: 1.16rem;
    line-height: 2.15;
    color: #2d2d2d;
    white-space: pre-wrap;
    max-width: 720px;
    width: 100%;
    animation: fadeUp 0.6s ease both;
}
.letter-card::before {
    content: ''; position: absolute;
    top: -16px; left: 50%;
    transform: translateX(-50%) rotate(-2deg);
    width: 130px; height: 30px;
    background: rgba(229,224,216,0.9);
    border: 1px dashed rgba(45,45,45,0.25);
    box-shadow: 0 1px 2px rgba(0,0,0,0.06);
}
@keyframes fadeUp {
    from { opacity:0; transform: rotate(-0.6deg) translateY(24px); }
    to   { opacity:1; transform: rotate(-0.6deg) translateY(0); }
}
.envelope-hint {
    font-family: 'Patrick Hand','Ma Shan Zheng',cursive !important;
    font-size: 1.15rem;
    color: #4ea8de;
    transform: rotate(-1deg);
    display: inline-block;
    padding: 6px 0;
}

/* 时间轴：Step 卡片导航 */
.step-nav {
    display: flex; flex-wrap: wrap;
    gap: 16px; justify-content: center;
    margin: 14px 0 34px;
    padding: 0 12px;
}
.step-nav-card {
    display: inline-flex; flex-direction: column; align-items: flex-start;
    background: #ffffff;
    border: 2.5px solid #2d2d2d;
    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px;
    box-shadow: 4px 4px 0px 0px #2d2d2d;
    padding: 12px 22px 14px;
    text-decoration: none !important;
    color: #2d2d2d !important;
    transition: all 0.12s ease;
    transform: rotate(-0.6deg);
    max-width: 320px;
    cursor: pointer;
}
.step-nav-card:nth-child(even) {
    transform: rotate(0.9deg);
    border-radius: 15px 225px 15px 255px / 255px 15px 225px 15px;
}
.step-nav-card:hover {
    background: #e8f4fb;
    transform: translate(2px,2px) rotate(-1deg) !important;
    box-shadow: 2px 2px 0px 0px #2d2d2d;
    color: #2d2d2d !important;
    text-decoration: none !important;
}
.step-nav-num {
    font-family: 'Kalam','Ma Shan Zheng',cursive !important;
    font-size: 0.95rem; font-weight: 700;
    color: #4ea8de;
    letter-spacing: 1px;
    margin-bottom: 4px;
}
.step-nav-title {
    font-family: 'Patrick Hand','Ma Shan Zheng',cursive !important;
    font-size: 1.02rem;
    line-height: 1.5;
    color: #2d2d2d;
}

/* 时间轴：Step 区块 */
.step-anchor { display: block; height: 1px; scroll-margin-top: 24px; }
.step-block {
    position: relative;
    background: #ffffff;
    border: 3px solid #2d2d2d;
    border-radius: 35px 18px 30px 20px / 20px 30px 15px 25px;
    box-shadow: 6px 6px 0px 0px #2d2d2d;
    padding: 36px 32px 30px;
    margin: 0 0 44px 0;
    transform: rotate(-0.2deg);
}
.step-block::before {
    content: ''; position: absolute;
    top: -14px; left: 50%;
    transform: translateX(-50%) rotate(-2deg);
    width: 130px; height: 28px;
    background: rgba(229,224,216,0.92);
    border: 1px dashed rgba(45,45,45,0.28);
    box-shadow: 0 1px 2px rgba(0,0,0,0.06);
}
.step-block-title {
    font-family: 'Kalam','Ma Shan Zheng',cursive !important;
    font-size: 1.55rem;
    font-weight: 700;
    color: #4ea8de;
    margin: 0 0 18px 0;
    display: inline-block;
    border-bottom: 2px dashed rgba(45,45,45,0.28);
    padding-bottom: 6px;
    transform: rotate(-0.5deg);
}

/* 时间轴：行区块 */
.row-block {
    background: #fefdf9;
    border: 2px dashed #2d2d2d;
    border-radius: 18px 225px 20px 255px / 255px 20px 225px 18px;
    padding: 22px 24px 18px;
    margin-bottom: 22px;
    transform: rotate(-0.15deg);
}
.row-block:nth-child(even) {
    border-radius: 225px 18px 255px 20px / 20px 255px 18px 225px;
    transform: rotate(0.15deg);
}
.row-block:last-child { margin-bottom: 0; }
.row-text {
    font-family: 'Patrick Hand','Ma Shan Zheng',cursive !important;
    font-size: 1.1rem;
    line-height: 1.95;
    color: #2d2d2d;
    margin-bottom: 16px;
    white-space: pre-wrap;
}
.row-img-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}
.row-img {
    background: #ffffff;
    padding: 8px;
    border: 2px solid #2d2d2d;
    box-shadow: 4px 4px 0px 0px #2d2d2d;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    transform: rotate(-1deg);
}
.row-img:nth-child(even) { transform: rotate(1.2deg); }
.row-img:hover {
    transform: rotate(0deg) scale(1.04);
    box-shadow: 6px 6px 0px 0px #2d2d2d;
    z-index: 2;
}
.row-img img {
    width: 100%;
    height: 160px;
    object-fit: cover;
    display: block;
    border: 1px solid #2d2d2d;
    background: #e5e0d8;
}

/* 心里话便签 */
.thought-grid {
    display: grid; grid-template-columns: 1fr;
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
    font-family: 'Patrick Hand','Ma Shan Zheng',cursive !important;
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
    transform: rotate(0deg) translate(-2px,-2px);
    box-shadow: 6px 6px 0px 0px #2d2d2d;
    z-index: 2;
}
.thought-card::before {
    content: ''; position: absolute;
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
    font-family: 'Kalam','Ma Shan Zheng',cursive !important;
    font-size: 1.3rem;
    font-weight: 700;
    color: #4ea8de;
    margin-bottom: 8px;
    display: inline-block;
    border-bottom: 2px dashed rgba(45,45,45,0.25);
    padding-bottom: 2px;
}
.thought-card:nth-child(even) .thought-title { color:#2d5da1; }

/* iframe / Footer */
iframe { border: none !important; }
.footer-note {
    text-align: center;
    font-family: 'Kalam','Ma Shan Zheng',cursive !important;
    font-size: 1.14rem;
    color: #2d2d2d;
    padding: 46px 0 70px;
    transform: rotate(-0.5deg);
    letter-spacing: 1px;
}
.footer-note span { border-bottom: 2px dashed #4ea8de; padding-bottom: 2px; }

/* 响应式 */
@media (max-width: 1000px) { .row-img-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) {
    .letter-card { padding: 32px 24px 28px; font-size: 1.08rem; }
    .thought-card { padding: 22px 20px; font-size: 1.03rem; }
    .hero-sub { font-size: 1.1rem; }
    .nav-row { gap: 8px; }
    .row-img-grid { grid-template-columns: repeat(2, 1fr); }
    .step-block { padding: 28px 20px 22px; }
    .row-block { padding: 18px 16px 14px; }
    .row-img img { height: 130px; }
}
@media (max-width: 450px) { .row-img-grid { grid-template-columns: 1fr; } }
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ============================================================
#  🎇 首页画框烟花
# ============================================================
FIREWORKS_HTML = """<!DOCTYPE html>
<html><head><style>
html, body { margin:0; padding:0; overflow:hidden; background:transparent; }
.frame {
    position: relative; width: calc(100% - 26px); height: calc(100% - 26px);
    margin: 13px;
    background: linear-gradient(180deg, #1e1b3a 0%, #0d0a20 100%);
    border: 3px solid #2d2d2d;
    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px;
    box-shadow: 6px 6px 0px 0px #2d2d2d;
    overflow: hidden; transform: rotate(-0.4deg);
}
.frame::before {
    content: ''; position: absolute; top: -16px; left: 50%;
    transform: translateX(-50%) rotate(-2deg);
    width: 140px; height: 30px;
    background: rgba(229,224,216,0.92);
    border: 1px dashed rgba(45,45,45,0.28);
    z-index: 10;
}
canvas { display:block; width:100%; height:100%; cursor:crosshair; }
</style></head>
<body><div class="frame"><canvas id="fw"></canvas></div>
<script>
const canvas = document.getElementById('fw');
const ctx = canvas.getContext('2d');
let W = 1, H = 1;
function resize(){
  const dpr = window.devicePixelRatio || 1;
  W = canvas.clientWidth || 1; H = canvas.clientHeight || 1;
  canvas.width = W*dpr; canvas.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
}
const particles = [];
const gravity = 0.035, friction = 0.985;
const rnd = (a,b) => a + Math.random()*(b-a);
function explode(x,y){
  const hue = Math.random()*360;
  const count = 70 + Math.floor(Math.random()*50);
  const power = rnd(2.2,5.2);
  for (let i=0;i<count;i++){
    const angle = Math.random()*Math.PI*2;
    const speed = power*Math.pow(Math.random(),0.6);
    particles.push({x,y,vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed,life:1,decay:rnd(0.007,0.018),hue:hue+rnd(-25,25),size:rnd(1.2,2.6)});
  }
  for (let i=0;i<14;i++){
    const angle = Math.random()*Math.PI*2;
    particles.push({x,y,vx:Math.cos(angle)*rnd(0.5,2),vy:Math.sin(angle)*rnd(0.5,2),life:1,decay:0.05,hue:hue,size:2.2});
  }
}
function launch(){ explode(rnd(W*0.12,W*0.88), rnd(H*0.15,H*0.62)); }
function loop(){
  ctx.globalCompositeOperation = 'source-over';
  ctx.fillStyle = 'rgba(13,10,32,0.16)';
  ctx.fillRect(0,0,W,H);
  ctx.globalCompositeOperation = 'lighter';
  for (let i=particles.length-1;i>=0;i--){
    const p = particles[i];
    p.vx *= friction; p.vy = p.vy*friction + gravity;
    p.x += p.vx; p.y += p.vy; p.life -= p.decay;
    if (p.life <= 0 || p.y > H+30){ particles.splice(i,1); continue; }
    ctx.beginPath();
    ctx.fillStyle = 'hsla(' + p.hue + ',100%,' + (55+p.life*20) + '%,' + p.life + ')';
    ctx.arc(p.x, p.y, Math.max(p.size*p.life,0.4), 0, Math.PI*2);
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
</script></body></html>"""


# ============================================================
#  🛠 工具函数
# ============================================================
def _safe_str(v):
    if v is None:
        return ""
    try:
        if pd.isna(v):
            return ""
    except Exception:
        pass
    return str(v).strip()


def load_timeline_steps():
    """
    返回：
    [
      {
        "title": "Step1：...",
        "rows": [
          {"text": "第1行文字", "images": [Path, Path]},
          {"text": "第2行文字", "images": [Path, Path]},
        ],
        "index": 0
      },
      ...
    ]
    """
    steps = []
    if not TIMELINE_XLSX.exists():
        return steps

    try:
        df = pd.read_excel(TIMELINE_XLSX, header=None, engine="openpyxl")
    except Exception:
        return steps

    # 1. 读取 Excel 中的标题和文字
    current_step = None
    for _, row in df.iterrows():
        cells = list(row)
        col_a = _safe_str(cells[0]) if len(cells) > 0 else ""
        col_b = _safe_str(cells[1]) if len(cells) > 1 else ""

        if col_a:
            current_step = {
                "title": col_a,
                "rows": [],
                "index": len(steps),
            }
            steps.append(current_step)

        if col_b and current_step is not None:
            current_step["rows"].append({"text": col_b, "images": []})

    # 2. 遍历 photos/timeline 下的所有图片，根据文件名分类
    if not TIMELINE_IMG_DIR.exists():
        return steps

    all_imgs = [p for p in TIMELINE_IMG_DIR.iterdir() if p.suffix.lower() in IMG_EXTS]
    
    # 使用字典按 (step_idx, row_idx) 暂存图片和排序序号
    img_buckets = {}

    for p in all_imgs:
        # 匹配 step1-1-1 或 Step1-1-1
        m = re.match(r'^step(\d+)-(\d+)-(\d+)', p.stem, re.IGNORECASE)
        if m:
            s_idx = int(m.group(1)) - 1  # Step 序号 (0-based)
            r_idx = int(m.group(2)) - 1  # 行号 (0-based)
            img_seq = int(m.group(3))    # 行内图片序号
            img_buckets.setdefault((s_idx, r_idx), []).append((img_seq, p))
        else:
            # 不符合命名规则的图片直接忽略，或者你也可以让它默认排在某处
            pass

    # 3. 将图片装入对应的数据结构
    for s_idx, s in enumerate(steps):
        for r_idx, r in enumerate(s["rows"]):
            key = (s_idx, r_idx)
            if key in img_buckets:
                items = img_buckets[key]
                items.sort(key=lambda x: x[0])  # 按序号排序
                r["images"].extend([p for _, p in items])

    return steps


def img_to_html(path, rotation):
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
    except Exception:
        return ""
    suffix = path.suffix.lower().lstrip(".")
    if suffix == "jpg":
        suffix = "jpeg"
    return (
        f'<div class="row-img" style="transform: rotate({rotation}deg);">'
        f'<img src="data:image/{suffix};base64,{data}" alt="" />'
        f'</div>'
    )


SCROLL_JS = """
<!DOCTYPE html><html><body><script>
(function(){
  const parentDoc = window.parent.document;
  function bind(){
    parentDoc.querySelectorAll('.step-nav-card').forEach(function(card){
      if (card.dataset.bound) return;
      card.dataset.bound = '1';
      card.onclick = function(e){
        e.preventDefault();
        const id = this.getAttribute('href').slice(1);
        const target = parentDoc.getElementById(id);
        if (target) target.scrollIntoView({behavior:'smooth', block:'start'});
      };
    });
  }
  const obs = new MutationObserver(bind);
  obs.observe(parentDoc.body, {childList:true, subtree:true});
  bind();
})();
</script></body></html>"""


# ============================================================
#  🧭 顶部导航
# ============================================================
NAV_ITEMS = [
    ("home", "🏠 首页"),
    ("letter", "✉️ 写给你的信"),
    ("timeline", "📸 时间轴"),
    ("thoughts", "💭 一些心里话"),
]
st.markdown('<div class="nav-row">', unsafe_allow_html=True)
cols = st.columns(len(NAV_ITEMS))
for i, (key, label) in enumerate(NAV_ITEMS):
    with cols[i]:
        is_active = (st.session_state.current_page == key)
        if st.button(label, key=f"nav_{key}", use_container_width=True, type="primary" if is_active else "secondary"):
            if st.session_state.current_page != key:
                st.session_state.current_page = key
                st.rerun()
st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
#  🏠 首页
# ============================================================
if st.session_state.current_page == "home":
    st.markdown(f'''
    <div class="hero">
        <h1 class="hero-title">
            <span class="name">{html.escape(FRIEND_NAME)}</span>，<span class="accent">生日快乐</span>
            <span style="display:inline-block;transform:rotate(-14deg);">🎉</span>
        </h1>
        <svg class="hero-underline" viewBox="0 0 420 14" preserveAspectRatio="none">
            <path d="M2,8 Q22,2 42,8 T82,8 T122,8 T162,8 T202,8 T242,8 T282,8 T322,8 T362,8 T402,8"
                  stroke="#4ea8de" stroke-width="3" fill="none" stroke-linecap="round"/>
        </svg>
        <div><span class="hero-sub">{html.escape(SUB_TITLE)} ✨</span></div>
    </div>
    ''', unsafe_allow_html=True)
    components.html(FIREWORKS_HTML, height=440, scrolling=False)


# ============================================================
#  ✉️ 信件页
# ============================================================
elif st.session_state.current_page == "letter":
    st.markdown('<div class="section-title">一封<span class="marker">手写</span>的信</div>', unsafe_allow_html=True)
    if "letter_opened" not in st.session_state:
        st.session_state.letter_opened = False
    if not st.session_state.letter_opened:
        st.markdown('<div style="text-align:center;"><span class="envelope-hint">点击下面的按钮，拆开这封信 ✉️</span></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("✉️  拆开这封信", use_container_width=True):
                st.session_state.letter_opened = True
                st.rerun()
    else:
        st.markdown(f'<div class="letter-wrap"><div class="letter-card">{html.escape(LETTER)}</div></div>', unsafe_allow_html=True)


# ============================================================
#  📸 时间轴页
# ============================================================
elif st.session_state.current_page == "timeline":
    st.markdown('<div class="section-title">我们的<span class="marker">回忆</span></div>', unsafe_allow_html=True)

    steps = load_timeline_steps()

    if steps:
        # Step 卡片导航
        nav_html = '<div class="step-nav">'
        for i, s in enumerate(steps):
            nav_html += (
                f'<a href="#step-{i}" class="step-nav-card">'
                f'<span class="step-nav-num">Step {i + 1}</span>'
                f'<span class="step-nav-title">{html.escape(s["title"])}</span>'
                f'</a>'
            )
        nav_html += '</div>'
        st.markdown(nav_html, unsafe_allow_html=True)

        # 每个 Step 的内容区块
        for i, s in enumerate(steps):
            rows_html = ""
            for j, row in enumerate(s["rows"]):
                text_html = html.escape(row["text"]).replace("\n", "<br>")
                if row["images"]:
                    imgs_parts = []
                    for k, p in enumerate(row["images"]):
                        rot = PHOTO_ROTATIONS[k % len(PHOTO_ROTATIONS)]
                        imgs_parts.append(img_to_html(p, rot))
                    imgs_html = f'<div class="row-img-grid">{"".join(imgs_parts)}</div>'
                else:
                    imgs_html = ""
                rows_html += (
                    f'<div class="row-block">'
                    f'<div class="row-text">{text_html}</div>'
                    f'{imgs_html}'
                    f'</div>'
                )

            st.markdown(
                f'<div id="step-{i}" class="step-anchor"></div>'
                f'<div class="step-block">'
                f'<div class="step-block-title">{html.escape(s["title"])}</div>'
                f'{rows_html}'
                f'</div>',
                unsafe_allow_html=True,
            )

        components.html(SCROLL_JS, height=0)

    else:
        st.markdown(
            '<div style="text-align:center;color:#888;padding:40px 0;">'
            '（时间轴还没加载出来，请检查 时间轴照片.xlsx 是否在根目录）'
            '</div>',
            unsafe_allow_html=True,
        )


# ============================================================
#  💭 心里话页
# ============================================================
elif st.session_state.current_page == "thoughts":
    st.markdown('<div class="section-title">一些<span class="marker">心里话</span></div>', unsafe_allow_html=True)
    parts = []
    for title, body in THOUGHTS:
        parts.append(
            f'<div class="thought-card">'
            f'<div class="thought-title">{html.escape(title)}</div>'
            f'<div>{html.escape(body)}</div>'
            f'</div>'
        )
    st.markdown(f'<div class="thought-grid">{"".join(parts)}</div>', unsafe_allow_html=True)


# ============================================================
#  🎁 Footer
# ============================================================
st.markdown(
    f'<div class="footer-note">—— <span>来自 {html.escape(SENDER_NAME)} 的一点小心意</span> 🎁</div>',
    unsafe_allow_html=True,
)
