import streamlit as st
import random
import json
from streamlit_js_eval import streamlit_js_eval, get_geolocation

st.set_page_config(page_title="Zwicky Box Generator", layout="centered")

st.title("🧊 Zwicky Box Generator")
st.markdown("Define your problem dimensions and generate random combinations.")

# Load or initialize dimensions
saved_data = streamlit_js_eval(js_expressions="localStorage.getItem('zwickyBoxData')", key="load_data")
if saved_data:
    try:
        dimensions = json.loads(saved_data)
    except:
        dimensions = {}
else:
    dimensions = {}

st.subheader("Define Dimensions")

# Add new dimension
with st.form("add_dimension"):
    col1, col2 = st.columns([2, 3])
    with col1:
        new_dim = st.text_input("New Column Name")
    with col2:
        new_vals = st.text_input("Values (comma-separated)")
    submitted = st.form_submit_button("Add")
    if submitted and new_dim and new_vals:
        dimensions[new_dim] = [v.strip() for v in new_vals.split(",") if v.strip()]
        streamlit_js_eval(js_expressions=f"localStorage.setItem('zwickyBoxData', '{json.dumps(dimensions)}')", key="save_data")

# Show current dimensions
if dimensions:
    for col, vals in dimensions.items():
        st.write(f"**{col}**: {', '.join(vals)}")

    if st.button("🎲 Generate Combination"):
        result = {col: random.choice(vals) for col, vals in dimensions.items()}
        st.success("Here’s a generated combination:")
        st.json(result)
else:
    st.info("No dimensions defined yet.")

# Reset option
if st.button("🧹 Clear All"):
    dimensions.clear()
    streamlit_js_eval(js_expressions="localStorage.removeItem('zwickyBoxData')", key="clear_data")
    st.experimental_rerun()