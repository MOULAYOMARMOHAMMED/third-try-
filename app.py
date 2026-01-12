import streamlit as st

st.set_page_config(
    page_title="Gas Properties App",
    layout="wide"
)

st.title("🛢️ Gas Properties Calculator")
st.markdown("""
### Welcome

This application allows you to calculate **gas Z-factor, Bg, and expansion factor**
using the **Hall–Yarborough correlation**.

👉 Use the **sidebar** to navigate between pages.

---

**Features**
- Reservoir-condition calculations  
- Pressure-dependent curves  
- Interactive pressure slider  
- Matplotlib scientific plots  
- Excel & PNG export  

Developed for **petroleum & reservoir engineering applications**.
""")

st.info("Select **Gas Properties Calculator** from the left menu to begin.")
