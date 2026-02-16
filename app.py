import streamlit as st
import streamlit.components.v1 as components
import re
import json

# --- KONFIGURÁCIÓ ---
st.set_page_config(page_title="Pro-Súgógép v2.2", layout="wide")

# --- JELSZÓVÉDELEM ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if not st.session_state.auth:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.title("🔐 Belépés")
            pwd = st.text_input("Jelszó", type="password")
            # Megjegyzés: A 'password' kulcsot a Streamlit Cloud Secrets-ben kell beállítani
            if st.button("Belépés"):
                if pwd == st.secrets.get("password", "admin123"):
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Hibás jelszó!")
        st.stop()

check_password()

# --- OLDALSÁV ---
st.sidebar.header("⚙️ Beállítások")
nyers_szoveg = st.sidebar.text_area("Szöveg beillesztése", "Ide másolja a szöveget...", height=200)

szavak = re.findall(r'\S+', nyers_szoveg)
szavak_json = json.dumps(szavak)

wpm = st.sidebar.slider("Sebesség (Szó/Perc)", 10, 600, 180)
betumeret = st.sidebar.slider("Betűméret (px)", 20, 250, 80)
sorkoz = st.sidebar.slider("Sorköz", 1.0, 3.0, 1.2, 0.1)

szoveg_szin = st.sidebar.color_picker("Betűszín", "#FFFFFF")
hatter_szin = st.sidebar.color_picker("Háttérszín", "#000000")
egy_szo_mod = st.sidebar.toggle("Egy szó mód (Villogó)", value=False)

# --- TELEPROMPTER ENGINE ---
# A dupla kapcsos zárójelek {{ }} szükségesek a f-string miatt!
html_kod = f"""
<div id="wrapper" style="
    background-color: {hatter_szin}; 
    border: 1px solid #444;
    border-radius: 15px; 
    position: relative; 
    overflow: hidden; 
    height: 75vh; 
    width: 90%;
    margin: 0 auto;
    box-sizing: border-box;">
    
    <button onclick="openFullscreen();" style="position: absolute; right: 15px; top: 15px; z-index: 100; cursor: pointer; padding: 5px 12px; background: rgba(128,128,128,0.3); color: white; border: 1px solid rgba(255,255,255,0.3); border-radius: 5px;">📺 Teljes képernyő</button>
    
    <div id="container" style="
        height: 100%; 
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow-y: hidden;
        cursor: pointer;
        padding: 0 10%; 
        box-sizing: border-box;">
        
        <div id="content" style="
            color: {szoveg_szin}; 
            font-size: {betumeret}px; 
            line-height: {sorkoz}; 
            font-family: Arial, sans-serif; 
            text-align: center;
            white-space: pre-wrap;
            width: 100%;">
            {"Kattints a kezdéshez..." if egy_szo_mod else nyers_szoveg}
        </div>
    </div>
</div>

<script>
    var container = document.getElementById('container');
    var content = document.getElementById('content');
    var isRsvp = {str(egy_szo_mod).lower()};
    var words = {szavak_json};
    var wpm = {wpm};
    
    var scrolling = false;
    var currentIndex = 0;
    var lastUpdate = 0;
    var startTime = 0;

    function update(timestamp) {{
        if (!scrolling) return;

        if (isRsvp) {{
            var interval = 60000 / wpm;
            if (timestamp - lastUpdate > interval) {{
                if (currentIndex < words.length) {{
                    content.innerText = words[currentIndex];
                    currentIndex++;
                    lastUpdate = timestamp;
                }} else {{
                    scrolling = false;
                    currentIndex = 0;
                }}
            }}
        }} else {{
            if (!startTime) startTime = timestamp;
            var totalTime = (words.length / wpm) * 60 * 1000;
            var elapsed = timestamp - startTime;
            var progress = elapsed / totalTime;
            
            var maxScroll = content.scrollHeight + container.offsetHeight;
            container.scrollTop = progress * maxScroll;
            
            if (progress >= 1.2) scrolling = false;
        }}
        
        if (scrolling) requestAnimationFrame(update);
    }}

    container.onclick = function() {{
        if (!scrolling) {{
            scrolling = true;
            if (isRsvp && currentIndex >= words.length) currentIndex = 0;
            if (!isRsvp) {{
                // Onnan folytatja, ahol a görgetés áll
                var totalTime = (words.length / wpm) * 60 * 1000;
                var currentProgress = container.scrollTop / (content.scrollHeight + container.offsetHeight);
                startTime = performance.now() - (currentProgress * totalTime);
            }}
            requestAnimationFrame(update);
        }} else {{
            scrolling = false;
        }}
    }};

    function openFullscreen() {{
        var elem = document.getElementById("wrapper");
        if (elem.requestFullscreen) {{ elem.requestFullscreen(); }}
        else if (elem.webkitRequestFullscreen) {{ elem.webkitRequestFullscreen(); }}
        else if (elem.msRequestFullscreen) {{ elem.msRequestFullscreen(); }}
    }}
</script>

<style>
    #container::-webkit-scrollbar {{ display: none; }}
    #container {{ -ms-overflow-style: none; scrollbar-width: none; }}
</style>
"""

components.html(html_kod, height=780)

st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
