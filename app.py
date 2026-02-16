import streamlit as st
import streamlit.components.v1 as components
import re

# --- KONFIGURÁCIÓ ---
st.set_page_config(page_title="Pro-Súgógép WPM", layout="wide")

# --- JELSZÓVÉDELEM ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if not st.session_state.auth:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.title("🔐 Belépés")
            pwd = st.text_input("Jelszó", type="password")
            if st.button("Belépés") and pwd == st.secrets.get("password", "admin123"):
                st.session_state.auth = True
                st.rerun()
            else: st.stop()

check_password()

# --- OLDALSÁV ---
st.sidebar.header("⚙️ Vezérlőpult")
nyers_szoveg = st.sidebar.text_area("Szöveg", "Ez egy teszt szöveg a súgógéphez.", height=250)

# Szavak számlálása a WPM-hez
szavak_szama = len(re.findall(r'\w+', nyers_szoveg))
st.sidebar.write(f"Szavak száma: **{szavak_szama}**")

wpm = st.sidebar.slider("Sebesség (Szó/Perc - WPM)", 10, 300, 120)
betumeret = st.sidebar.slider("Betűméret (px)", 20, 300, 80)
sorkoz = st.sidebar.slider("Sorköz", 1.0, 5.0, 1.2, 0.1)

# Színbeállítások
szoveg_szin = st.sidebar.color_picker("Betűszín", "#FFFFFF")
hatter_szin = st.sidebar.color_picker("Háttérszín", "#000000")

# "Egy szó" mód segítő (Középre rendezés)
egy_szo_mod = st.sidebar.checkbox("Egy szó/sor mód (Középre igazítás)")

igazitas = "center" if egy_szo_mod else "left"
padding_top = "40vh" if egy_szo_mod else "50px"

# --- TELEPROMPTER ENGINE ---
html_kod = f"""
<div id="wrapper" style="background-color:{hatter_szin}; border-radius: 15px; position: relative; overflow: hidden;">
    <button onclick="openFullscreen();" style="position: absolute; right: 20px; top: 20px; z-index: 100; opacity: 0.5;">📺 Teljes képernyő</button>
    
    <div id="container" style="
        background-color:{hatter_szin}; 
        color:{szoveg_szin}; 
        font-size:{betumeret}px; 
        line-height:{sorkoz}; 
        text-align:{igazitas};
        font-family: 'Arial', sans-serif; 
        height:85vh; 
        overflow-y:scroll; 
        padding-top: {padding_top};
        padding-bottom: 90vh;
        scroll-behavior: linear;
        -ms-overflow-style: none;  scrollbar-width: none;">
        
        <div id="content" style="white-space: pre-wrap;">{nyers_szoveg}</div>
    </div>
</div>

<script>
    var container = document.getElementById('container');
    var wpm = {wpm};
    var wordCount = {szavak_szama};
    var scrolling = false;
    var startTime;
    var startPos;

    function scroll() {{
        if (!scrolling) return;
        
        var totalHeight = document.getElementById('content').scrollHeight;
        // Kiszámoljuk a teljes időt ezredmásodpercben (perc -> ms)
        var totalTimeMs = (wordCount / wpm) * 60 * 1000;
        var elapsed = performance.now() - startTime;
        
        var progress = elapsed / totalTimeMs;
        container.scrollTop = startPos + (totalHeight * progress);

        if (container.scrollTop < totalHeight + 500) {{
            requestAnimationFrame(scroll);
        }}
    }}

    container.onclick = function() {{
        if (!scrolling) {{
            scrolling = true;
            startTime = performance.now();
            startPos = container.scrollTop;
            scroll();
        }} else {{
            scrolling = false;
        }}
    }};

    function openFullscreen() {{
        var elem = document.getElementById("wrapper");
        if (elem.requestFullscreen) {{ elem.requestFullscreen(); }}
        else if (elem.webkitRequestFullscreen) {{ elem.webkitRequestFullscreen(); }}
    }}
</script>
<style>
    #container::-webkit-scrollbar {{ display: none; }}
</style>
"""

st.components.v1.html(html_kod, height=900)
