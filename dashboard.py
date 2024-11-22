import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dashboard_handel as dh

data = pd.read_csv("registry_check_results.csv")
found_counts = data["found"].value_counts().reset_index()
found_counts.columns = ["found", "count"]

category_counts = dh.dfr1["Category"].value_counts().reset_index()
category_counts.columns = ["Category", "Count"]

subCategory_found_counts_dfr2 = (
    dh.dfr2.groupby(["subCategory", "found"]).size().reset_index(name="count")
)
subCategory_found_counts_pivot_dfr2 = subCategory_found_counts_dfr2.pivot(
    index="subCategory", columns="found", values="count"
).fillna(0)

subCategory_found_counts_dfr3 = (
    dh.dfr3.groupby(["subCategory", "found"]).size().reset_index(name="count")
)
subCategory_found_counts_pivot_dfr3 = subCategory_found_counts_dfr3.pivot(
    index="subCategory", columns="found", values="count"
).fillna(0)

def dynamic_fontsize(scale=1):
    base_size = 18
    return base_size * scale

pie_colors = ["#B33D3D", "#0066CC", "#338B33", "#FF9933"]
doughnut_colors = ["#990033", "#003366", "#336633", "#CC6600"]
bar_chart_colors_dfr2 = ["#8B0000", "#2F4F4F"]
bar_chart_colors_dfr3 = ["#A52A2A", "#556B2F"]

sns.set(style="whitegrid")

def plot_pie_chart():
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        found_counts["count"],
        labels=found_counts["found"],
        autopct="%1.1f%%",
        colors=pie_colors[: len(found_counts)],
    )
    ax.set_title(
        "Detection Rate of paths",
        fontsize=dynamic_fontsize(1.2),
        weight="normal",
        style="italic",
    )
    ax.legend(
        wedges,
        [
            f"{cat} ({val})"
            for cat, val in zip(found_counts["found"], found_counts["count"])
        ],
        title="Legend",
        loc="upper left",
        bbox_to_anchor=(1, 0.8),
        fontsize=dynamic_fontsize(0.8),
    )
    plt.tight_layout(pad=2)
    return fig

def plot_doughnut_chart():
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        category_counts["Count"],
        labels=category_counts["Category"],
        autopct="%1.1f%%",
        startangle=140,
        colors=doughnut_colors[: len(category_counts)],
        wedgeprops=dict(width=0.2),
    )
    ax.set_title(
        "Types of paths available",
        fontsize=dynamic_fontsize(1.2),
        weight="normal",
        style="italic",
    )
    ax.legend(
        wedges,
        [
            f"{cat} ({val})"
            for cat, val in zip(category_counts["Category"], category_counts["Count"])
        ],
        title="Legend",
        loc="upper left",
        bbox_to_anchor=(1, 0.8),
        fontsize=dynamic_fontsize(0.8),
    )
    plt.tight_layout(pad=2)
    return fig

def plot_bar_chart_dfr2():
    fig, ax = plt.subplots()
    subCategory_found_counts_pivot_dfr2.plot(
        kind="bar", ax=ax, color=bar_chart_colors_dfr2, width=0.8
    )
    ax.set_title(
        "HKLM System Categories",
        fontsize=dynamic_fontsize(1.2),
        weight="normal",
        style="italic",
    )
    ax.set_xlabel("Subcategory", fontsize=dynamic_fontsize(0.9))
    ax.set_ylabel("Count", fontsize=dynamic_fontsize(0.9))
    ax.tick_params(axis="both", labelsize=dynamic_fontsize(0.8))
    ax.grid(True, color="gray", linestyle="--", linewidth=0.5, alpha=0.5)
    for p in ax.patches:
        ax.annotate(
            f"{int(p.get_height())}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=dynamic_fontsize(0.8),
            color="black",
            xytext=(0, 5),
            textcoords="offset points",
        )
    plt.tight_layout(pad=2)
    return fig

def plot_bar_chart_dfr3():
    fig, ax = plt.subplots()
    subCategory_found_counts_pivot_dfr3.plot(
        kind="bar", ax=ax, color=bar_chart_colors_dfr3, width=0.8
    )
    ax.set_title(
        "HKLM Software Categories",
        fontsize=dynamic_fontsize(1.2),
        weight="normal",
        style="italic",
    )
    ax.set_xlabel("Subcategory", fontsize=dynamic_fontsize(0.9))
    ax.set_ylabel("Count", fontsize=dynamic_fontsize(0.9))
    ax.tick_params(axis="both", labelsize=dynamic_fontsize(0.8))
    ax.grid(True, color="gray", linestyle="--", linewidth=0.5, alpha=0.5)
    for p in ax.patches:
        ax.annotate(
            f"{int(p.get_height())}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=dynamic_fontsize(0.8),
            color="black",
            xytext=(0, 5),
            textcoords="offset points",
        )
    plt.tight_layout(pad=2)
    return fig