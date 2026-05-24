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

    tab_bh1, tab_bh2, tab_bh3 = st.tabs(["📊 Born-Haber Cycle", "🧮 Born-Landé", "📝 Step Details"])

    with tab_bh1:
        st.markdown(f"**Born-Haber Cycle for {data['formula']}**")

        # Build cycle steps
        steps = []
        if data["formula"] == "CaCl₂":
            steps = [
                ("ΔH_atom(M)", data["dh_atom_M"], "#10b981", f"M(s) → M(g)"),
                ("IE", data["ie"], "#f59e0b", f"M(g) → M{{z+}}(g) + ze⁻"),
                ("2 × ΔH_atom(X)", 2 * data["dh_atom_X"], "#3b82f6", f"2X₂ → 2X(g)"),
                ("2 × EA", 2 * data["ea"], "#ef4444", f"2X(g) + 2e⁻ → 2X⁻(g)"),
                ("LE (calc)", -le_calc, "#8b5cf6", f"M{{z+}}(g) + 2X⁻(g) → MX₂(s)"),
            ]
        elif data["formula"] == "Na₂O":
            steps = [
                ("2 × ΔH_atom(M)", 2 * data["dh_atom_M"], "#10b981", f"2Na(s) → 2Na(g)"),
                ("2 × IE", 2 * data["ie"], "#f59e0b", f"2Na(g) → 2Na⁺(g) + 2e⁻"),
                ("ΔH_atom(X)", data["dh_atom_X"], "#3b82f6", f"½O₂ → O(g)"),
                ("EA (O → O²⁻)", data["ea"], "#ef4444", f"O(g) + 2e⁻ → O²⁻(g)"),
                ("LE (calc)", -le_calc, "#8b5cf6", f"2Na⁺(g) + O²⁻(g) → Na₂O(s)"),
            ]
        else:
            steps = [
                ("ΔH_atom(M)", data["dh_atom_M"], "#10b981", f"M(s) → M(g)"),
                ("IE (total)", data["ie"], "#f59e0b", f"M(g) → M{{z+}}(g) + ze⁻"),
                ("ΔH_atom(X)", data["dh_atom_X"], "#3b82f6", f"½X₂ → X(g)"),
                ("EA", data["ea"], "#ef4444", f"X(g) + e⁻ → X⁻(g)"),
                ("LE (calc)", -le_calc, "#8b5cf6", f"M{{z+}}(g) + X⁻(g) → MX(s)"),
            ]

        # Energy level diagram
        energy_levels = [0]
        level_labels = ["Elements (standard states)"]
        level_colors = ["#6366f1"]
        cumulative = 0
        for name, val, color, _ in steps:
            cumulative += val
            energy_levels.append(cumulative)
            level_labels.append(name)
            level_colors.append(color)

        # Add final ΔH_f
        energy_levels.append(data["dh_f"])
        level_labels.append(f"ΔH_f = {data['dh_f']:+.0f}")
        level_colors.append("#10b981" if data["dh_f"] < 0 else "#ef4444")

        fig = go.Figure()
        y_pos = list(range(len(energy_levels)))
        fig.add_trace(go.Scatter(
            x=energy_levels, y=y_pos, mode="lines+markers",
            marker=dict(size=10, color=level_colors),
            line=dict(color="#555", width=2, dash="dot"),
            text=level_labels,
            hovertemplate="%{text}<br>%{x:+.0f} kJ/mol<extra></extra>",
            showlegend=False,
        ))

        for i in range(len(energy_levels) - 1):
            mid_y = (y_pos[i] + y_pos[i + 1]) / 2
            diff = energy_levels[i + 1] - energy_levels[i]
            fig.add_annotation(x=energy_levels[i] + diff / 2, y=mid_y,
                               text=f"{diff:+.0f}",
                               showarrow=False, font=dict(size=11, color="#aaa"))

        fig.update_layout(
            height=400,
            xaxis=dict(title="Enthalpy (kJ/mol)"),
            yaxis=dict(visible=False),
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

    with tab_bh2:
        st.markdown("### Born-Landé Equation")
        st.latex(r"U = -\frac{N_A A z^+ z^- e^2}{4\pi\varepsilon_0 r_0}\left(1 - \frac{1}{n}\right)")

        st.markdown("Adjust parameters to see how lattice energy changes:")
        col_l1, col_l2, col_l3 = st.columns(3)
        with col_l1:
            adj_z = st.slider("Ionic charge (z⁺ = z⁻)", 1, 3, z, key="bl_z")
        with col_l2:
            adj_r = st.slider("Interionic distance r₀ (pm)", 50, 400, int(r0 * 1e12) if r0 * 1e12 < 400 else 250,
                              5, key="bl_r")
        with col_l3:
            adj_n = st.slider("Born exponent (n)", 5, 12, n, key="bl_n")

        adj_r_m = adj_r * 1e-12
        U_adj = -(N_A * A * adj_z * adj_z * e**2) / (4 * math.pi * eps0 * adj_r_m) * (1 - 1/adj_n) / 1000

        st.metric("Adjusted Lattice Energy", f"{U_adj:+.0f} kJ/mol")

        if adj_z != z or adj_r != r0 * 1e12 or adj_n != n:
            delta = U_adj - U
            st.info(f"💡 Change from default: {delta:+.0f} kJ/mol")

        st.markdown("""
        **Factors affecting lattice energy:**
        - **Higher ionic charge** → much more exothermic (stronger attraction)
        - **Smaller ionic radius** → more exothermic (ions closer together)
        - **Higher Born exponent** → slightly less exothermic
        """)

    with tab_bh3:
        st.markdown(f"### Born-Haber Cycle Steps — {data['formula']}")
        for name, val, color, desc in steps:
            st.markdown(f"""<div style="background:{color}22;border-left:4px solid {color};
                        padding:8px 12px;border-radius:6px;margin:6px 0;">
                        <b style="color:{color}">{name}</b>: {val:+.0f} kJ/mol<br>
                        <span style="color:#aaa;font-size:0.9em">{desc}</span>
                        </div>""", unsafe_allow_html=True)

        total = sum(v for _, v, _, _ in steps)
        st.markdown(f"""<div style="background:#1a1d2a;padding:10px 12px;border-radius:6px;margin-top:10px;">
            <b>Sum of steps:</b> {total:+.0f} kJ/mol<br>
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

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with Python · Streamlit · Plotly · NumPy")
