import re
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

file = "regionalgrossvalueaddedbalancedperheadandincomecomponents.xlsx"
data = pd.read_excel(file, sheet_name="Table 3", header=1)

# Select the broad UK regions and nations.
regions = data[data["ITL"].astype(str).str.strip() == "ITL1"].copy()

# Find year columns and select the latest year with data.
years = []
for column in data.columns:
    match = re.fullmatch(r"((?:19|20)\d{2})(?:\.0)?", str(column))
    if match:
        years.append((int(match.group(1)), column))

years.sort(reverse=True)
for year, column in years:
    values = pd.to_numeric(regions[column], errors="coerce")
    if values.notna().any():
        regions["value"] = values
        break
else:
    raise ValueError("No year columns with regional data were found.")

regions = regions.dropna(subset=["value"])
regions = regions.sort_values("value")

fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

bars = ax.barh(regions["Region name"], regions["value"], color="#28758c")
ax.axvline(100, color="#d17b37", linestyle="--", linewidth=1.5,
           label="UK benchmark = 100")

ax.bar_label(bars, fmt="%.1f", padding=4, fontsize=9)
ax.set_xlim(0, regions["value"].max() * 1.18)
ax.set_xlabel("GVA per head index (UK less Extra-Regio = 100)")
ax.set_title(f"Regional economic output per person, {year}",
             loc="left", fontsize=17, fontweight="bold", pad=18)
ax.legend(frameon=False, loc="lower right")
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", alpha=0.2)
ax.set_axisbelow(True)

fig.text(0.01, 0.01, "Source: Office for National Statistics · Table 3",
         fontsize=9, color="#555555")
plt.tight_layout(rect=(0, 0.04, 1, 1))

output = "regional_gva_chart.png"
plt.savefig(output, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Chart saved: {output}")
subprocess.run(["open", output], check=True)
