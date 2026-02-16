import streamlit as st
import streamlit.components.v1 as components

# --- OLDAL BEÁLLÍTÁSA ---
st.set_page_config(page_title="Pro-Súgógép", layout="wide")

# --- EGYSZERŰ JELSZÓVÉDELEM ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    
    if not st.session_state.auth:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.title("🔐 Belépés")
            pwd = st.text_input("Kérjük, adja meg a jelszót", type="password")
            if st.button("Belépés"):
                if pwd == st.secrets["password"]:
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Hibás jelszó!")
        st.stop()

check_password()

# --- OLDALSÁV (VEZÉRLŐPULT) ---
st.sidebar.header("⚙️ Beállítások")
szoveg = st.sidebar.text_area("Szöveg beillesztése", "Üdvözöljük a magyar nyelvű súgógépben! Kattintson a fekete mezőre a görgetéshez.", height=300)

sebesseg = st.sidebar.slider("Görgetési sebesség", 0, 100, 20, help="0 = megállítva")
betumeret = st.sidebar.slider("Betűméret (px)", 20, 150, 60)
sorkoz = st.sidebar.slider("Sorköz", 1.0, 3.0, 1.5, 0.1)

szoveg_szin = st.sidebar.color_picker("Betűszín", "#FFFFFF")
hatter_szin = st.sidebar.color_picker("Háttérszín", "#000000")

st.sidebar.markdown("---")
st.sidebar.info("Tipp: Használja az F11-et a böngésző teljes képernyőjéhez, vagy kattintson a lenti gombra a mező nagyításához.")

# --- TELEPROMPTER MEGJELENÍTÉS ---
# HTML/JS injektálás a sima görgetéshez és fullscreen funkcióhoz
html_kod = f"""
<div id="wrapper" style="background-color:{hatter_szin}; padding: 20px; border-radius: 15px; position: relative;">
    <button onclick="openFullscreen();" style="position: absolute; right: 20px; top: 20px; z-index: 100; cursor: pointer; padding: 5px 10px;">Full Screen 📺</button>
    
    <div id="container" style="
        background-color:{hatter_szin}; 
        color:{szoveg_szin}; 
        font-size:{betumeret}px; 
        line-height:{sorkoz}; 
        font-family: 'Arial', sans-serif; 
        height:80vh; 
        overflow-y:auto; 
        padding:100px 50px; 
        scroll-behavior: smooth;">
        <div id="content" style="white-space: pre-wrap; padding-bottom: 500px;">{szoveg}</div>
    </div>
</div>

<script>
    var container = document.getElementById('container');
    var speed = {sebesseg};
    var pos = 0;
    var interval;

    function scrollStep() {{
        if (speed > 0) {{
            pos += speed / 50;
            container.scrollTop = pos;
        }}
    }}

    // Indítás/Megállítás kattintásra
    var scrolling = false;
    container.onclick = function() {{
        if (!scrolling) {{
            interval = setInterval(scrollStep, 10);
            scrolling = true;
        }} else {{
            clearInterval(interval);
            scrolling = false;
        }}
    }};

    // Teljes képernyő funkció
    function openFullscreen() {{
        var elem = document.getElementById("wrapper");
        if (elem.requestFullscreen) {{
            elem.requestFullscreen();
        }} else if (elem.webkitRequestFullscreen) {{ /* Safari */
            elem.webkitRequestFullscreen();
        }} else if (elem.msRequestFullscreen) {{ /* IE11 */
            elem.msRequestFullscreen();
        }}
    }}
</script>
"""

st.components.v1.html(html_kod, height=850)

# --- LÁBJEGYZET ---
st.markdown("---")
st
