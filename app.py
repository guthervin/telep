import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Pro-Prompt", layout="wide")

# --- SIMPLE AUTH ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    
    if not st.session_state.auth:
        pwd = st.sidebar.text_input("Enter Password", type="password")
        if pwd == st.secrets["password"]: # We will set this in the cloud settings
            st.session_state.auth = True
            st.rerun()
        else:
            st.stop()

check_password()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Settings")
text_input = st.sidebar.text_area("Paste Script Here", "Welcome to your pro teleprompter...")
speed = st.sidebar.slider("Scroll Speed", 1, 50, 10)
font_size = st.sidebar.slider("Font Size (px)", 20, 100, 50)
text_color = st.sidebar.color_picker("Text Color", "#FFFFFF")
bg_color = st.sidebar.color_picker("Background Color", "#000000")
highlight_color = st.sidebar.color_picker("Highlight Color", "#FFFF00")

# --- TELEPROMPTER ENGINE ---
# We use a bit of Javascript for the smooth scrolling
html_code = f"""
<div id="container" style="background-color:{bg_color}; color:{text_color}; font-size:{font_size}px; font-family:sans-serif; height:80vh; overflow:hidden; padding:50px; border-radius:10px;">
    <div id="content" style="white-space: pre-wrap;">{text_input}</div>
</div>

<script>
    var container = document.getElementById('container');
    var speed = {speed};
    var pos = 0;
    
    function scroll() {{
        pos += speed / 10;
        container.scrollTop = pos;
        if (pos < container.scrollHeight) {{
            requestAnimationFrame(scroll);
        }}
    }}
    
    // Start scrolling on click
    container.onclick = function() {{
        scroll();
    }};
</script>
"""

st.markdown(f"### Teleprompter (Click the black box to start)")
components.html(html_code, height=600)