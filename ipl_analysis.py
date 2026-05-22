"""
IPL Cricket Performance Analytics
===================================
Author      : [Your Name]
Tools Used  : Python (Pandas, Matplotlib, Seaborn)
Dataset     : IPL Matches & Deliveries (2008–2023)
Source      : https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020

Objectives:
  1. Which teams win the most matches?
  2. Who are the top run-scorers across seasons?
  3. Which bowlers take the most wickets?
  4. Does toss decision impact match result?
  5. Season-wise run trends

Run:
    pip install pandas matplotlib seaborn
    python ipl_analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ─── CONFIG ───────────────────────────────────────────────────────────────────
MATCHES_CSV     = "data/matches.csv"
DELIVERIES_CSV  = "data/deliveries.csv"
OUTPUT_DIR      = "visualizations/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── STYLE ────────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.dpi": 150,
    "figure.facecolor": "white",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

COLOR_PRIMARY   = "#1a73e8"
COLOR_ACCENT    = "#e84d1a"
COLOR_SUCCESS   = "#2e7d32"
TEAM_COLORS = {
    "Mumbai Indians":               "#005DA0",
    "Chennai Super Kings":          "#F9CD05",
    "Royal Challengers Bangalore":  "#C8102E",
    "Kolkata Knight Riders":        "#3A225D",
    "Sunrisers Hyderabad":          "#F7A721",
    "Delhi Capitals":               "#0078BC",
    "Rajasthan Royals":             "#EA1A85",
    "Punjab Kings":                 "#D71920",
}

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
print("📂 Loading data...")

try:
    matches     = pd.read_csv(MATCHES_CSV)
    deliveries  = pd.read_csv(DELIVERIES_CSV)
    print(f"✅ Matches    : {matches.shape[0]:,} rows | {matches.shape[1]} columns")
    print(f"✅ Deliveries : {deliveries.shape[0]:,} rows | {deliveries.shape[1]} columns")
except FileNotFoundError as e:
    print(f"\n⚠️  {e}")
    print("\n📌 Please download the IPL dataset from Kaggle:")
    print("   https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020")
    print("\n   Place matches.csv and deliveries.csv inside the  data/  folder.")
    print("\n🔁 Running with SAMPLE DEMO DATA for preview...\n")
    matches, deliveries = _generate_sample_data()

# ─── QUICK OVERVIEW ───────────────────────────────────────────────────────────
print("\n── Matches sample ──")
print(matches.head(3).to_string())
print("\n── Deliveries sample ──")
print(deliveries.head(3).to_string())
print(f"\nSeason range : {matches['season'].min()} – {matches['season'].max()}")
print(f"Total matches: {len(matches):,}")
print(f"Total teams  : {matches['team1'].nunique()}")

# ─── 1. MOST WINS BY TEAM ─────────────────────────────────────────────────────
print("\n[1/5] Plotting team win counts...")

wins = matches["winner"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 5))
colors  = [TEAM_COLORS.get(t, COLOR_PRIMARY) for t in wins.index]
bars    = ax.barh(wins.index[::-1], wins.values[::-1], color=colors[::-1], height=0.65)

for bar in bars:
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
            f"{int(bar.get_width())}", va="center", fontsize=9, color="#555")

ax.set_xlabel("Number of Wins")
ax.set_title("Top 10 Teams by Total IPL Wins (2008–2023)", fontsize=13, fontweight="bold", pad=12)
ax.set_xlim(0, wins.values.max() + 20)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}01_team_wins.png")
plt.close()
print("   ✅ Saved: visualizations/01_team_wins.png")

# ─── 2. TOP 10 RUN-SCORERS ────────────────────────────────────────────────────
print("[2/5] Plotting top batters...")

top_batters = (
    deliveries.groupby("batter")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_batters.values, y=top_batters.index, ax=ax,
            palette=sns.color_palette("Blues_r", len(top_batters)))

for bar in ax.patches:
    ax.text(bar.get_width() + 50, bar.get_y() + bar.get_height() / 2,
            f"{int(bar.get_width()):,}", va="center", fontsize=9)

ax.set_xlabel("Total Runs")
ax.set_title("Top 10 IPL Run-Scorers (All Time)", fontsize=13, fontweight="bold", pad=12)
ax.set_xlim(0, top_batters.values.max() + 1000)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}02_top_batters.png")
plt.close()
print("   ✅ Saved: visualizations/02_top_batters.png")

# ─── 3. TOP 10 WICKET-TAKERS ──────────────────────────────────────────────────
print("[3/5] Plotting top bowlers...")

wickets = deliveries[deliveries["dismissal_kind"].notna() &
                      (~deliveries["dismissal_kind"].isin(
                          ["run out", "retired hurt", "obstructing the field"]))]

top_bowlers = (
    wickets.groupby("bowler")["dismissal_kind"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_bowlers.values, y=top_bowlers.index, ax=ax,
            palette=sns.color_palette("Oranges_r", len(top_bowlers)))

for bar in ax.patches:
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
            f"{int(bar.get_width())}", va="center", fontsize=9)

ax.set_xlabel("Total Wickets")
ax.set_title("Top 10 IPL Wicket-Takers (All Time)", fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}03_top_bowlers.png")
plt.close()
print("   ✅ Saved: visualizations/03_top_bowlers.png")

# ─── 4. TOSS DECISION vs MATCH WIN ───────────────────────────────────────────
print("[4/5] Analysing toss impact...")

matches["toss_match_win"] = matches["toss_winner"] == matches["winner"]
toss_analysis = (
    matches.groupby("toss_decision")["toss_match_win"]
    .mean()
    .mul(100)
    .round(1)
    .reset_index()
)
toss_analysis.columns = ["Toss Decision", "Win %"]

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(toss_analysis["Toss Decision"], toss_analysis["Win %"],
              color=[COLOR_PRIMARY, COLOR_ACCENT], width=0.5)

for bar, pct in zip(bars, toss_analysis["Win %"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            f"{pct}%", ha="center", fontsize=11, fontweight="bold")

ax.set_ylabel("Win Percentage (%)")
ax.set_ylim(0, 100)
ax.set_title("Does Winning the Toss Help?", fontsize=13, fontweight="bold", pad=12)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}04_toss_impact.png")
plt.close()
print("   ✅ Saved: visualizations/04_toss_impact.png")

# ─── 5. SEASON-WISE TOTAL RUNS ────────────────────────────────────────────────
print("[5/5] Plotting season run trends...")

season_runs = (
    deliveries
    .merge(matches[["id", "season"]], left_on="match_id", right_on="id")
    .groupby("season")["total_runs"]
    .sum()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(season_runs["season"], season_runs["total_runs"] / 1_000,
        marker="o", linewidth=2.5, markersize=7, color=COLOR_SUCCESS)
ax.fill_between(season_runs["season"], season_runs["total_runs"] / 1_000,
                alpha=0.12, color=COLOR_SUCCESS)

for _, row in season_runs.iterrows():
    ax.annotate(f"{row['total_runs']/1_000:.0f}k",
                (row["season"], row["total_runs"] / 1_000),
                textcoords="offset points", xytext=(0, 8),
                ha="center", fontsize=8, color="#444")

ax.set_xlabel("Season")
ax.set_ylabel("Total Runs (thousands)")
ax.set_title("IPL Season-Wise Total Runs Trend", fontsize=13, fontweight="bold", pad=12)
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}05_season_runs.png")
plt.close()
print("   ✅ Saved: visualizations/05_season_runs.png")

print("\n🎉 All 5 charts saved in  visualizations/  — open them to review!\n")


# ─── SAMPLE DATA GENERATOR (fallback if CSV not found) ────────────────────────
def _generate_sample_data():
    """Generates tiny demo DataFrames so the script runs without real CSVs."""
    import numpy as np
    rng = np.random.default_rng(42)
    teams = list(TEAM_COLORS.keys())
    seasons = list(range(2008, 2024))
    n_matches = 900

    m_team1   = rng.choice(teams, n_matches)
    m_team2   = rng.choice(teams, n_matches)
    m_winner  = rng.choice(teams, n_matches)
    m_toss_w  = rng.choice(teams, n_matches)
    m_toss_d  = rng.choice(["bat", "field"], n_matches)
    m_season  = rng.choice(seasons, n_matches)

    matches = pd.DataFrame({
        "id": range(1, n_matches + 1),
        "season": m_season, "team1": m_team1, "team2": m_team2,
        "toss_winner": m_toss_w, "toss_decision": m_toss_d, "winner": m_winner,
    })

    batters  = [f"Player_{i}" for i in range(50)]
    bowlers  = [f"Bowler_{i}"  for i in range(30)]
    dis_kinds = ["caught", "bowled", "lbw", "run out", None, None, None]
    n_del = 80_000

    deliveries = pd.DataFrame({
        "match_id":       rng.integers(1, n_matches + 1, n_del),
        "batter":         rng.choice(batters, n_del),
        "bowler":         rng.choice(bowlers, n_del),
        "batsman_runs":   rng.integers(0, 7, n_del),
        "total_runs":     rng.integers(0, 7, n_del),
        "dismissal_kind": rng.choice(dis_kinds, n_del),
    })
    return matches, deliveries
