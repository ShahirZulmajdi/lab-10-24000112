import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Lab 10 | Data Story", layout="wide")

# --- Data (fictional practice values) ---
# Changed one rating: Python 3.0 -> 2.2, so Python is now the lowest-rated skill
skills = ["Data storytelling", "Python", "Chart selection",
          "Color and labels", "Data cleaning"]
ratings = [2.4, 2.2, 3.2, 3.7, 4.1]
df = pd.DataFrame({"Skill": skills, "Average rating": ratings})

# Sort so the lowest rating sits at the top (position as a highlight)
df = df.sort_values("Average rating").reset_index(drop=True)
low_skill = df.loc[0, "Skill"]
low_value = df.loc[0, "Average rating"]

# --- Reframed story for a different audience ---
audience = st.sidebar.radio("Audience", ["Workshop instructor", "Department manager", "Students"])

stories = {
    "Workshop instructor": (
        f"Start Your Next Workshop With {low_skill}",
        f"Takeaway: {low_skill} has the lowest average self-rating, so plan the first session around it."),
    "Department manager": (
        f"Fund Extra Support for {low_skill}",
        f"Takeaway: {low_skill} is the weakest skill, so it gives the most value for training resources."),
    "Students": (
        "Plan a Workshop Around Students' Needs",
        f"Takeaway: {low_skill} is the main area for support."),
}
page_title, takeaway = stories[audience]

st.title(page_title)
st.write(f"Audience: {audience.lower()}.")
st.write(takeaway)

# --- Chart ---
fig, ax = plt.subplots(figsize=(8, 4.5))
bar_colors = ["#E07A3F" if s == low_skill else "#B0B7C3" for s in df["Skill"]]
bars = ax.barh(df["Skill"], df["Average rating"], color=bar_colors)

ax.set_xlim(0, 5)
ax.set_xticks(range(0, 6))
ax.set_xlabel("Average self-rating (1 = beginner, 5 = confident)")
ax.set_title(f"{low_skill} received the lowest average rating", loc="left")
ax.invert_yaxis()

# Removed detail: gridlines and extra spines (value labels already give exact numbers)
for side in ["top", "right", "bottom"]:
    ax.spines[side].set_visible(False)
ax.tick_params(axis="x", length=0)

for bar, value in zip(bars, df["Average rating"]):
    ax.text(value + 0.05, bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}", va="center")

# Text annotation highlight on the lowest bar
ax.annotate("Lowest: focus here first",
            xy=(low_value + 0.35, 0), xytext=(low_value + 1.1, 0),
            va="center", color="#E07A3F", fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="#E07A3F"))

fig.tight_layout()
st.pyplot(fig, clear_figure=True)
# Revised explanatory label: says what each bar represents
st.caption("Fictional practice values. Each bar is the average self-rating for one skill "
           "(1-5 scale), not an individual student's score.")
