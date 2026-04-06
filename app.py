import streamlit as st
import plotly.graph_objects as go
import math


#import methods
from find_optimal_k_analytical import probability_success, optimal_k
from simulate_distributions import simulate_distribution
from simulate import simulate
from waiting_cost import sim_with_cost, optimal_k_with_cost


st.set_page_config(page_title="Secretary Problem", layout="wide")
st.title("Optimal Stopping Explorer")


st.sidebar.header("Parameters")

mode = st.sidebar.radio("Mode", ["Classic", "Cost Penalty", "Distribution"])

N = st.sidebar.slider("Candidates (N)", 10, 200, 50, 5)
opt = optimal_k(N)
st.sidebar.caption(f"Optimal k* = {opt} ({opt/N*100:.1f}% of N)")

k = st.sidebar.slider("Rejection threshold (k)", 1, N - 1, min(opt, N - 1))

if mode == "Classic":
    trials = st.sidebar.slider("Trials", 500, 10000, value=1000, step = 100)

elif mode == "Cost Penalty":
    cost = st.sidebar.slider("Cost per step", 0.001, 0.02, 0.005, 0.001, format="%.3f")
    trials = st.sidebar.slider("Trials per k", 500, 10000, value=500, step = 100)

elif mode == "Distribution":
    dist = st.sidebar.radio("Distribution", ["uniform", "normal", "pareto", "lognormal"])
    trials = st.sidebar.slider("Trials", 500,10000, value=2000,step = 100)


# ── Classic ───────────────────────────────────────────────────────────────────
if mode == "Classic":
    cur_p = probability_success(N, k)
    opt_p = probability_success(N, opt)

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Your P(success)", f"{cur_p:.4f}")
    c2.metric("Optimal k*", opt)
    c3.metric("P at k*", f"{opt_p:.4f}")

    # Curve
    ks = list(range(1, N))
    ps = [probability_success(N, ki) for ki in ks]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ks, y=ps, mode="lines", name="P(success)"))
    fig.add_vline(x=k, line_dash="dash", line_color="green",
                  annotation_text=f"k={k}", annotation_font_color="green")
    fig.add_vline(x=opt, line_dash="dot", line_color="red",
                  annotation_text=f"k*={opt}", annotation_font_color="red")
    fig.add_hline(y=1/math.e, line_dash="dot", line_color="grey",
                  annotation_text="1/e", annotation_font_color="grey")
    fig.update_layout(title="P(success) vs k", xaxis_title="k", yaxis_title="P(success)")
    st.plotly_chart(fig, use_container_width=True)

    # Monte Carlo
    if st.button("Run simulate()"):
        with st.spinner("Simulating…"):
            sim_p = simulate(N, k, trials)
        st.success(f"simulate(N={N}, k={k}, t={trials}) = **{sim_p:.4f}**")
        st.caption(f"Analytic: {cur_p:.4f}   |   Difference: {abs(sim_p - cur_p):.4f}")


# ── Cost Penalty ──────────────────────────────────────────────────────────────
elif mode == "Cost Penalty":
    st.subheader(f"sim_with_cost — cost={cost:.3f}")

    step   = max(1, N // 40)
    ks_all = list(range(1, N, step))

    prog = st.progress(0, text="Sweeping k values…")
    rewards = []
    for i, ki in enumerate(ks_all):
        rewards.append(sim_with_cost(N, ki, cost, t=trials))
        prog.progress((i + 1) / len(ks_all))
    prog.empty()

    best_k = ks_all[rewards.index(max(rewards))]
    best_r = max(rewards)
    cur_r  = sim_with_cost(N, k, cost, t=trials)

    c1, c2, c3 = st.columns(3)
    c1.metric("Reward at your k", f"{cur_r:.4f}")
    c2.metric("Cost-optimal k*", best_k)
    c3.metric("Best reward", f"{best_r:.4f}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ks_all, y=rewards, mode="lines", name="Net reward"))
    fig.add_vline(x=k, line_dash="dash", line_color="green",
                  annotation_text=f"k={k}", annotation_font_color="green")
    fig.add_vline(x=best_k, line_dash="dot", line_color="red",
                  annotation_text=f"k*={best_k}", annotation_font_color="red")
    fig.add_vline(x=opt, line_dash="dot", line_color="grey",
                  annotation_text=f"classic k*={opt}", annotation_font_color="grey")
    fig.update_layout(title=f"Net reward vs k  (cost={cost:.3f})",
                      xaxis_title="k", yaxis_title="E[net reward]")
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Net reward = hired_value − cost × stopping_time. Higher cost shifts optimal k left.")


# ── Distribution ──────────────────────────────────────────────────────────────
elif mode == "Distribution":
    st.subheader(f"simulate_distribution — {dist}")

    step  = max(1, N // 30)
    ks_sw = list(range(1, N, step))

    prog = st.progress(0, text=f"Sweeping k ({dist})…")
    sim_ps = []
    for i, ki in enumerate(ks_sw):
        sim_ps.append(simulate_distribution(N, ki, dist, trials))
        prog.progress((i + 1) / len(ks_sw))
    prog.empty()

    best_k = ks_sw[sim_ps.index(max(sim_ps))]
    best_p = max(sim_ps)
    cur_sim_p = simulate_distribution(N, k, dist, trials)

    c1, c2, c3 = st.columns(3)
    c1.metric("Simulated P at your k", f"{cur_sim_p:.4f}")
    c2.metric("Best k (simulated)", best_k)
    c3.metric("Best P (simulated)", f"{best_p:.4f}")

    # Only plot the simulated sweep — this is what actually changes with distribution
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ks_sw, y=sim_ps, mode="lines+markers",
                             name=f"simulate_distribution ({dist})"))
    fig.add_vline(x=k, line_dash="dash", line_color="green",
                  annotation_text=f"k={k}", annotation_font_color="green")
    fig.add_vline(x=best_k, line_dash="dot", line_color="red",
                  annotation_text=f"best k={best_k}", annotation_font_color="red")
    fig.update_layout(title=f"P(success) vs k — {dist} distribution",
                      xaxis_title="k", yaxis_title="P(best hired)")
    st.plotly_chart(fig, use_container_width=True)

    # Comparison bar chart across all distributions at the current k
    st.markdown(f"#### All distributions at k={k}")
    all_dists = ["uniform", "normal", "pareto", "lognormal"]
    with st.spinner("Simulating all distributions for comparison…"):
        all_ps = [simulate_distribution(N, k, d, trials) for d in all_dists]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=all_dists, y=all_ps,
                          marker_color=["green" if d == dist else "steelblue" for d in all_dists]))
    fig2.add_hline(y=1/math.e, line_dash="dot", line_color="grey",
                   annotation_text="1/e ≈ 0.368", annotation_font_color="grey")
    fig2.update_layout(title=f"P(success) by distribution at k={k}",
                       xaxis_title="distribution", yaxis_title="P(best hired)")
    st.plotly_chart(fig2, use_container_width=True)