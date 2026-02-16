import streamlit as st
import streamlit.components.v1 as components
import re
import json

# --- KONFIGURÁCIÓ ---
st.set_page_config(page_title="Pro-Súgógép v2.1", layout="wide")

# --- JELSZÓVÉDELEM ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if not st.session_state.auth:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.title("🔐 Belépés")
            pwd = st.text_input("Jelszó", type="password")
            if st.button("Belépés"):
                # Streamlit Secrets-ből olvassa, vagy alapértelmezett
                correct_pwd = st.secrets.get("password", "admin123")
                if pwd == correct_pwd:
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Hibás jelszó!")
        st.stop()

check_password()

# --- OLDALSÁV ---
st.sidebar.header("⚙️ Beállítások")
nyers_szoveg = st.sidebar.text_area("Szöveg beillesztése", "Ez egy minta szöveg. Próbáld ki a villogó módot is!", height=200)

# Szöveg tisztítása és szavakra bontása
szavak = re.findall(r'\S+', nyers_szoveg)
szavak_json = json.dumps(szavak) # Biztonságos átadás JS-nek

wpm = st.sidebar.slider("Sebesség (Szó/Perc)", 10, 600, 180)
betumeret = st.sidebar.slider("Betűméret (px)", 20, 250, 80)
sorkoz = st.sidebar.slider("Sorköz", 1.0, 3.0, 1.2, 0.1)

szoveg_szin = st.sidebar.color_picker("Betűszín", "#FFFFFF")
hatter_szin = st.sidebar.color_picker("Háttérszín", "#000000")

egy_szo_mod = st.sidebar.toggle("Egy szó mód (Villogó)", value=False)

# --- TELEPROMPTER MEGJELENÍTÉS ---
html_kod = f"""
<div id="wrapper" style="
    background-color: {hatter_szin}; 
    border: 2px solid #444;
    border-radius: 15px; 
    position: relative; 
    overflow: hidden; 
    height: 75vh; 
    width: 90%;
    margin: 0 auto;
    box-sizing: border-box;">
    
    <button onclick="openFullscreen();" style="position: absolute; right: 10px; top: 10px; z-index: 100; cursor: pointer; padding: 5px 10px; background: rgba(255,255,255,0.2); color: white; border: none; border-radius: 5px;">📺 Teljes képernyő</button>
    
    <div id="container" style="
        height: 100%; 
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow-y: hidden;
        cursor: pointer;
        padding: 0 5%; 
        box-sizing: border-box;">
        
        <div id="content" style="
            color: {szoveg_szin}; 
            font-size: {betumeret}px; 
            line-height: {sorkoz}; 
            font-family: Arial, sans-serif; 
            text-align: center;
            white-space: pre-wrap;
            width: 100%;">
            {nyers_szoveg if not egy_szo_mod else "Kattints az indításhoz"}
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
    var scrollPos = 0;

    function update
