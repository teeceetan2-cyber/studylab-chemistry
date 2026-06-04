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
    "🔥 Energetics",
    "📖 Notes",
])

topic_map = {
    "⚗️ Acids & Bases": ["pH Calculator"],
    "🧮 Stoichiometry": ["Molar Mass Calculator", "Stoichiometry"],
    "💨 Gas Laws": ["Ideal Gas Law"],
    "🔬 Periodic Table": ["Periodic Trend Explorer"],
    "🔥 Energetics": [
        "⚡ Enthalpy Profile",
        "🔥 Calorimetry",
        "📐 Hess's Law",
        "🔗 Bond Enthalpy",
        "⚛️ Lattice Energy",
        "🧿 Gibbs Free Energy",
    ],
    "📖 Notes": ["Qualitative Analysis", "Electrolysis", "Reactivity Series"],
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
    st.markdown("Explore how properties vary across groups and down periods. Compare up to 2 different sets.")

    # ── Comprehensive element data: Groups 1A–8A & Period 4 ──
    ELEMENTS = {
        # Group 1A (Alkali metals)
        "Li": {"Atomic Radius": 152, "Ionization Energy": 5.39, "Electronegativity": 0.98, "Electron Affinity": 0.618, "Group": "1A", "Period": 2, "Color": "#e74c3c"},
        "Na": {"Atomic Radius": 186, "Ionization Energy": 5.14, "Electronegativity": 0.93, "Electron Affinity": 0.548, "Group": "1A", "Period": 3, "Color": "#e74c3c"},
        "K":  {"Atomic Radius": 227, "Ionization Energy": 4.34, "Electronegativity": 0.82, "Electron Affinity": 0.502, "Group": "1A", "Period": 4, "Color": "#e74c3c"},
        "Rb": {"Atomic Radius": 248, "Ionization Energy": 4.18, "Electronegativity": 0.78, "Electron Affinity": 0.486, "Group": "1A", "Period": 5, "Color": "#e74c3c"},
        "Cs": {"Atomic Radius": 265, "Ionization Energy": 3.89, "Electronegativity": 0.79, "Electron Affinity": 0.472, "Group": "1A", "Period": 6, "Color": "#e74c3c"},
        # Group 2A (Alkaline earth)
        "Be": {"Atomic Radius": 112, "Ionization Energy": 9.32, "Electronegativity": 1.57, "Electron Affinity": -0.5, "Group": "2A", "Period": 2, "Color": "#f39c12"},
        "Mg": {"Atomic Radius": 160, "Ionization Energy": 7.65, "Electronegativity": 1.31, "Electron Affinity": -0.4, "Group": "2A", "Period": 3, "Color": "#f39c12"},
        "Ca": {"Atomic Radius": 197, "Ionization Energy": 6.11, "Electronegativity": 1.00, "Electron Affinity": 0.024, "Group": "2A", "Period": 4, "Color": "#f39c12"},
        "Sr": {"Atomic Radius": 215, "Ionization Energy": 5.70, "Electronegativity": 0.95, "Electron Affinity": 0.052, "Group": "2A", "Period": 5, "Color": "#f39c12"},
        "Ba": {"Atomic Radius": 222, "Ionization Energy": 5.21, "Electronegativity": 0.89, "Electron Affinity": 0.138, "Group": "2A", "Period": 6, "Color": "#f39c12"},
        # Group 3A (13)
        "B":  {"Atomic Radius": 87,  "Ionization Energy": 8.30, "Electronegativity": 2.04, "Electron Affinity": 0.277, "Group": "3A", "Period": 2, "Color": "#2ecc71"},
        "Al": {"Atomic Radius": 143, "Ionization Energy": 5.99, "Electronegativity": 1.61, "Electron Affinity": 0.433, "Group": "3A", "Period": 3, "Color": "#2ecc71"},
        "Ga": {"Atomic Radius": 122, "Ionization Energy": 6.00, "Electronegativity": 1.81, "Electron Affinity": 0.43, "Group": "3A", "Period": 4, "Color": "#2ecc71"},
        "In": {"Atomic Radius": 163, "Ionization Energy": 5.79, "Electronegativity": 1.78, "Electron Affinity": 0.30, "Group": "3A", "Period": 5, "Color": "#2ecc71"},
        "Tl": {"Atomic Radius": 170, "Ionization Energy": 6.11, "Electronegativity": 1.62, "Electron Affinity": 0.20, "Group": "3A", "Period": 6, "Color": "#2ecc71"},
        # Group 4A (14)
        "C":  {"Atomic Radius": 77,  "Ionization Energy": 11.26, "Electronegativity": 2.55, "Electron Affinity": 1.262, "Group": "4A", "Period": 2, "Color": "#1abc9c"},
        "Si": {"Atomic Radius": 117, "Ionization Energy": 8.15, "Electronegativity": 1.90, "Electron Affinity": 1.385, "Group": "4A", "Period": 3, "Color": "#1abc9c"},
        "Ge": {"Atomic Radius": 122, "Ionization Energy": 7.90, "Electronegativity": 2.01, "Electron Affinity": 1.23, "Group": "4A", "Period": 4, "Color": "#1abc9c"},
        "Sn": {"Atomic Radius": 140, "Ionization Energy": 7.34, "Electronegativity": 1.96, "Electron Affinity": 1.20, "Group": "4A", "Period": 5, "Color": "#1abc9c"},
        "Pb": {"Atomic Radius": 175, "Ionization Energy": 7.42, "Electronegativity": 2.33, "Electron Affinity": 0.36, "Group": "4A", "Period": 6, "Color": "#1abc9c"},
        # Group 5A (15)
        "N":  {"Atomic Radius": 75,  "Ionization Energy": 14.53, "Electronegativity": 3.04, "Electron Affinity": -0.07, "Group": "5A", "Period": 2, "Color": "#3498db"},
        "P":  {"Atomic Radius": 110, "Ionization Energy": 10.49, "Electronegativity": 2.19, "Electron Affinity": 0.746, "Group": "5A", "Period": 3, "Color": "#3498db"},
        "As": {"Atomic Radius": 121, "Ionization Energy": 9.81, "Electronegativity": 2.18, "Electron Affinity": 0.81, "Group": "5A", "Period": 4, "Color": "#3498db"},
        "Sb": {"Atomic Radius": 140, "Ionization Energy": 8.64, "Electronegativity": 2.05, "Electron Affinity": 1.05, "Group": "5A", "Period": 5, "Color": "#3498db"},
        "Bi": {"Atomic Radius": 155, "Ionization Energy": 7.29, "Electronegativity": 2.02, "Electron Affinity": 0.95, "Group": "5A", "Period": 6, "Color": "#3498db"},
        # Group 6A (16)
        "O":  {"Atomic Radius": 73,  "Ionization Energy": 13.62, "Electronegativity": 3.44, "Electron Affinity": 1.461, "Group": "6A", "Period": 2, "Color": "#9b59b6"},
        "S":  {"Atomic Radius": 104, "Ionization Energy": 10.36, "Electronegativity": 2.58, "Electron Affinity": 2.077, "Group": "6A", "Period": 3, "Color": "#9b59b6"},
        "Se": {"Atomic Radius": 117, "Ionization Energy": 9.75, "Electronegativity": 2.55, "Electron Affinity": 2.02, "Group": "6A", "Period": 4, "Color": "#9b59b6"},
        "Te": {"Atomic Radius": 137, "Ionization Energy": 9.01, "Electronegativity": 2.10, "Electron Affinity": 1.97, "Group": "6A", "Period": 5, "Color": "#9b59b6"},
        "Po": {"Atomic Radius": 167, "Ionization Energy": 8.42, "Electronegativity": 2.00, "Electron Affinity": 1.09, "Group": "6A", "Period": 6, "Color": "#9b59b6"},
        # Group 7A (Halogens)
        "F":  {"Atomic Radius": 71,  "Ionization Energy": 17.42, "Electronegativity": 3.98, "Electron Affinity": 3.399, "Group": "7A", "Period": 2, "Color": "#e67e22"},
        "Cl": {"Atomic Radius": 99,  "Ionization Energy": 12.97, "Electronegativity": 3.16, "Electron Affinity": 3.613, "Group": "7A", "Period": 3, "Color": "#e67e22"},
        "Br": {"Atomic Radius": 114, "Ionization Energy": 11.81, "Electronegativity": 2.96, "Electron Affinity": 3.365, "Group": "7A", "Period": 4, "Color": "#e67e22"},
        "I":  {"Atomic Radius": 133, "Ionization Energy": 10.45, "Electronegativity": 2.66, "Electron Affinity": 3.059, "Group": "7A", "Period": 5, "Color": "#e67e22"},
        "At": {"Atomic Radius": 140, "Ionization Energy": 9.32, "Electronegativity": 2.20, "Electron Affinity": 2.80, "Group": "7A", "Period": 6, "Color": "#e67e22"},
        # Group 8A (Noble gases)
        "He": {"Atomic Radius": 31,  "Ionization Energy": 24.59, "Electronegativity": 0.0, "Electron Affinity": -0.5, "Group": "8A", "Period": 1, "Color": "#95a5a6"},
        "Ne": {"Atomic Radius": 69,  "Ionization Energy": 21.56, "Electronegativity": 0.0, "Electron Affinity": -1.2, "Group": "8A", "Period": 2, "Color": "#95a5a6"},
        "Ar": {"Atomic Radius": 97,  "Ionization Energy": 15.76, "Electronegativity": 0.0, "Electron Affinity": -1.0, "Group": "8A", "Period": 3, "Color": "#95a5a6"},
        "Kr": {"Atomic Radius": 112, "Ionization Energy": 14.00, "Electronegativity": 0.0, "Electron Affinity": -0.6, "Group": "8A", "Period": 4, "Color": "#95a5a6"},
        "Xe": {"Atomic Radius": 130, "Ionization Energy": 12.13, "Electronegativity": 0.0, "Electron Affinity": -0.5, "Group": "8A", "Period": 5, "Color": "#95a5a6"},
        "Rn": {"Atomic Radius": 145, "Ionization Energy": 10.75, "Electronegativity": 0.0, "Electron Affinity": -0.5, "Group": "8A", "Period": 6, "Color": "#95a5a6"},
        # Period 4 transition metals + Ga–Kr
        "Sc": {"Atomic Radius": 162, "Ionization Energy": 6.56, "Electronegativity": 1.36, "Electron Affinity": 0.188, "Group": "3B", "Period": 4, "Color": "#1abc9c"},
        "Ti": {"Atomic Radius": 147, "Ionization Energy": 6.83, "Electronegativity": 1.54, "Electron Affinity": 0.079, "Group": "4B", "Period": 4, "Color": "#3498db"},
        "V":  {"Atomic Radius": 134, "Ionization Energy": 6.75, "Electronegativity": 1.63, "Electron Affinity": 0.525, "Group": "5B", "Period": 4, "Color": "#9b59b6"},
        "Cr": {"Atomic Radius": 128, "Ionization Energy": 6.77, "Electronegativity": 1.66, "Electron Affinity": 0.666, "Group": "6B", "Period": 4, "Color": "#e74c3c"},
        "Mn": {"Atomic Radius": 127, "Ionization Energy": 7.43, "Electronegativity": 1.55, "Electron Affinity": 0.0, "Group": "7B", "Period": 4, "Color": "#e67e22"},
        "Fe": {"Atomic Radius": 126, "Ionization Energy": 7.90, "Electronegativity": 1.83, "Electron Affinity": 0.151, "Group": "8B", "Period": 4, "Color": "#f39c12"},
        "Co": {"Atomic Radius": 125, "Ionization Energy": 7.88, "Electronegativity": 1.88, "Electron Affinity": 0.662, "Group": "8B", "Period": 4, "Color": "#2ecc71"},
        "Ni": {"Atomic Radius": 124, "Ionization Energy": 7.64, "Electronegativity": 1.91, "Electron Affinity": 1.156, "Group": "8B", "Period": 4, "Color": "#1abc9c"},
        "Cu": {"Atomic Radius": 128, "Ionization Energy": 7.73, "Electronegativity": 1.90, "Electron Affinity": 1.235, "Group": "1B", "Period": 4, "Color": "#3498db"},
        "Zn": {"Atomic Radius": 134, "Ionization Energy": 9.39, "Electronegativity": 1.65, "Electron Affinity": 0.0, "Group": "2B", "Period": 4, "Color": "#9b59b6"},
    }

    # Property mapping
    props = {
        "Atomic Radius (pm)": ("Atomic Radius", "pm"),
        "Ionization Energy (eV)": ("Ionization Energy", "eV"),
        "Electronegativity (Pauling)": ("Electronegativity", "Pauling"),
        "Electron Affinity (eV)": ("Electron Affinity", "eV"),
    }

    # Set definitions: groups + period
    set_elements = {
        "Group 1A": [sym for sym, d in ELEMENTS.items() if d["Group"] == "1A"],
        "Group 2A": [sym for sym, d in ELEMENTS.items() if d["Group"] == "2A"],
        "Group 3A": [sym for sym, d in ELEMENTS.items() if d["Group"] == "3A"],
        "Group 4A": [sym for sym, d in ELEMENTS.items() if d["Group"] == "4A"],
        "Group 5A": [sym for sym, d in ELEMENTS.items() if d["Group"] == "5A"],
        "Group 6A": [sym for sym, d in ELEMENTS.items() if d["Group"] == "6A"],
        "Group 7A": [sym for sym, d in ELEMENTS.items() if d["Group"] == "7A"],
        "Group 8A": [sym for sym, d in ELEMENTS.items() if d["Group"] == "8A"],
        "Period 2": [sym for sym, d in ELEMENTS.items() if d["Period"] == 2],
        "Period 3": [sym for sym, d in ELEMENTS.items() if d["Period"] == 3],
        "Period 4": [sym for sym, d in ELEMENTS.items() if d["Period"] == 4],
    }

    group_colors = {
        "Group 1A": "#e74c3c", "Group 2A": "#f39c12", "Group 3A": "#2ecc71",
        "Group 4A": "#1abc9c", "Group 5A": "#3498db", "Group 6A": "#9b59b6",
        "Group 7A": "#e67e22", "Group 8A": "#95a5a6", "Period 2": "#a78bfa",
        "Period 3": "#f472b6", "Period 4": "#6366f1",
    }

    col1, col2 = st.columns([2, 1])
    with col1:
        trend = st.selectbox("Property", list(props.keys()))
    with col2:
        chart_type = st.selectbox("Chart type", ["Bar chart", "Line chart"])

    prop, unit = props[trend]

    # Set 1
    set1_label = st.selectbox("Set 1", list(set_elements.keys()), key="set1")
    compare = st.checkbox("Compare with another set")

    set2_label = None
    if compare:
        set2_options = [s for s in set_elements.keys() if s != set1_label]
        set2_label = st.selectbox("Set 2", set2_options, key="set2")

    # Build chart
    fig = go.Figure()
    colors_list = ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899"]

    def add_set_to_fig(fig, label, elements_list, color, prop, chart_type, idx=0):
        names = elements_list
        vals = [ELEMENTS[n][prop] for n in names]
        dash = "dot" if idx == 1 else "solid"
        if chart_type == "Bar chart":
            offset = -0.2 if idx == 0 else 0.2
            fig.add_trace(go.Bar(
                x=names, y=vals, name=label,
                marker_color=color, opacity=0.85,
                offset=offset,
                text=[f"{v:.2f}" for v in vals],
                textposition="outside",
                hovertemplate=f"<b>%{{x}}</b><br>{prop}: %{{y:.2f}} {unit}<extra>{label}</extra>",
            ))
        else:
            marker = dict(size=10, color=color, symbol="circle" if idx == 0 else "diamond")
            fig.add_trace(go.Scatter(
                x=names, y=vals, mode="lines+markers",
                name=label, line=dict(color=color, width=2, dash=dash),
                marker=marker,
                hovertemplate=f"<b>%{{x}}</b><br>{prop}: %{{y:.2f}} {unit}<extra>{label}</extra>",
            ))

    add_set_to_fig(fig, set1_label, set_elements[set1_label],
                   group_colors.get(set1_label, colors_list[0]), prop, chart_type, 0)

    if set2_label:
        add_set_to_fig(fig, set2_label, set_elements[set2_label],
                       group_colors.get(set2_label, colors_list[1]), prop, chart_type, 1)

    fig.update_layout(
        height=450,
        xaxis_title="Element",
        yaxis_title=f"{prop} ({unit})",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#ccc",
        hovermode="x unified",
        barmode="group",
        margin=dict(l=10, r=10, t=10, b=30),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Trend description
    decreasing = ["Atomic Radius"]
    if prop in decreasing:
        trend_dir = f"decreases across a period (L→R) and increases down a group (top→bottom)"
    elif prop == "Ionization Energy":
        trend_dir = f"generally increases across a period (L→R) and decreases down a group (top→bottom)"
    elif prop == "Electronegativity":
        trend_dir = f"increases across a period (L→R) and decreases down a group (top→bottom)"
    else:
        trend_dir = f"varies; generally more negative (exothermic) for halogens, least for noble gases"

    st.info(f"💡 **{prop} Trend:** {trend_dir}.")

    if set2_label:
        st.markdown(f"📊 **{set1_label}** vs **{set2_label}** — values shown side by side for comparison.")

# ================================================================
#                    ⚡ ENTHALPY PROFILE
# ================================================================
elif topic == "⚡ Enthalpy Profile":
    st.markdown("## ⚡ Enthalpy Profile")
    st.markdown("Visualize energy changes in exothermic and endothermic reactions.")

    col1, col2 = st.columns(2)
    with col1:
        dh = st.number_input("Enthalpy change ΔH (kJ/mol)", -500.0, 500.0, -100.0, 5.0,
                             help="Negative = exothermic, Positive = endothermic")
    with col2:
        ea = st.number_input("Activation energy Ea (kJ/mol)", 0.0, 500.0, 50.0, 5.0,
                             help="Energy barrier from reactants to transition state")

    is_exo = dh < 0
    dh_abs = abs(dh)

    # Energy profile: reactants at 0, products at dh, peak at ea
    r_energy = 0.0
    ts_energy = ea
    p_energy = dh

    # Build smooth curve
    x_curve = np.linspace(0, 4, 200)
    y_curve = np.piecewise(x_curve,
        [x_curve < 1.5, (x_curve >= 1.5) & (x_curve < 2.5), x_curve >= 2.5],
        [lambda x: np.interp(x, [0, 1.5], [r_energy, ts_energy]),
         lambda x: np.interp(x, [1.5, 2.5], [ts_energy, ts_energy]),
         lambda x: np.interp(x, [2.5, 4], [ts_energy, p_energy])])
    # Smooth using polynomial
    z = np.polyfit([0, 1.5, 2.5, 4], [r_energy, ts_energy, ts_energy, p_energy], 3)
    y_smooth = np.polyval(z, x_curve)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_curve, y=y_smooth, mode="lines",
                              line=dict(color="#6366f1", width=3),
                              name="Reaction progress",
                              hovertemplate="Energy: %{y:.1f} kJ/mol<extra></extra>"))
    # Horizontal dashed lines for energy levels
    max_y = max(ea, 0) * 1.3
    min_y = min(dh, 0) * 1.3
    y_range = [min_y - 20, max_y + 20]
    fig.add_hline(y=r_energy, line=dict(color="#10b981", width=1, dash="dot"), name="Reactants")
    fig.add_hline(y=p_energy, line=dict(color="#f59e0b", width=1, dash="dot"), name="Products")
    fig.add_hline(y=ts_energy, line=dict(color="#ef4444", width=1, dash="dot"), name="Transition state")

    # ΔH arrow
    mid_x = 2.0
    arrow_y = (r_energy + p_energy) / 2
    fig.add_annotation(x=3.8, y=arrow_y,
                       text=f"ΔH = {dh:+.0f} kJ/mol {'🔥' if is_exo else '❄️'}",
                       showarrow=False,
                       font=dict(size=14, color="#10b981" if is_exo else "#ef4444"))

    # Ea arrow
    ea_mid_y = (r_energy + ts_energy) / 2
    fig.add_annotation(x=1.5, y=ea_mid_y - 20,
                       text=f"Ea = {ea:.0f} kJ/mol",
                       showarrow=False,
                       font=dict(size=12, color="#f59e0b"))

    fig.update_layout(
        height=450,
        xaxis=dict(showticklabels=False, title="Reaction progress →"),
        yaxis=dict(title="Enthalpy (kJ/mol)"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#ccc",
        margin=dict(l=10, r=10, t=10, b=30),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Summary
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Reaction type", "Exothermic 🔥" if is_exo else "Endothermic ❄️")
    with col_b:
        st.metric("ΔH", f"{dh:+.0f} kJ/mol")
    with col_c:
        st.metric("Activation Energy Ea", f"{ea:.0f} kJ/mol")

    st.info(f"""
    💡 **{('Exothermic' if is_exo else 'Endothermic')} reactions** — The products have
    **{'lower' if is_exo else 'higher'}** enthalpy than the reactants.
    ΔH = **{dh:+.0f} kJ/mol**.
    """)

# ================================================================
#                      🔥 CALORIMETRY
# ================================================================
elif topic == "🔥 Calorimetry":
    st.markdown("## 🔥 Calorimetry")
    st.latex(r"q = mc\Delta T")
    st.markdown("Solve for any variable in the heat equation.")

    solve_for = st.radio("Solve for:", ["Heat energy (q)", "Mass (m)", "Specific heat capacity (c)", "Temperature change (ΔT)"],
                          horizontal=True)

    if solve_for == "Heat energy (q)":
        col1, col2, col3 = st.columns(3)
        with col1:
            m = st.number_input("Mass (g)", 0.0, 10000.0, 100.0, 1.0)
        with col2:
            c = st.number_input("Specific heat capacity (J/g·°C)", 0.0, 10.0, 4.18, 0.01,
                                help="Water = 4.18, Ice = 2.09, Aluminum = 0.90")
        with col3:
            dt = st.number_input("ΔT (°C)", -200.0, 200.0, 10.0, 0.5)
        q = m * c * dt
        unit = "kJ" if abs(q) >= 1000 else "J"
        val = q / 1000 if abs(q) >= 1000 else q
        st.success(f"**q = {val:.4f} {unit}**")
        st.markdown(f"""<div class="result-box">
            q = {m:.2f}g × {c:.4f} J/g°C × {dt:+.2f}°C = {q:.2f} J = {q/1000:.4f} kJ
        </div>""", unsafe_allow_html=True)
        if q > 0:
            st.info("🔥 System **gains** heat (endothermic process)")
        else:
            st.info("❄️ System **loses** heat (exothermic process)")

    elif solve_for == "Mass (m)":
        col1, col2, col3 = st.columns(3)
        with col1:
            q = st.number_input("Heat energy q (J)", 0.0, 1e7, 4180.0, 100.0)
        with col2:
            c = st.number_input("Specific heat capacity (J/g·°C)", 0.0, 10.0, 4.18, 0.01)
        with col3:
            dt = st.number_input("ΔT (°C)", 0.0, 200.0, 10.0, 0.5)
        m = q / (c * dt) if c * dt > 0 else 0
        st.success(f"**m = {m:.4f} g**")

    elif solve_for == "Specific heat capacity (c)":
        col1, col2, col3 = st.columns(3)
        with col1:
            q = st.number_input("Heat energy q (J)", 0.0, 1e7, 4180.0, 100.0)
        with col2:
            m = st.number_input("Mass (g)", 0.0, 10000.0, 100.0, 1.0)
        with col3:
            dt = st.number_input("ΔT (°C)", 0.0, 200.0, 10.0, 0.5)
        c = q / (m * dt) if m * dt > 0 else 0
        st.success(f"**c = {c:.4f} J/g·°C**")
        if 4.0 < c < 4.3:
            st.info("💡 This is close to water's specific heat capacity (4.18 J/g·°C)")

    else:  # ΔT
        col1, col2, col3 = st.columns(3)
        with col1:
            q = st.number_input("Heat energy q (J)", -1e7, 1e7, 4180.0, 100.0)
        with col2:
            m = st.number_input("Mass (g)", 0.0, 10000.0, 100.0, 1.0)
        with col3:
            c = st.number_input("Specific heat capacity (J/g·°C)", 0.0, 10.0, 4.18, 0.01)
        dt = q / (m * c) if m * c > 0 else 0
        st.success(f"**ΔT = {dt:.4f} °C**")

    st.markdown("### Common Specific Heat Capacities")
    common_c = {"Water": 4.18, "Ice (−10°C)": 2.09, "Steam": 2.01, "Aluminum": 0.90,
                 "Copper": 0.39, "Iron": 0.45, "Gold": 0.13, "Ethanol": 2.44}
    cols = st.columns(4)
    for i, (mat, val) in enumerate(common_c.items()):
        cols[i % 4].metric(mat, f"{val} J/g·°C")

# ================================================================
#                   📐 HESS'S LAW
# ================================================================
elif topic == "📐 Hess's Law":
    st.markdown("## 📐 Hess's Law")
    st.latex(r"\Delta H_{\text{target}} = \sum \Delta H_{\text{steps}}")
    st.markdown("Calculate the enthalpy change of a target reaction using known ΔH values of other reactions.")

    st.subheader("Step Reactions")
    n_steps = st.slider("Number of steps", 2, 5, 3)

    step_eqs = []
    step_dhs = []
    coeffs = []
    cols = st.columns(min(n_steps, 3))
    for i in range(n_steps):
        with cols[i % 3]:
            st.markdown(f"**Step {i + 1}**")
            eq = st.text_input(f"Equation {i + 1}", placeholder=f"e.g. A → B",
                               key=f"hess_eq_{i}", label_visibility="collapsed")
            dh = st.number_input(f"ΔH {i + 1} (kJ/mol)", -1000.0, 1000.0, 0.0, 5.0,
                                 key=f"hess_dh_{i}", format="%.1f", label_visibility="collapsed")
            coeff = st.selectbox(f"Coefficient", [1, -1, 2, -2, 3, -3, 0.5, -0.5], index=0,
                                 key=f"hess_c_{i}", label_visibility="collapsed",
                                 help="Use -1 if the reaction is reversed, 2 if doubled, etc.")
            step_eqs.append(eq)
            step_dhs.append(dh)
            coeffs.append(coeff)

    target_dh = sum(dh * c for dh, c in zip(step_dhs, coeffs))

    if any(eq for eq in step_eqs):
        st.divider()
        st.subheader("Calculation")
        lines = []
        for i, (eq, dh, c) in enumerate(zip(step_eqs, step_dhs, coeffs)):
            sign = "+" if c >= 0 else "−"
            arrow = "→" if c >= 0 else "←"
            mod_eq = f"{eq}"
            if abs(c) != 1:
                mod_eq = f"({abs(c):g}) {eq.split('→')[0].strip() if '→' in eq else eq} → ..."
            lines.append(f"{sign} ΔH{i + 1} = {c * dh:+.1f} kJ/mol")

        st.markdown(f"""<div class="result-box">
            <b>Target ΔH = {' + '.join(f'({c:.1f} × {dh:.1f})' for dh, c in zip(step_dhs, coeffs) if c != 0) if any(c != 0 for c in coeffs) else '0'}</b><br>
            <b>ΔH<sub>target</sub> = {target_dh:+.2f} kJ/mol</b>
        </div>""", unsafe_allow_html=True)

        # Visual bar
        colors = ["#10b981" if dh * c >= 0 else "#ef4444" for dh, c in zip(step_dhs, coeffs)]
        fig = go.Figure()
        for i, (eq, dh, c, color) in enumerate(zip(step_eqs, step_dhs, coeffs, colors)):
            val = c * dh
            fig.add_trace(go.Bar(
                x=[abs(val)], y=[f"Step {i + 1}"], orientation="h",
                marker_color=color,
                name=f"Step {i + 1}: {val:+.0f} kJ/mol",
                text=f"{val:+.0f}" if val != 0 else "0",
                textposition="outside",
            ))
        fig.add_trace(go.Bar(
            x=[abs(target_dh)], y=["Target"], orientation="h",
            marker_color="#6366f1",
            name=f"Target: {target_dh:+.0f} kJ/mol",
            text=f"{target_dh:+.0f}",
            textposition="outside",
        ))
        fig.update_layout(
            height=60 * (n_steps + 2),
            barmode="relative",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#ccc",
            xaxis=dict(title="ΔH (kJ/mol)"),
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

# ================================================================
#                     🔗 BOND ENTHALPY
# ================================================================
elif topic == "🔗 Bond Enthalpy":
    st.markdown("## 🔗 Bond Enthalpy")
    st.latex(r"\Delta H = \sum \text{{Bonds broken}} - \sum \text{{Bonds formed}}")

    BOND_ENERGIES = {
        "H−H": 436, "H−F": 565, "H−Cl": 431, "H−Br": 366, "H−I": 299,
        "C−H": 413, "C−C": 347, "C=C": 612, "C≡C": 839,
        "C−O": 358, "C=O": 799, "C≡O": 1072,
        "C−N": 305, "C=N": 615, "C≡N": 891,
        "O−H": 463, "O−O": 146, "O=O": 498,
        "N−H": 391, "N≡N": 945, "N−N": 163,
        "F−F": 158, "Cl−Cl": 242, "Br−Br": 193, "I−I": 151,
        "S−H": 363, "S−S": 268,
        "P−O": 335, "P=O": 544,
        "Si−O": 464, "Si−Si": 222,
        "C−Cl": 339, "C−Br": 276, "C−I": 240,
        "O−C=O": 532,
    }

    tab_b, tab_c = st.tabs(["Calculator", "Bond Energy Table"])

    with tab_b:
        st.markdown("Enter bonds broken (reactants) and bonds formed (products):")
        col_b1, col_b2 = st.columns(2)

        with col_b1:
            st.markdown("**Bonds Broken** (energy absorbed)")
            broken_bonds = []
            for i in range(6):
                bb = st.selectbox(f"Bond {i + 1}", [""] + sorted(BOND_ENERGIES.keys()), index=0,
                                  key=f"bb_{i}", label_visibility="collapsed")
                bc = st.number_input(f"Count", 0, 10, 1, key=f"bc_{i}", label_visibility="collapsed")
                if bb and bc:
                    broken_bonds.append((bb, BOND_ENERGIES[bb], bc))

        with col_b2:
            st.markdown("**Bonds Formed** (energy released)")
            formed_bonds = []
            for i in range(6):
                fb = st.selectbox(f"Bond {i + 1}", [""] + sorted(BOND_ENERGIES.keys()), index=0,
                                  key=f"fb_{i}", label_visibility="collapsed")
                fc = st.number_input(f"Count", 0, 10, 1, key=f"fc_{i}", label_visibility="collapsed")
                if fb and fc:
                    formed_bonds.append((fb, BOND_ENERGIES[fb], fc))

        if broken_bonds or formed_bonds:
            total_broken = sum(energy * count for _, energy, count in broken_bonds)
            total_formed = sum(energy * count for _, energy, count in formed_bonds)
            dh_bond = total_broken - total_formed

            st.divider()
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric("Energy absorbed (broken)", f"{total_broken:.0f} kJ/mol")
            with col_r2:
                st.metric("Energy released (formed)", f"{total_formed:.0f} kJ/mol")
            with col_r3:
                st.metric("ΔH", f"{dh_bond:+.0f} kJ/mol",
                          delta_color="inverse")

            fig = go.Figure()
            fig.add_trace(go.Bar(name="Bonds broken (+)", x=["Energy"], y=[total_broken],
                                  marker_color="#ef4444",
                                  text=f"{total_broken:.0f} kJ/mol", textposition="outside"))
            fig.add_trace(go.Bar(name="Bonds formed (−)", x=["Energy"], y=[-total_formed],
                                  marker_color="#10b981",
                                  text=f"−{total_formed:.0f} kJ/mol", textposition="outside"))
            fig.add_trace(go.Bar(name=f"ΔH = {dh_bond:+.0f}", x=["Net"], y=[dh_bond],
                                  marker_color="#6366f1",
                                  text=f"{dh_bond:+.0f} kJ/mol", textposition="outside"))
            fig.update_layout(height=300, plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)", font_color="#ccc",
                              margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)

            st.info("Exothermic " if dh_bond < 0 else "Endothermic ")

    with tab_c:
        st.markdown("**Average Bond Energies (kJ/mol)**")
        cols = st.columns(3)
        sorted_bonds = sorted(BOND_ENERGIES.items(), key=lambda x: x[0])
        for i, (bond, energy) in enumerate(sorted_bonds):
            cols[i % 3].metric(bond, f"{energy} kJ/mol")

# ================================================================
#                    ⚛️ LATTICE ENERGY
# ================================================================
elif topic == "⚛️ Lattice Energy":
    st.markdown("## ⚛️ Lattice Energy — Born-Haber Cycle")

    # Preset compounds with thermodynamic data (kJ/mol)
    COMPOUNDS = {
        "NaCl": {
            "formula": "NaCl", "cation": "Na⁺", "anion": "Cl⁻",
            "dh_f": -411, "dh_atom_M": 108, "dh_atom_X": 122,
            "ie": 496, "ea": -349, "le": None,  # calculated
            "r_cation": 102, "r_anion": 181, "z": 1, "n": 9, "A": 1.7476,
        },
        "MgO": {
            "formula": "MgO", "cation": "Mg²⁺", "anion": "O²⁻",
            "dh_f": -602, "dh_atom_M": 148, "dh_atom_X": 249,
            "ie": 2188, "ea": -844, "le": None,
            "r_cation": 72, "r_anion": 140, "z": 2, "n": 7, "A": 1.7476,
        },
        "KCl": {
            "formula": "KCl", "cation": "K⁺", "anion": "Cl⁻",
            "dh_f": -436, "dh_atom_M": 89, "dh_atom_X": 122,
            "ie": 419, "ea": -349, "le": None,
            "r_cation": 138, "r_anion": 181, "z": 1, "n": 9, "A": 1.7476,
        },
        "CaCl₂": {
            "formula": "CaCl₂", "cation": "Ca²⁺", "anion": "Cl⁻",
            "dh_f": -796, "dh_atom_M": 178, "dh_atom_X": 122,
            "ie": 1735, "ea": -349, "le": None,
            "r_cation": 100, "r_anion": 181, "z": 2, "n": 9, "A": 2.408,
        },
        "Na₂O": {
            "formula": "Na₂O", "cation": "Na⁺", "anion": "O²⁻",
            "dh_f": -414, "dh_atom_M": 108, "dh_atom_X": 249,
            "ie": 496, "ea": -844, "le": None,
            "r_cation": 102, "r_anion": 140, "z": 1, "n": 7, "A": 2.408,
        },
    }

    compound = st.selectbox("Select compound", list(COMPOUNDS.keys()), key="bh_compound")
    data = COMPOUNDS[compound]

    # Calculate lattice energy using Born-Haber cycle
    # ΔH_f = ΔH_atom(M) + IE + ΔH_atom(X) + EA + LE
    # LE = ΔH_f - ΔH_atom(M) - IE - ΔH_atom(X) - EA
    nacl_stoich = 1 if data["formula"] not in ["CaCl₂", "Na₂O"] else (
        2 if data["formula"] == "CaCl₂" else 1  # Na₂O: needs different handling
    )

    if data["formula"] == "CaCl₂":
        le_calc = data["dh_f"] - data["dh_atom_M"] - data["ie"] - 2 * data["dh_atom_X"] - 2 * data["ea"]
    elif data["formula"] == "Na₂O":
        le_calc = data["dh_f"] - 2 * data["dh_atom_M"] - 2 * data["ie"] - data["dh_atom_X"] - data["ea"]
    else:
        le_calc = data["dh_f"] - data["dh_atom_M"] - data["ie"] - data["dh_atom_X"] - data["ea"]

    # Born-Landé theoretical calculation
    N_A = 6.022e23
    e = 1.602e-19
    eps0 = 8.854e-12
    r0 = (data["r_cation"] + data["r_anion"]) * 1e-12  # pm to m
    z = data["z"]
    A = data["A"]
    n = data["n"]
    U = -(N_A * A * z * z * e**2) / (4 * math.pi * eps0 * r0) * (1 - 1/n) / 1000  # kJ/mol

    tab_bh1, tab_bh3 = st.tabs(["📊 Born-Haber Cycle", "📝 Step Details"])

    with tab_bh1:
        st.markdown(f"**Born-Haber Cycle for {data['formula']}**")

        # Build cycle steps (up to EA only — LE is separate)
        steps = []
        if data["formula"] == "CaCl₂":
            steps = [
                ("ΔH_atom(M)", data["dh_atom_M"], "#10b981"),
                ("IE", data["ie"], "#f59e0b"),
                ("2 × ΔH_atom(X)", 2 * data["dh_atom_X"], "#3b82f6"),
                ("2 × EA", 2 * data["ea"], "#ef4444"),
            ]
        elif data["formula"] == "Na₂O":
            steps = [
                ("2 × ΔH_atom(M)", 2 * data["dh_atom_M"], "#10b981"),
                ("2 × IE", 2 * data["ie"], "#f59e0b"),
                ("ΔH_atom(X)", data["dh_atom_X"], "#3b82f6"),
                ("EA (O → O²⁻)", data["ea"], "#ef4444"),
            ]
        else:
            steps = [
                ("ΔH_atom(M)", data["dh_atom_M"], "#10b981"),
                ("IE (total)", data["ie"], "#f59e0b"),
                ("ΔH_atom(X)", data["dh_atom_X"], "#3b82f6"),
                ("EA", data["ea"], "#ef4444"),
            ]

        # Energy level diagram: [0] → ... → gaseous ions (after EA) → product (ΔH_f)
        # LE is the BIG DROP from ions to product
        energy_levels = [0]
        level_labels = ["Elements<br>M(s) + ½X₂(g)"]
        level_colors = ["#6366f1"]
        cumulative = 0
        for name, val, color in steps:
            cumulative += val
            energy_levels.append(cumulative)
            level_labels.append(name)
            level_colors.append(color)

        # Gaseous ions level (after EA) = last cumulative value
        ions_level = cumulative
        product_level = data["dh_f"]

        # Add the product level as final point
        energy_levels.append(product_level)
        level_labels.append(f"{data['formula']}(s)")
        level_colors.append("#10b981" if product_level < 0 else "#ef4444")

        # Also add ΔH_f as an annotation
        dh_f_str = f"ΔH_f = {product_level:+.0f}"

        fig = go.Figure()
        n_points = len(energy_levels)
        x_pos = list(range(n_points))

        # Main path: elements up to gaseous ions (steps 0 through EA)
        fig.add_trace(go.Scatter(
            x=x_pos[:n_points-1], y=energy_levels[:n_points-1], mode="lines+markers",
            marker=dict(size=10, color=level_colors[:n_points-1]),
            line=dict(color="#555", width=2, dash="dot"),
            text=level_labels[:n_points-1],
            hovertemplate="%{text}<br>%{y:+.0f} kJ/mol<extra></extra>",
            name="Steps",
            showlegend=False,
        ))

        # Gaseous ion label at top
        ion_label = data.get("cation", "M⁺") + "(g) + " + data.get("anion", "X⁻") + "(g)"
        fig.add_annotation(
            x=x_pos[n_points-2], y=ions_level,
            text=f"<b>{ion_label}</b>",
            showarrow=True, arrowhead=0, arrowcolor="#888", arrowsize=0.5,
            ax=40, ay=-20,
            font=dict(size=12, color="#f59e0b"),
            bgcolor="#1a1d2a",
            bordercolor="#555",
            borderwidth=1,
        )

        # ── LATTICE ENERGY: bold arrow from ions DOWN to product ──
        le_x = (x_pos[n_points-2] + x_pos[n_points-1]) / 2
        le_mid_y = (ions_level + product_level) / 2
        fig.add_annotation(
            x=le_x + 0.6, y=le_mid_y,
            text=f"<b>Lattice Energy<br>−{abs(le_calc):.0f} kJ/mol</b>",
            font=dict(size=13, color="#8b5cf6"),
            showarrow=False,
            xanchor="left",
        )
        # Draw the vertical LE arrow separately
        fig.add_annotation(
            x=le_x, y=product_level,
            ax=le_x, ay=ions_level,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True,
            arrowhead=2, arrowsize=2, arrowwidth=4, arrowcolor="#8b5cf6",
            text="",
        )

        # Product point
        fig.add_trace(go.Scatter(
            x=[x_pos[n_points-1]], y=[product_level], mode="markers",
            marker=dict(size=14, color="#10b981", symbol="diamond",
                        line=dict(color="white", width=2)),
            text=[f"{data['formula']}(s)"],
            hovertemplate="%{text}<br>%{y:+.0f} kJ/mol<extra></extra>",
            name="Product",
            showlegend=False,
        ))

        # Step annotations (arrows between levels)
        for i in range(len(steps)):
            mid_x = (x_pos[i] + x_pos[i + 1]) / 2
            diff = energy_levels[i + 1] - energy_levels[i]
            color = "#10b981" if diff >= 0 else "#ef4444"
            fig.add_annotation(x=mid_x, y=energy_levels[i] + diff / 2,
                               text=f"{diff:+.0f}",
                               showarrow=False, font=dict(size=10, color=color))

        # ΔH_f bracket on the right
        fig.add_annotation(
            x=max(x_pos) + 0.8, y=(0 + product_level) / 2,
            text=f"<b>ΔH_f = {product_level:+.0f} kJ/mol</b>",
            showarrow=False,
            font=dict(size=12, color="#10b981"),
        )
        # Bracket lines for ΔH_f
        fig.add_annotation(
            x=max(x_pos) + 0.3, y=0,
            ax=max(x_pos) + 0.3, ay=product_level,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=0, arrowwidth=2, arrowcolor="#10b981",
            text="",
        )

        fig.update_layout(
            height=450,
            xaxis=dict(visible=False),
            yaxis=dict(title="Enthalpy (kJ/mol)", zeroline=True, zerolinecolor="#555"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#ccc",
            margin=dict(l=10, r=30, t=10, b=30),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.metric("Lattice Energy (Born-Haber)", f"{le_calc:+.0f} kJ/mol",
                  help="From experimental ΔH_f and cycle data")
        st.metric("Lattice Energy (Born-Landé)", f"{U:+.0f} kJ/mol",
                  help="Theoretical value using Born-Landé equation")



    with tab_bh3:
        st.markdown(f"### Born-Haber Cycle Steps — {data['formula']}")

        cation = data.get("cation", "M⁺")
        anion = data.get("anion", "X⁻")
        formula = data["formula"]

        step_descs = {
            "ΔH_atom(M)": f"{formula.split(chr(8216) if chr(8216) in formula else formula)[0] if formula[0].isalpha() else 'M'}(s) → {formula.split(chr(8216) if chr(8216) in formula else formula)[0] if formula[0].isalpha() else 'M'}(g)",
        }

        step_labels = {
            "ΔH_atom(M)": f"M(s) → M(g)",
            "IE": f"M(g) → {cation}(g) + e⁻",
            "IE (total)": f"M(g) → {cation}(g) + e⁻",
            "2 × IE": f"2M(g) → 2{cation}(g) + 2e⁻",
            "ΔH_atom(X)": f"½X₂(g) → X(g)",
            "2 × ΔH_atom(X)": f"X₂(g) → 2X(g)",
            "EA": f"X(g) + e⁻ → {anion}(g)",
            "2 × EA": f"2X(g) + 2e⁻ → 2{anion}(g)",
            "EA (O → O²⁻)": f"O(g) + 2e⁻ → O²⁻(g)",
        }

        for name, val, color in steps:
            desc = step_labels.get(name, name)
            st.markdown(f"""<div style="background:{color}22;border-left:4px solid {color};
                        padding:8px 12px;border-radius:6px;margin:6px 0;">
                        <b style="color:{color}">{name}</b>: {val:+.0f} kJ/mol<br>
                        <span style="color:#aaa;font-size:0.9em">{desc}</span>
                        </div>""", unsafe_allow_html=True)

        # Lattice Energy as separate bold step
        st.markdown(f"""<div style="background:#8b5cf622;border-left:4px solid #8b5cf6;
                    padding:8px 12px;border-radius:6px;margin:6px 0;">
                    <b style="color:#8b5cf6">Lattice Energy</b>: {le_calc:+.0f} kJ/mol<br>
                    <span style="color:#aaa;font-size:0.9em">{cation}(g) + {anion}(g) → {formula}(s)</span>
                    </div>""", unsafe_allow_html=True)

        step_total = sum(v for _, v, _ in steps)
        st.markdown(f"""<div style="background:#1a1d2a;padding:10px 12px;border-radius:6px;margin-top:10px;">
            <b>Gaseous ions (after EA):</b> {step_total:+.0f} kJ/mol<br>
            <b>After Lattice Energy:</b> {step_total + le_calc:+.0f} kJ/mol<br>
            <b>ΔH<sub>f</sub> (experimental):</b> {data['dh_f']:+.0f} kJ/mol
        </div>""", unsafe_allow_html=True)

# ================================================================
#                   🧿 GIBBS FREE ENERGY
# ================================================================
elif topic == "🧿 Gibbs Free Energy":
    st.markdown("## 🧿 Gibbs Free Energy & Entropy")
    st.latex(r"\Delta G = \Delta H - T\Delta S")
    st.markdown("Predict reaction spontaneity.")

    tab_g1, tab_g2 = st.tabs(["🧮 Calculator", "📊 Spontaneity Explorer"])

    with tab_g1:
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            dh_g = st.number_input("ΔH (kJ/mol)", -500.0, 500.0, -100.0, 5.0, key="gibbs_dh")
        with col_g2:
            ds_g = st.number_input("ΔS (J/mol·K)", -300.0, 300.0, 100.0, 5.0, key="gibbs_ds",
                                   help="Entropy change in J/mol·K")
        with col_g3:
            t_g = st.number_input("Temperature T (K)", 0.0, 2000.0, 298.0, 5.0, key="gibbs_t",
                                  help="Standard = 298 K")

        ds_kj = ds_g / 1000.0  # Convert to kJ
        dg = dh_g - t_g * ds_kj

        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("ΔG", f"{dg:+.2f} kJ/mol")
        with col_r2:
            spont = dg < 0
            label = "Spontaneous 🟢" if spont else "Non-spontaneous 🔴"
            if abs(dg) < 1:
                label = "Equilibrium ⚠️"
            st.metric("Spontaneity", label)
        with col_r3:
            st.metric("TΔS term", f"{t_g * ds_kj:+.2f} kJ/mol")

        # Spontaneity summary
        if dh_g < 0 and ds_g > 0:
            summary = "**ΔH < 0, ΔS > 0** → Spontaneous at **all** temperatures"
        elif dh_g > 0 and ds_g < 0:
            summary = "**ΔH > 0, ΔS < 0** → Non-spontaneous at **all** temperatures"
        elif dh_g < 0 and ds_g < 0:
            t_crit = dh_g / ds_kj
            summary = f"**ΔH < 0, ΔS < 0** → Spontaneous **below** T = {t_crit:.0f} K"
        else:
            t_crit = dh_g / ds_kj
            summary = f"**ΔH > 0, ΔS > 0** → Spontaneous **above** T = {t_crit:.0f} K"

        st.info(f"💡 {summary}")

    with tab_g2:
        st.markdown("### Spontaneity vs Temperature")
        st.markdown("See how ΔG changes with temperature.")

        col_e1, col_e2 = st.columns(2)
        with col_e1:
            dh_e = st.number_input("ΔH (kJ/mol)", -500.0, 500.0, -100.0, 5.0, key="gibbs_exp_dh")
        with col_e2:
            ds_e = st.number_input("ΔS (J/mol·K)", -300.0, 300.0, 100.0, 5.0, key="gibbs_exp_ds")

        ds_e_kj = ds_e / 1000.0
        temps = np.linspace(50, 1500, 300)
        dg_vals = dh_e - temps * ds_e_kj

        # Find critical temperature if applicable
        if abs(ds_e) > 0.1:
            t_crit = dh_e / ds_e_kj
        else:
            t_crit = None

        fig = go.Figure()
        colors = ["#10b981" if v < 0 else "#ef4444" for v in dg_vals]
        fig.add_trace(go.Scatter(
            x=temps, y=dg_vals, mode="lines",
            line=dict(color="#6366f1", width=3),
            name="ΔG vs T",
            hovertemplate="T = %{x:.0f} K<br>ΔG = %{y:+.2f} kJ/mol<extra></extra>",
        ))

        # Zero line
        fig.add_hline(y=0, line=dict(color="#888", width=1, dash="dash"),
                       annotation_text="Spontaneous ΔG < 0")

        # Critical temperature marker
        if t_crit and 50 <= t_crit <= 1500:
            dg_at_tcrit = dh_e - t_crit * ds_e_kj
            fig.add_trace(go.Scatter(
                x=[t_crit], y=[dg_at_tcrit], mode="markers",
                marker=dict(size=14, color="#f59e0b", symbol="star"),
                name=f"T_crit = {t_crit:.0f} K",
            ))

        # Fill between curve and zero
        dg_pos = [v if v > 0 else 0 for v in dg_vals]
        dg_neg = [v if v < 0 else 0 for v in dg_vals]
        fig.add_trace(go.Scatter(
            x=temps, y=dg_pos, mode="lines",
            fill="tozeroy", fillcolor="rgba(239,68,68,0.1)",
            line=dict(width=0), showlegend=False, hovertemplate="%{y:.1f}",
        ))
        fig.add_trace(go.Scatter(
            x=temps, y=dg_neg, mode="lines",
            fill="tozeroy", fillcolor="rgba(16,185,129,0.1)",
            line=dict(width=0), showlegend=False, hovertemplate="%{y:.1f}",
        ))

        fig.update_layout(
            height=400,
            xaxis=dict(title="Temperature (K)"),
            yaxis=dict(title="ΔG (kJ/mol)"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#ccc",
            hovermode="x unified",
            margin=dict(l=10, r=10, t=10, b=30),
        )
        st.plotly_chart(fig, use_container_width=True)

        if t_crit:
            if ds_e > 0 and dh_e < 0:
                st.success("🟢 Spontaneous at all temperatures (ΔH < 0, ΔS > 0)")
            elif ds_e < 0 and dh_e > 0:
                st.error("🔴 Non-spontaneous at all temperatures (ΔH > 0, ΔS < 0)")
            elif ds_e < 0 and dh_e < 0:
                st.info(f"🟢 Spontaneous below {t_crit:.0f} K | 🔴 Non-spontaneous above")
            else:
                st.info(f"🔴 Non-spontaneous below {t_crit:.0f} K | 🟢 Spontaneous above")

# ================================================================
#                     🔋 ELECTROLYSIS
# ================================================================
elif topic == "Electrolysis":
    st.markdown("## 🔋 Electrolysis — Comparison Table")
    st.markdown("Comparing dilute HCl, NaCl(aq), and concentrated NaCl side by side.")

    rows = [
        ("Cation", "H⁺", "H⁺, Na⁺", "H⁺, Na⁺"),
        ("Anion", "OH⁻, Cl⁻", "OH⁻, Cl⁻", "OH⁻, Cl⁻"),
    ]
    eq_rows = [
        ("Anode Eqn",
         "4OH⁻ → 2H₂O + O₂ + 4e⁻",
         "2Cl⁻ → Cl₂ + 2e⁻",
         "2Cl⁻ → Cl₂ + 2e⁻"),
        ("Overall",
         "2H₂O → 2H₂ + O₂",
         "2Cl⁻ + 2H₂O → H₂ + Cl₂ + 2OH⁻",
         "2Cl⁻ + 2H₂O → H₂ + Cl₂ + 2OH⁻"),
    ]
    obs_rows = [
        ("Products", "H₂, O₂", "H₂, Cl₂, NaOH", "H₂, Cl₂, NaOH"),
        ("Anode obs.",
         "Bubbles of O₂<br>(vol. = ½ H₂)",
         "Bubbles of Cl₂<br>(yellowish-green, vol. = H₂)",
         "Bubbles of Cl₂<br>(yellowish-green, vol. = H₂)"),
        ("Electrolyte",
         "Acid conc. ↑",
         "[NaCl] ↑, pH constant",
         "NaOH forms, pH ↑"),
    ]

    html = """<table style="width:100%;border-collapse:collapse;font-size:14px;">
    <tr style="background:#1a1a2e;">
        <th style="border:1px solid #444;padding:8px 10px;text-align:center;">Electrolyte</th>
        <th style="border:1px solid #444;padding:8px 10px;text-align:center;">Dilute HCl</th>
        <th style="border:1px solid #444;padding:8px 10px;text-align:center;">NaCl (aq)</th>
        <th style="border:1px solid #444;padding:8px 10px;text-align:center;">Conc. NaCl</th>
    </tr>"""

    def _td(v):
        return f'<td style="border:1px solid #444;padding:8px 10px;text-align:center;">{v}</td>'

    def _tr(label, v1, v2, v3):
        return (f'<tr><td style="border:1px solid #444;padding:8px 10px;background:#1a1a2e;font-weight:600;">{label}</td>'
                + _td(v1) + _td(v2) + _td(v3) + "</tr>")

    for r in rows:
        html += _tr(*r)

    html += """<tr>
        <td style="border:1px solid #444;padding:8px 10px;background:#1a1a2e;font-weight:600;">Cathode</td>
        <td colspan="3" style="border:1px solid #444;padding:8px 10px;text-align:center;">
            2H⁺(aq) + 2e⁻ → H₂(g)<br><small>Same for all — bubbles of H₂ gas</small>
        </td>
    </tr>"""

    for r in eq_rows:
        html += _tr(*r)

    for r in obs_rows:
        html += _tr(*r)

    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📊 Electrochemical Series — Order of Discharge")

    anion_html = """<table style="width:100%;border-collapse:collapse;font-size:14px;">
    <tr style="background:#1a1a2e;">
        <th style="border:1px solid #444;padding:8px 10px;text-align:center;">Anion</th>
        <th style="border:1px solid #444;padding:8px 10px;text-align:center;">Order of Discharge</th>
    </tr>
    <tr>
        <td style="border:1px solid #444;padding:8px 10px;text-align:center;font-weight:600;">OH⁻</td>
        <td style="border:1px solid #444;padding:8px 10px;text-align:center;">Usually first</td>
    </tr>
    <tr>
        <td style="border:1px solid #444;padding:8px 10px;text-align:center;font-weight:600;">I⁻</td>
        <td rowspan="3" style="border:1px solid #444;padding:8px 10px;text-align:center;">Discharged first if present<br>in high concentrations</td>
    </tr>
    <tr><td style="border:1px solid #444;padding:8px 10px;text-align:center;font-weight:600;">Br⁻</td></tr>
    <tr><td style="border:1px solid #444;padding:8px 10px;text-align:center;font-weight:600;">Cl⁻</td></tr>
    <tr>
        <td style="border:1px solid #444;padding:8px 10px;text-align:center;font-weight:600;">CO₃²⁻</td>
        <td rowspan="3" style="border:1px solid #444;padding:8px 10px;text-align:center;">Never discharged</td>
    </tr>
    <tr><td style="border:1px solid #444;padding:8px 10px;text-align:center;font-weight:600;">SO₄²⁻</td></tr>
    <tr><td style="border:1px solid #444;padding:8px 10px;text-align:center;font-weight:600;">NO₃⁻</td></tr>
    </table>"""
    st.markdown(anion_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cations = [
        ("K⁺", "Not discharged"),
        ("Na⁺", "Not discharged"),
        ("Ca²⁺", "Not discharged"),
        ("Mg²⁺", "Not discharged"),
        ("Al³⁺", "Not discharged"),
        ("Zn²⁺", "Not discharged"),
        ("Fe²⁺", "Not discharged"),
        ("Pb²⁺", "Not discharged"),
        ("H⁺", "H₂ discharged"),
        ("Cu²⁺", "Metal discharged"),
        ("Ag⁺", "Metal discharged"),
        ("Au⁺", "Metal discharged"),
        ("Pt²⁺", "Metal discharged"),
    ]

    cation_html = """<table style="width:60%;border-collapse:collapse;font-size:14px;margin:0 auto;">
    <tr style="background:#1a1a2e;">
        <th style="border:1px solid #444;padding:8px 10px;text-align:center;">Cation</th>
        <th style="border:1px solid #444;padding:8px 10px;text-align:center;">Discharge Behavior</th>
    </tr>"""
    for ion, behavior in cations:
        bg = "#0f3a2e" if "H₂" in behavior else "#2a1a3e" if "Metal" in behavior else "inherit"
        cation_html += f"""<tr>
            <td style="border:1px solid #444;padding:6px 10px;text-align:center;font-weight:600;">{ion}</td>
            <td style="border:1px solid #444;padding:6px 10px;text-align:center;background:{bg};">{behavior}</td>
        </tr>"""
    cation_html += "</table>"
    st.markdown(cation_html, unsafe_allow_html=True)

    st.caption("Trend: Top = least likely to discharge · Bottom = most likely to discharge")

# ================================================================
#                     🔥 REACTIVITY SERIES
# ================================================================
elif topic == "Reactivity Series":
    st.markdown("## 🔥 Reactivity Series — Metals with Water & Acid")
    st.markdown("Reactivity decreases from top to bottom.")

    html = """<table style="width:100%;border-collapse:collapse;font-size:13px;">
    <tr style="background:#1a1a2e;">
        <th style="border:1px solid #444;padding:8px 6px;text-align:center;">Metal</th>
        <th style="border:1px solid #444;padding:8px 6px;text-align:center;" colspan="2">Cold Water</th>
        <th style="border:1px solid #444;padding:8px 6px;text-align:center;" colspan="2">Steam</th>
        <th style="border:1px solid #444;padding:8px 6px;text-align:center;" colspan="2">Dilute HCl</th>
    </tr>
    <tr style="background:#1a1a2e;">
        <th style="border:1px solid #444;padding:4px 6px;"></th>
        <th style="border:1px solid #444;padding:4px 6px;text-align:center;">Observation</th>
        <th style="border:1px solid #444;padding:4px 6px;text-align:center;">Forms H₂ &</th>
        <th style="border:1px solid #444;padding:4px 6px;text-align:center;">Observation</th>
        <th style="border:1px solid #444;padding:4px 6px;text-align:center;">Forms H₂ &</th>
        <th style="border:1px solid #444;padding:4px 6px;text-align:center;">Observation</th>
        <th style="border:1px solid #444;padding:4px 6px;text-align:center;">Forms H₂ &</th>
    </tr>"""

    metals = [
        ("K", "Reacts explosively", "KOH", "Reacts explosively", "K₂O", "Reacts explosively", "KCl"),
        ("Na", "Reacts violently", "NaOH", "Reacts explosively", "Na₂O", "Reacts explosively", "NaCl"),
        ("Ca", "Reacts readily", "Ca(OH)₂", "Reacts explosively", "CaO", "Reacts violently", "CaCl₂"),
        ("Mg", "Reacts very slowly", "Mg(OH)₂", "Reacts violently with a bright white glow", "MgO", "Reacts rapidly", "MgCl₂"),
        ("Al", "No apparent reaction due to the layer of aluminium oxide", "—", "—", "—", "*Reacts readily", "AlCl₃"),
        ("Zn", "No reaction", "—", "Reacts readily", "ZnO**", "Reacts moderately fast", "ZnCl₂"),
        ("Fe", "No reaction", "—", "Reacts slowly", "Fe₃O₄", "Reacts slowly", "FeCl₂"),
        ("Sn", "No reaction", "—", "No reaction", "—", "Reacts very slowly", "SnCl₂"),
        ("Pb", "No reaction", "—", "No reaction", "—", "***No apparent reaction due to the insoluble layer of lead(II) chloride", "—"),
        ("Cu", "No reaction", "—", "No reaction", "—", "No reaction", "—"),
        ("Ag", "No reaction", "—", "No reaction", "—", "No reaction", "—"),
        ("Au", "No reaction", "—", "No reaction", "—", "No reaction", "—"),
    ]

    def _td(v, span=False):
        s = ' rowspan="2"' if span else ''
        return f'<td{s} style="border:1px solid #444;padding:6px 8px;text-align:center;">{v}</td>'

    for metal, *cols in metals:
        html += f'<tr><td style="border:1px solid #444;padding:6px 8px;text-align:center;font-weight:600;">{metal}</td>'
        for v in cols:
            html += _td(v)
        html += "</tr>"

    html += '</table>'

    st.markdown(html, unsafe_allow_html=True)

    st.markdown("""
    <small>
    * Dilute HCl dissolves the oxide layer, allowing underlying Al to react.<br>
    ** ZnO is yellow when hot and white when cold.<br>
    *** Extremely slow reaction that stops gradually due to the formation of PbCl₂.
    </small>
    """, unsafe_allow_html=True)
# ================================================================
elif topic == "Qualitative Analysis":
    st.markdown("## 📖 Qualitative Analysis — Summary of Tests")
    st.markdown("Reference chart for identifying cations and anions based on reactions with common reagents.")

    col_n, col_a = st.columns([4, 1])
    with col_n:
        st.markdown("### NaOH(aq)")
    with col_a:
        st.markdown("*Excess NaOH*")
    naoh_data = [
        ("Na⁺", "No precipitate", "N/A"),
        ("K⁺", "No precipitate", "N/A"),
        ("NH₄⁺", "NH₃ gas evolved on warming", "N/A"),
        ("Ca²⁺", "White", "Insoluble"),
        ("Zn²⁺", "White", "Soluble"),
        ("Pb²⁺", "White", "Soluble"),
        ("Al³⁺", "White", "Soluble"),
        ("Cu²⁺", "Blue", "Insoluble"),
        ("Fe²⁺", "Green → turns reddish-brown on standing", "N/A"),
        ("Fe³⁺", "Reddish-brown", "Insoluble"),
    ]
    na_cols = st.columns([1, 2, 1])
    na_cols[0].markdown("**Cation**")
    na_cols[1].markdown("**Precipitate with NaOH(aq)**")
    na_cols[2].markdown("**In xs NaOH**")
    for ion, ppt, xs in naoh_data:
        c1, c2, c3 = st.columns([1, 2, 1])
        c1.markdown(f"`{ion}`")
        c2.markdown(ppt)
        c3.markdown(xs)

    st.divider()

    col_nh, col_a2 = st.columns([4, 1])
    with col_nh:
        st.markdown("### NH₃(aq)")
    with col_a2:
        st.markdown("*Excess NH₃*")
    nh3_data = [
        ("Na⁺", "No precipitate", "N/A"),
        ("K⁺", "No precipitate", "N/A"),
        ("NH₄⁺", "No precipitate", "N/A"),
        ("Ca²⁺", "White", "Insoluble"),
        ("Zn²⁺", "White", "Soluble"),
        ("Pb²⁺", "White", "Insoluble"),
        ("Al³⁺", "White", "Insoluble"),
        ("Cu²⁺", "Blue", "Soluble → dark blue solution"),
        ("Fe²⁺", "Green → turns reddish-brown on standing", "Insoluble"),
        ("Fe³⁺", "Reddish-brown", "Insoluble"),
    ]
    nh_cols = st.columns([1, 2, 1])
    nh_cols[0].markdown("**Cation**")
    nh_cols[1].markdown("**Precipitate with NH₃(aq)**")
    nh_cols[2].markdown("**In xs NH₃**")
    for ion, ppt, xs in nh3_data:
        c1, c2, c3 = st.columns([1, 2, 1])
        c1.markdown(f"`{ion}`")
        c2.markdown(ppt)
        c3.markdown(xs)

    st.divider()

    st.markdown("### Dilute Acid (HCl, H₂SO₄)")
    st.markdown("**Effervescence observed?**")
    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown("✅ **Yes** — gas evolved")
        st.markdown("- **H₂** → Metal present")
        st.markdown("- **CO₂** → CO₃²⁻ (carbonate) present")
        st.markdown("- **SO₂** → SO₃²⁻ (sulfite) present")
    with c_b:
        st.markdown("❌ **No** — no effervescence")
        st.markdown("- No reactive metal, carbonate, or sulfite detected")

    st.caption("Source: chemlectures.sg · Page 11 · www.chemlectures.sg")

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with Python · Streamlit · Plotly · NumPy")
