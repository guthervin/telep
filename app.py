import streamlit as st
import streamlit.components.v1 as components
import re

# --- KONFIGURÁCIÓ ---
st.set_page_config(page_title="Pro-Súgógép v2.0", layout="wide")

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
nyers_szoveg = st.sidebar.text_area("Szöveg", "Illessze be a szöveget ide...", height=200)

# Szöveg feldolgozása (tisztítás a villogó módhoz)
szavak = re.findall(r'\S+', nyers_szoveg)
szavak_szama = len(szavak)
st.sidebar.write(f"Szavak száma: **{szavak_szama}**")

wpm = st.sidebar.slider("Sebesség (Szó/Perc)", 10, 600, 200)
betumeret = st.sidebar.slider("Betűméret (px)", 20, 300, 100)
sorkoz = st.sidebar.slider("Sorköz", 1.0, 3.0, 1.2, 0.1)

szoveg_szin = st.sidebar.color_picker("Betűszín", "#FFFFFF")
hatter_szin = st.sidebar.color_picker("Háttérszín", "#000000")

egy_szo_mod = st.sidebar.toggle("Egy szó mód (Villogó)", value=False)

# --- TELEPROMPTER ENGINE ---
html_kod = f"""
<div id="wrapper" style="
    background-color:{hatter_szin}; 
    border-radius: 15px; 
    position: relative; 
    overflow: hidden; 
    height: 80vh; 
    margin: 0 5%;">
    
    <button onclick="openFullscreen();" style="position: absolute; right: 15px; top: 15px; z-index: 100; cursor: pointer; padding: 8px; opacity: 0.6;">📺 Teljes képernyő</button>
    
    <div id="container" style="
        background-color:{hatter_szin}; 
        color:{szoveg_szin}; 
        font-size:{betumeret}px; 
        line-height:{sorkoz}; 
        font-family: 'Arial', sans-serif; 
        height: 100%; 
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        overflow-y: hidden;
        cursor: pointer;">
        
        <div id="content" style="padding: 0 5%; white-space: pre-wrap;">{nyers_szoveg}</div>
    </div>
</div>

<script>
    var container = document.getElementById('container');
    var content = document.getElementById('content');
    var isRsvp = {str(egy_szo_mod).lower()};
    var words = {szavak};
    var wpm = {wpm};
    var scrolling = False;
    
    var currentIndex = 0;
    var lastUpdate = 0;
    var scrollPos = 0;
    var startTime = 0;

    function update(timestamp) {{
        if (!scrolling) return;

        if (isRsvp) {{
            // --- VILLOGÓ MÓD LOGIKA ---
            var interval = 60000 / wpm;
            if (timestamp - lastUpdate > interval) {{
                if (currentIndex < words.length) {{
                    content.innerText = words[currentIndex];
                    currentIndex++;
                    lastUpdate = timestamp;
                }} else {{
                    scrolling = false;
                }}
            }}
        }} else {{
            // --- GÖRDÜLŐ MÓD LOGIKA ---
            if (!startTime) startTime = timestamp;
            var totalHeight = content.scrollHeight;
            var totalTime = (words.length / wpm) * 60 * 1000;
            var progress = (timestamp - startTime) / totalTime;
            
            container.scrollTop = totalHeight * progress;
        }}
        
        if (scrolling) requestAnimationFrame(update);
    }}

    container.onclick = function() {{
        if (!scrolling) {{
            scrolling = true;
            if (!isRsvp) startTime = performance.now() - (container.scrollTop / content.scrollHeight * ((words.length / wpm) * 60 * 1000));
            requestAnimationFrame(update);
        }} else {{
            scrolling = false;
            startTime = 0;
        }}
    }};

    function openFullscreen() {{
        var elem = document.getElementById("wrapper");
        if (elem.requestFullscreen) {{ elem.requestFullscreen(); }}
        else if (elem.webkitRequestFullscreen) {{ elem.webkitRequestFullscreen(); }}
    }}
</script>
"""

st.components.v1.html(html_kod, height=700)

st.markdown("""
<style>
    .stApp { margin: 0 5%; }
    iframe { border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

st.caption(f"Üzemmód: {'Villogó (RSVP)' if egy_szo_mod else 'Gördülő'} | Margók: 5% fix")
