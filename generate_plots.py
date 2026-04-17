# generate_plots.py — Generates all benchmark charts for the report
# Run: python generate_plots.py
# Output: report_charts/ folder with PNG images

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

os.makedirs("report_charts", exist_ok=True)

# ─── Raw benchmark data ───────────────────────────────────────────────────────
LABELS = [
    "u=1k\nt=10k\ne=0",
    "u=1k\nt=10k\ne=2",
    "u=1k\nt=10k\ne=5",
    "u=10k\nt=50k\ne=2",
    "u=50k\nt=100k\ne=5",
]

PG = {
    "Q1": [0.045, 0.043, 0.043, 0.122, 0.191],
    "Q2": [0.036, 0.026, 0.014, 0.039, 0.093],
    "Q3": [0.208, 0.211, 0.206, 4.470, 18.18],
    "Q4": [0.006, 0.019, 0.041, 0.069, 0.212],
}
MG = {
    "Q1": [2.289, 2.128, 2.264, 78.518, 908.626],
    "Q2": [0.025, 0.033, 0.022,  0.119,   0.453],
    "Q3": [0.010, 0.010, 0.010,  0.049,   0.110],
    "Q4": [0.002, 0.011, 0.015,  0.035,   0.165],
}

x = range(len(LABELS))

# ─── Fig 1: Part 1.2 — Q1 & Q3 full comparison (log scale) ──────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Part 1.2 — PostgreSQL vs MongoDB: Query Execution Time (seconds)", fontsize=13)

for ax, q, title in zip(axes, ["Q1","Q3"],
                         ["Q1 – All trips with user & station info",
                          "Q3 – Station trip counts"]):
    ax.plot(x, PG[q], "o-",  color="#2563eb", label="PostgreSQL")
    ax.plot(x, MG[q], "s--", color="#dc2626", label="MongoDB")
    ax.set_title(title, fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels(LABELS, fontsize=8)
    ax.set_ylabel("Time (s)"); ax.legend(); ax.grid(alpha=0.3)
    ax.set_yscale("log")

plt.tight_layout()
plt.savefig("report_charts/fig1_q1_q3_comparison.png", dpi=150)
plt.close()
print("Saved: fig1_q1_q3_comparison.png")

# ─── Fig 2: Part 1.2 — Q2 & Q4 comparison ───────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Part 1.2 — PostgreSQL vs MongoDB: Q2 & Q4 Execution Time", fontsize=13)

for ax, q, title in zip(axes, ["Q2","Q4"],
                         ["Q2 – Users: trip count & avg duration",
                          "Q4 – Trips with at least one ERROR event"]):
    ax.plot(x, PG[q], "o-",  color="#2563eb", label="PostgreSQL")
    ax.plot(x, MG[q], "s--", color="#dc2626", label="MongoDB")
    ax.set_title(title, fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels(LABELS, fontsize=8)
    ax.set_ylabel("Time (s)"); ax.legend(); ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("report_charts/fig2_q2_q4_comparison.png", dpi=150)
plt.close()
print("Saved: fig2_q2_q4_comparison.png")

# ─── Fig 3: Part 1.2 — All 4 queries side-by-side bar chart ─────────────────
fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("Part 1.2 — All Queries: PostgreSQL vs MongoDB (seconds)", fontsize=13)

for ax, q in zip(axes.flatten(), ["Q1","Q2","Q3","Q4"]):
    w = 0.35
    xi = [i - w/2 for i in x]
    xj = [i + w/2 for i in x]
    ax.bar(xi, PG[q], width=w, color="#2563eb", label="PostgreSQL", alpha=0.85)
    ax.bar(xj, MG[q], width=w, color="#dc2626", label="MongoDB",    alpha=0.85)
    ax.set_title(f"{q}", fontsize=11)
    ax.set_xticks(list(x)); ax.set_xticklabels(LABELS, fontsize=7)
    ax.set_ylabel("Time (s)"); ax.legend(fontsize=8); ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("report_charts/fig3_all_queries_bar.png", dpi=150)
plt.close()
print("Saved: fig3_all_queries_bar.png")

# ─── Fig 4: Part 1.4 — Spark Q2 vs PostgreSQL Q2 vs MongoDB Q2 ──────────────
configs  = ["u=1k\nt=10k", "u=10k\nt=50k", "u=50k\nt=100k"]
pg_q2    = [0.036,  0.039,  0.093]
mg_q2    = [0.025,  0.119,  0.453]
spark_q2 = [None,   None,   0.181]   # only measured at largest config

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot([0,1,2], pg_q2, "o-",  color="#2563eb", label="PostgreSQL Q2")
ax.plot([0,1,2], mg_q2, "s--", color="#dc2626", label="MongoDB Q2 (in-DB)")
ax.plot([2],    [0.181], "D",   color="#16a34a", markersize=9, label="Spark Q2 (0.181s)")
ax.set_title("Part 1.4 — Spark Q2 vs In-Database Q2", fontsize=12)
ax.set_xticks([0,1,2]); ax.set_xticklabels(configs)
ax.set_ylabel("Time (s)"); ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("report_charts/fig4_spark_q2_comparison.png", dpi=150)
plt.close()
print("Saved: fig4_spark_q2_comparison.png")

# ─── Fig 5: Part 2.2 — GraphFrames PageRank & CC times ──────────────────────
tasks  = ["PageRank\n(top 3 stations)", "Connected\nComponents"]
times  = [3.84, 9.92]
colors = ["#7c3aed", "#0891b2"]

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(tasks, times, color=colors, alpha=0.85, width=0.4)
for bar, t in zip(bars, times):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f"{t}s", ha="center", fontsize=11, fontweight="bold")
ax.set_title("Part 2.2 — Spark GraphFrames: Execution Time\n(u=50k, t=100k, e=5)", fontsize=12)
ax.set_ylabel("Time (s)"); ax.set_ylim(0, 13); ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("report_charts/fig5_graphframes_times.png", dpi=150)
plt.close()
print("Saved: fig5_graphframes_times.png")

# ─── Fig 6: Part 1.2 — Q3 PostgreSQL scalability (bottleneck highlight) ─────
trip_counts = [10000, 50000, 100000]
pg_q3_scale = [0.208, 4.47, 18.18]
mg_q3_scale = [0.010, 0.049, 0.110]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(trip_counts, pg_q3_scale, "o-",  color="#2563eb", linewidth=2, label="PostgreSQL Q3")
ax.plot(trip_counts, mg_q3_scale, "s--", color="#dc2626", linewidth=2, label="MongoDB Q3")
ax.set_title("Part 1.2 — Q3 Scalability: Station Aggregation", fontsize=12)
ax.set_xlabel("Number of Trips"); ax.set_ylabel("Time (s)")
ax.legend(); ax.grid(alpha=0.3)
ax.fill_between(trip_counts, pg_q3_scale, alpha=0.08, color="#2563eb")
plt.tight_layout()
plt.savefig("report_charts/fig6_q3_scalability.png", dpi=150)
plt.close()
print("Saved: fig6_q3_scalability.png")

print("\nAll charts saved in report_charts/")