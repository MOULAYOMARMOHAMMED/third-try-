import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import calculate_z_factor

st.title("📊 Gas Properties Calculator")

# -------------------------
# Sidebar Inputs
# -------------------------
st.sidebar.header("Input Parameters")

temp_f = st.sidebar.number_input("Temperature (°F)", value=200.0)
p_res = st.sidebar.number_input("Reservoir Pressure (psia)", value=3000.0)
gamma = st.sidebar.number_input("Gas Specific Gravity", value=0.7)

run = st.sidebar.button("Calculate")

if run:
    # -------------------------
    # Thermodynamics
    # -------------------------
    t_rankine = temp_f + 459.67

    pc = 756.8 - 131 * gamma - 3.6 * gamma**2
    tc = 169.2 + 349.5 * gamma - 74 * gamma**2

    tpr = t_rankine / tc
    ppr = p_res / pc

    z_res = calculate_z_factor(ppr, tpr, gamma)
    bg_res = 14.695 / 519.7 * z_res * t_rankine / p_res
    exp_res = 1 / bg_res

    # -------------------------
    # Results
    # -------------------------
    st.subheader("Reservoir Results")

    c1, c2, c3 = st.columns(3)
    c1.metric("Z-Factor", f"{z_res:.5f}")
    c2.metric("Bg (ft³/scf)", f"{bg_res:.5f}")
    c3.metric("Expansion Factor", f"{exp_res:.5f}")

    # -------------------------
    # Pressure Range
    # -------------------------
    pressures, z_vals, bg_vals, exp_vals = [], [], [], []

    p = p_res
    while p >= 14.5:
        z = calculate_z_factor(p / pc, tpr, gamma)
        bg = 14.695 / 519.7 * z * t_rankine / p

        pressures.append(p)
        z_vals.append(z)
        bg_vals.append(bg)
        exp_vals.append(1 / bg)

        p -= 14.6

    df = pd.DataFrame({
        "Pressure (psia)": pressures,
        "Z-Factor": z_vals,
        "Bg (ft³/scf)": bg_vals,
        "Expansion Factor": exp_vals
    })

    # -------------------------
    # Pressure Slider
    # -------------------------
    st.subheader("Adjust Pressure")

    p_slider = st.slider(
        "Pressure (psia)",
        min_value=14.5,
        max_value=p_res,
        value=p_res,
        step=1.0
    )

    z_s = calculate_z_factor(p_slider / pc, tpr, gamma)
    bg_s = 14.695 / 519.7 * z_s * t_rankine / p_slider
    exp_s = 1 / bg_s

    # -------------------------
    # Matplotlib Plots
    # -------------------------
    fig, axs = plt.subplots(2, 2, figsize=(14, 12))
    ax1, ax2, ax3, ax4 = axs.flatten()

    ax1.plot(pressures, z_vals, ".-")
    ax1.scatter(p_slider, z_s, color="red")
    ax1.set_title("Z-Factor vs Pressure")
    ax1.grid()

    ax2.plot(pressures, bg_vals, ".-", color="green")
    ax2.scatter(p_slider, bg_s, color="red")
    ax2.set_title("Bg vs Pressure")
    ax2.grid()

    ax3.plot(pressures, exp_vals, ".-", color="purple")
    ax3.scatter(p_slider, exp_s, color="red")
    ax3.set_title("Expansion Factor vs Pressure")
    ax3.grid()

    ax4.axis("off")
    ax4.text(
        0.5, 0.5,
        f"""
INPUT
T = {temp_f} °F
P = {p_slider:.2f} psia
γ = {gamma}

RESULTS
Z = {z_s:.5f}
Bg = {bg_s:.5f}
Exp = {exp_s:.5f}
""",
        ha="center", va="center", fontsize=12
    )

    st.pyplot(fig)

    # -------------------------
    # Export
    # -------------------------
    # st.subheader("Export")
    
    # st.download_button(
    #     "Download Excel",
    #     data=df.to_excel(index=False),
    #     file_name="gas_properties.xlsx"

    # )
