import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="CricScope · Toss Impact",
    page_icon="🪙",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');
html, body, [class*="css"] {
    background-color: #0a0a0f;
    color: #e8e0d0;
    font-family: 'DM Sans', sans-serif;
}
.gold { color: #d4af37; }
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(212,175,55,0.18);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(12px);
}
.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 600;
    color: #d4af37;
    margin-bottom: 0.4rem;
    letter-spacing: 0.04em;
}
.stat-pill {
    display: inline-block;
    background: rgba(212,175,55,0.12);
    border: 1px solid rgba(212,175,55,0.3);
    border-radius: 20px;
    padding: 0.25rem 0.9rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: #d4af37;
    margin: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("matches.csv")
    return df

df = load_data()

st.markdown('<h1 style="font-family:\'Cormorant Garamond\',serif;color:#d4af37;font-size:2.8rem;">🪙 Toss Impact Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#a09880;font-size:1.05rem;">Does winning the toss actually give you an advantage? Let the data decide.</p>', unsafe_allow_html=True)

st.markdown("---")

# --- OVERALL TOSS WIN → MATCH WIN RATE ---
toss_match_win = df[df["toss_winner"] == df["winner"]].shape[0]
total_matches = df.shape[0]
toss_win_rate = round((toss_match_win / total_matches) * 100, 1)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:3rem;color:#d4af37;font-weight:700;">{toss_win_rate}%</div>
        <div style="color:#a09880;font-size:0.9rem;margin-top:0.3rem;">Toss Winners who won the match</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    bat_first = df[df["toss_decision"] == "bat"].shape[0]
    field_first = df[df["toss_decision"] == "field"].shape[0]
    bat_pct = round((bat_first / total_matches) * 100, 1)
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:3rem;color:#d4af37;font-weight:700;">{bat_pct}%</div>
        <div style="color:#a09880;font-size:0.9rem;margin-top:0.3rem;">Chose to Bat First after winning toss</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    field_pct = round((field_first / total_matches) * 100, 1)
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:3rem;color:#d4af37;font-weight:700;">{field_pct}%</div>
        <div style="color:#a09880;font-size:0.9rem;margin-top:0.3rem;">Chose to Field First after winning toss</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- TOSS DECISION WIN RATE ---
st.markdown('<div class="section-title">🏏 Win Rate by Toss Decision</div>', unsafe_allow_html=True)

decision_stats = []
for decision in ["bat", "field"]:
    subset = df[df["toss_decision"] == decision]
    wins = subset[subset["toss_winner"] == subset["winner"]].shape[0]
    total = subset.shape[0]
    decision_stats.append({
        "Decision": "Bat First" if decision == "bat" else "Field First",
        "Win Rate (%)": round((wins / total) * 100, 1),
        "Total Matches": total
    })

decision_df = pd.DataFrame(decision_stats)

fig1 = px.bar(
    decision_df,
    x="Decision",
    y="Win Rate (%)",
    color="Decision",
    color_discrete_map={"Bat First": "#d4af37", "Field First": "#4a9eff"},
    text="Win Rate (%)",
    title="Win Rate: Bat First vs Field First"
)
fig1.update_layout(
    paper_bgcolor="#0a0a0f",
    plot_bgcolor="#0a0a0f",
    font_color="#e8e0d0",
    title_font_color="#d4af37",
    showlegend=False
)
fig1.update_traces(texttemplate="%{text}%", textposition="outside")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# --- TEAM-WISE TOSS WIN RATE ---
st.markdown('<div class="section-title">🏆 Team-wise Toss Advantage</div>', unsafe_allow_html=True)

teams = df["toss_winner"].value_counts().index.tolist()
team_stats = []
for team in teams:
    toss_wins = df[df["toss_winner"] == team].shape[0]
    match_wins_after_toss = df[(df["toss_winner"] == team) & (df["winner"] == team)].shape[0]
    if toss_wins >= 10:
        team_stats.append({
            "Team": team,
            "Toss Win → Match Win (%)": round((match_wins_after_toss / toss_wins) * 100, 1),
            "Toss Wins": toss_wins
        })

team_df = pd.DataFrame(team_stats).sort_values("Toss Win → Match Win (%)", ascending=True)

fig2 = px.bar(
    team_df,
    x="Toss Win → Match Win (%)",
    y="Team",
    orientation="h",
    text="Toss Win → Match Win (%)",
    title="Which teams benefit most from winning the toss?",
    color="Toss Win → Match Win (%)",
    color_continuous_scale=[[0, "#1a1a2e"], [0.5, "#d4af37"], [1, "#ffd700"]]
)
fig2.update_layout(
    paper_bgcolor="#0a0a0f",
    plot_bgcolor="#0a0a0f",
    font_color="#e8e0d0",
    title_font_color="#d4af37",
    coloraxis_showscale=False,
    height=500
)
fig2.update_traces(texttemplate="%{text}%", textposition="outside")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# --- VENUE-WISE TOSS ADVANTAGE ---
st.markdown('<div class="section-title">🏟️ Venue-wise Toss Advantage</div>', unsafe_allow_html=True)

venue_stats = []
for venue in df["venue"].value_counts().index.tolist():
    subset = df[df["venue"] == venue]
    if subset.shape[0] >= 8:
        wins = subset[subset["toss_winner"] == subset["winner"]].shape[0]
        venue_stats.append({
            "Venue": venue,
            "Toss Win Rate (%)": round((wins / subset.shape[0]) * 100, 1),
            "Matches": subset.shape[0]
        })

venue_df = pd.DataFrame(venue_stats).sort_values("Toss Win Rate (%)", ascending=False).head(15)

fig3 = px.bar(
    venue_df,
    x="Toss Win Rate (%)",
    y="Venue",
    orientation="h",
    text="Toss Win Rate (%)",
    title="Top 15 Venues: Toss Win → Match Win Rate",
    color="Toss Win Rate (%)",
    color_continuous_scale=[[0, "#1a1a2e"], [0.5, "#d4af37"], [1, "#ffd700"]]
)
fig3.update_layout(
    paper_bgcolor="#0a0a0f",
    plot_bgcolor="#0a0a0f",
    font_color="#e8e0d0",
    title_font_color="#d4af37",
    coloraxis_showscale=False,
    height=500
)
fig3.update_traces(texttemplate="%{text}%", textposition="outside")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --- SEASON-WISE TOSS IMPACT ---
st.markdown('<div class="section-title">📅 Season-wise Toss Impact</div>', unsafe_allow_html=True)

season_stats = []
for season in sorted(df["season"].unique()):
    subset = df[df["season"] == season]
    wins = subset[subset["toss_winner"] == subset["winner"]].shape[0]
    season_stats.append({
        "Season": str(season),
        "Toss Win Rate (%)": round((wins / subset.shape[0]) * 100, 1)
    })

season_df = pd.DataFrame(season_stats)

fig4 = px.line(
    season_df,
    x="Season",
    y="Toss Win Rate (%)",
    title="Has toss advantage changed over the years?",
    markers=True,
    line_shape="spline"
)
fig4.update_layout(
    paper_bgcolor="#0a0a0f",
    plot_bgcolor="#0a0a0f",
    font_color="#e8e0d0",
    title_font_color="#d4af37"
)
fig4.update_traces(line_color="#d4af37", marker_color="#ffd700", marker_size=8)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
<div class="glass-card" style="margin-top:1rem;">
    <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:#d4af37;margin-bottom:0.5rem;">📊 Key Takeaways</div>
    <ul style="color:#a09880;line-height:1.9;">
        <li>Winning the toss gives a <strong style="color:#d4af37;">slight but not decisive</strong> advantage overall.</li>
        <li>Teams increasingly prefer to <strong style="color:#d4af37;">field first</strong> in modern IPL seasons.</li>
        <li>Toss advantage varies significantly <strong style="color:#d4af37;">by venue</strong> — some grounds heavily favour chasing.</li>
        <li>Certain teams extract <strong style="color:#d4af37;">more value</strong> from winning the toss than others.</li>
    </ul>
</div>
""", unsafe_allow_html=True)