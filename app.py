import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import math
import re

st.set_page_config(page_title="StudyLab — Chemistry", page_icon="🧪", layout="wide")

st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 700; text-align: center; margin-bottom: 0.3rem; }
    .sub-title { text-align: center; color: #888; margin-bottom: 2rem; }
    .result-box { background: #1a1a2e; border-radius: 8px; padding: 0.8rem 1rem; margin: 0.5rem 0; border-left: 4px solid #10b981; }
    h2 { border-bottom: 1px solid #333; padding-bottom: 0.3rem; }
    .stApp { background: #0f0f1a; }
    .block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧪 StudyLab — Chemistry</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive chemistry tools</div>', unsafe_allow_html=True)

# ── SIDEBAR: Category → Topic ─────────────────────────────
category = st.sidebar.selectbox("Category", [
    "⚗️ Acids & Bases",
    "🧮 Stoichiometry",
    "💨 Gas Laws",
    "🔬 Periodic Table",
])

topic_map = {
    "⚗️ Acids & Bases": ["pH Calculator"],
    "🧮 Stoichiometry": ["Molar Mass Calculator", "Stoichiometry"],
    "💨 Gas Laws": ["Ideal Gas Law"],
    "🔬 Periodic Table": ["Periodic Trend Explorer"],
}

topic = st.sidebar.radio("Topic", topic_map[category])

# ================================================================
#                         pH CALCULATOR
# ================================================================
if topic == "pH Calculator":
    st.markdown("## pH Calculator")
    st.latex(r"\text{pH} = -\log_{10}[H^+] \quad\quad \text{pOH} = -\log_{10}[OH^-]")
    st.latex(r"\text{pH} + \text{pOH} = 14")

    mode = st.radio("Input mode:", ["[H⁺] concentration", "[OH⁻] concentration", "pH value"], horizontal=True)

    if mode == "[H⁺] concentration":
        h_conc = st.number_input("[H⁺] (mol/L)", 1e-14, 1.0, 1e-7, format="%.2e")
        ph = -math.log10(h_conc)
        poh = 14.0 - ph
        oh = 10.0 ** -poh
    elif mode == "[OH⁻] concentration":
        oh_conc = st.number_input("[OH⁻] (mol/L)", 1e-14, 1.0, 1e-7, format="%.2e")
        poh = -math.log10(oh_conc)
        ph = 14.0 - poh
        h_conc = 10.0 ** -ph
        oh = oh_conc
    else:
        ph = st.number_input("pH", 0.0, 14.0, 7.0, 0.01)
        h_conc = 10.0 ** -ph
        poh = 14.0 - ph
        oh = 10.0 ** -poh

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("[H⁺]", f"{h_conc:.2e} mol/L")
    with col2: st.metric("pH", f"{ph:.2f}")
    with col3: st.metric("pOH", f"{poh:.2f}")

    col4, col5 = st.columns(2)
    with col4: st.metric("[OH⁻]", f"{oh:.2e} mol/L")

    if ph < 3:
        label, color = "Strong acid", "#ef4444"
    elif ph < 7:
        label, color = "Acid", "#f59e0b"
    elif ph == 7:
        label, color = "Neutral", "#10b981"
    elif ph < 11:
        label, color = "Base", "#3b82f6"
    else:
        label, color = "Strong base", "#8b5cf6"

    st.markdown(
        f'<div style="background:{color}33; border-left:4px solid {color}; '
        f'padding:0.5rem 1rem; border-radius:6px;">'
        f'<strong>{label}</strong> — pH {ph:.2f}</div>',
        unsafe_allow_html=True,
    )

    fig = go.Figure()
    ph_colorscale = px.colors.sequential.Viridis
    for i in range(14):
        idx = min(int(i / 14 * len(ph_colorscale)), len(ph_colorscale) - 1)
        fig.add_trace(
            go.Scatter(
                x=[i, i + 1], y=[0, 0], mode="lines",
                line=dict(width=24, color=ph_colorscale[idx]),
                hoverinfo="none", showlegend=False,
            )
        )
    fig.add_trace(
        go.Scatter(
            x=[ph], y=[0], mode="markers",
            marker=dict(size=16, color="white", symbol="diamond",
                        line=dict(color="black", width=2)),
            name=f"pH {ph:.2f}",
        )
    )
    fig.update_layout(
        height=90,
        xaxis=dict(range=[0, 14], tickvals=list(range(0, 15)), title="pH"),
        yaxis=dict(visible=False, range=[-0.5, 0.5]),
        margin=dict(l=10, r=10, t=10, b=30),
    )
    st.plotly_chart(fig, use_container_width=True)

# ================================================================
#                     MOLAR MASS CALCULATOR
# ================================================================
elif topic == "Molar Mass Calculator":
    st.markdown("## Molar Mass Calculator")
    elements = {
        "H": 1.008, "He": 4.003, "Li": 6.941, "Be": 9.012, "B": 10.811,
        "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
        "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.086, "P": 30.974,
        "S": 32.065, "Cl": 35.453, "K": 39.098, "Ar": 39.948, "Ca": 40.078,
        "Fe": 55.845, "Cu": 63.546, "Zn": 65.380, "Br": 79.904, "Ag": 107.868,
        "I": 126.904, "Au": 196.967, "Hg": 200.590, "Pb": 207.200,
    }

    formula = st.text_input("Enter chemical formula (e.g. H2O, CO2, H2SO4, C6H12O6)", "H2O").strip()

    parts = re.findall(r"([A-Z][a-z]?)(\d*)", formula)
    total_mass = 0.0
    breakdown = []
    unknown = []
    for el, count in parts:
        if el in elements:
            n = int(count) if count else 1
            mass = elements[el] * n
            total_mass += mass
            breakdown.append(f"{el}{count or ''} = {elements[el]:.3f} × {n} = {mass:.3f}")
        else:
            unknown.append(el)

    if unknown:
        st.error(f"Unknown element(s): {', '.join(unknown)}")
    else:
        st.success(f"**Molar mass of {formula}: {total_mass:.4f} g/mol**")
        with st.expander("Show breakdown"):
            for line in breakdown:
                st.markdown(f"- {line}")

        st.markdown("### Mass ↔ Moles Converter")
        mass_input = st.number_input("Mass (g)", 0.0, 1000.0, 18.0, 0.1)
        moles = mass_input / total_mass if total_mass > 0 else 0
        st.info(f"{mass_input:.2f} g of {formula} = **{moles:.6f} mol**")

# ================================================================
#                       STOICHIOMETRY
# ================================================================
elif topic == "Stoichiometry":
    st.markdown("## Stoichiometry Calculator")
    st.markdown("**Reaction:** aA + bB → cC + dD")
    st.latex(r"\text{Mole ratio: } \frac{n_A}{a} = \frac{n_B}{b} = \frac{n_C}{c} = \frac{n_D}{d}")

    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a: a = st.number_input("Coeff A", 1, 10, 1, key="s_a")
    with col_b: b = st.number_input("Coeff B", 0, 10, 1, key="s_b")
    with col_c: c = st.number_input("Coeff C", 0, 10, 1, key="s_c")
    with col_d: d = st.number_input("Coeff D", 0, 10, 1, key="s_d")

    nA = st.number_input("Moles of A given (mol)", 0.0, 100.0, 2.0, 0.1)

    st.subheader("Results")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Moles of B needed", f"{nA * b / a:.4f} mol" if b > 0 else "N/A")
    with col2: st.metric("Moles of C produced", f"{nA * c / a:.4f} mol" if c > 0 else "N/A")
    with col3: st.metric("Moles of D produced", f"{nA * d / a:.4f} mol" if d > 0 else "N/A")

# ================================================================
#                        IDEAL GAS LAW
# ================================================================
elif topic == "Ideal Gas Law":
    st.markdown("## Ideal Gas Law")
    st.latex(r"PV = nRT")

    P = st.slider("Pressure P (atm)", 0.1, 100.0, 1.0, 0.1)
    n = st.slider("Amount n (mol)", 0.1, 10.0, 1.0, 0.1)
    T = st.slider("Temperature T (K)", 100.0, 1500.0, 298.0, 1.0)

    R = 0.082057
    V = n * R * T / P

    st.success(f"**Volume V = {V:.4f} L**")

    v_vals = np.linspace(0.1, 50, 300)
    p_vals = n * R * T / v_vals
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=v_vals, y=p_vals, mode="lines",
                              line=dict(color="#6366f1", width=2), name="P vs V"))
    fig.add_trace(go.Scatter(x=[V], y=[P], mode="markers",
                              marker=dict(size=12, color="#ef4444", symbol="x"), name="Current"))
    fig.update_layout(height=350, xaxis_title="Volume (L)", yaxis_title="Pressure (atm)",
                      margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ================================================================
#                     PERIODIC TREND EXPLORER
# ================================================================
elif topic == "Periodic Trend Explorer":
    st.markdown("## Periodic Trends")
    st.markdown("Explore how properties vary across groups and down periods.")

    trend = st.selectbox("Property", [
        "Atomic Radius (pm)", "Ionization Energy (eV)",
        "Electronegativity (Pauling)", "Electron Affinity (eV)",
    ])

    elements_data = {
        "Li": {"Atomic Radius": 152, "Ionization Energy": 5.39, "Electronegativity": 0.98, "Electron Affinity": 0.618, "Period": 2},
        "Be": {"Atomic Radius": 112, "Ionization Energy": 9.32, "Electronegativity": 1.57, "Electron Affinity": -0.5, "Period": 2},
        "B":  {"Atomic Radius": 87,  "Ionization Energy": 8.30, "Electronegativity": 2.04, "Electron Affinity": 0.277, "Period": 2},
        "C":  {"Atomic Radius": 77,  "Ionization Energy": 11.26, "Electronegativity": 2.55, "Electron Affinity": 1.262, "Period": 2},
        "N":  {"Atomic Radius": 75,  "Ionization Energy": 14.53, "Electronegativity": 3.04, "Electron Affinity": -0.07, "Period": 2},
        "O":  {"Atomic Radius": 73,  "Ionization Energy": 13.62, "Electronegativity": 3.44, "Electron Affinity": 1.461, "Period": 2},
        "F":  {"Atomic Radius": 71,  "Ionization Energy": 17.42, "Electronegativity": 3.98, "Electron Affinity": 3.399, "Period": 2},
        "Ne": {"Atomic Radius": 69,  "Ionization Energy": 21.56, "Electronegativity": 0.0, "Electron Affinity": -1.2, "Period": 2},
        "Na": {"Atomic Radius": 186, "Ionization Energy": 5.14, "Electronegativity": 0.93, "Electron Affinity": 0.548, "Period": 3},
        "Mg": {"Atomic Radius": 160, "Ionization Energy": 7.65, "Electronegativity": 1.31, "Electron Affinity": -0.4, "Period": 3},
        "Al": {"Atomic Radius": 143, "Ionization Energy": 5.99, "Electronegativity": 1.61, "Electron Affinity": 0.433, "Period": 3},
        "Si": {"Atomic Radius": 117, "Ionization Energy": 8.15, "Electronegativity": 1.90, "Electron Affinity": 1.385, "Period": 3},
        "P":  {"Atomic Radius": 110, "Ionization Energy": 10.49, "Electronegativity": 2.19, "Electron Affinity": 0.746, "Period": 3},
        "S":  {"Atomic Radius": 104, "Ionization Energy": 10.36, "Electronegativity": 2.58, "Electron Affinity": 2.077, "Period": 3},
        "Cl": {"Atomic Radius": 99,  "Ionization Energy": 12.97, "Electronegativity": 3.16, "Electron Affinity": 3.613, "Period": 3},
        "Ar": {"Atomic Radius": 97,  "Ionization Energy": 15.76, "Electronegativity": 0.0, "Electron Affinity": -1.0, "Period": 3},
    }

    if "Radius" in trend:
        prop, unit = "Atomic Radius", "pm"
    elif "Ionization" in trend:
        prop, unit = "Ionization Energy", "eV"
    elif "Electronegativity" in trend:
        prop, unit = "Electronegativity", "Pauling"
    else:
        prop, unit = "Electron Affinity", "eV"

    period2 = {k: v for k, v in elements_data.items() if v["Period"] == 2}
    period3 = {k: v for k, v in elements_data.items() if v["Period"] == 3}

    fig = go.Figure()
    for label, data, color in [("Period 2", period2, "#6366f1"), ("Period 3", period3, "#10b981")]:
        names = list(data.keys())
        vals = [data[n][prop] for n in names]
        fig.add_trace(go.Scatter(x=names, y=vals, mode="lines+markers",
                                  name=label, line=dict(color=color, width=2),
                                  marker=dict(size=10, color=color)))
    fig.update_layout(height=400, xaxis_title="Element", yaxis_title=f"{prop} ({unit})",
                      margin=dict(l=20, r=20, t=20, b=20), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    decrease_across = "Radius" in trend
    st.info(
        f"💡 **Trend:** {prop} generally "
        f"{'decreases' if decrease_across else 'increases'} across a period "
        f"(left → right) and "
        f"{'increases' if decrease_across else 'decreases'} down a group (top → bottom)."
    )

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with Python · Streamlit · Plotly · NumPy")
