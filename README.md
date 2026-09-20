# MSCS 634 – Lab 1: Data Visualization, Preprocessing, and Statistical Analysis

**Student:** Aashish Shrestha
**Course:** Big Data and Data Mining MSCS-634-M50

This repository contains my work for Lab 1. The goal of the lab was to take a dataset all the way
from raw form to something clean and analysis-ready, using data visualization, data preprocessing,
and basic statistical analysis inside a Jupyter Notebook.

## Purpose of the lab

The lab is meant to practice the everyday steps of working with real data:

- loading a dataset into Pandas and getting a feel for it,
- exploring it visually to spot patterns and problems,
- cleaning it up (missing values, outliers, reducing and rescaling it), and
- summarising it with descriptive statistics and correlations.

## About the dataset

Instead of downloading an existing file, I generated my own retail **sales dataset**
(`sales_data.csv`) so that the analysis would be original and so I could control exactly what
issues it contained. The script that builds it is included as `generate_data.py`.

The dataset has 600 order records and 12 columns – a mix of categorical fields (`Region`,
`Product_Category`, `Product_Name`, `Sales_Rep`), numeric fields (`Units_Sold`, `Unit_Price`,
`Discount_Percent`, `Customer_Rating`, `Total_Sales`, `Shipping_Cost`), and a date (`Order_Date`).
I deliberately left some values missing in `Region`, `Discount_Percent`, and `Customer_Rating`, and
planted a handful of extreme orders so the outlier step would have something real to catch.

## What the notebook does

`MSCS_634_Lab_1.ipynb` is organised into the four required steps as Mention in Lab Assignment step by step:

1. **Data Collection** – load the CSV and preview it with `.head()`.
2. **Data Visualization** – six charts (scatter, line, bar, histogram, box, pie), each with a written insight.
3. **Data Preprocessing** – handle missing values, detect/remove outliers with the IQR method, reduce the data (sampling + dropping columns), and scale/discretize.
4. **Statistical Analysis** – `.info()`/`.describe()`, central tendency, dispersion, and a correlation matrix.

## Key insights

**From the visualizations**

- Total sales rise as unit price goes up, but a small group of points sit far from the rest – the first visible sign of outliers.
- Monthly sales over 2023–2024 bounce around rather than climbing steadily; the spikes matched months that held a few very large orders.
- Revenue is not shared evenly across product categories – one category clearly pulls in the most.
- `Units_Sold` is heavily right-skewed: most orders are small (roughly 1–40 units) with a long tail from a few oversized orders.
- Orders are split fairly evenly across the five regions, with no single region dominating.

**From the statistics**

- Using the IQR rule on `Total_Sales`, **48 orders** were flagged as outliers and removed, taking the dataset from **600 → 552 rows**.
- In the correlation matrix, `Total_Sales` is most related to `Unit_Price` (≈ 0.64) and `Units_Sold` (≈ 0.39), which makes sense since total sales are derived from them. `Discount_Percent` has a small negative relationship with sales, and `Customer_Rating` is basically independent of the other numbers.

## Challenges and decisions

- **Choosing fill strategies per column.** I matched the method to the column type: the mean for the continuous `Customer_Rating`, and the mode for the discrete `Discount_Percent` and the categorical `Region`. I also showed forward-fill, backward-fill, and row-dropping on copies so the alternatives are visible without changing the main data.
- **Which column to run IQR on.** I used `Total_Sales` because it reflects both kinds of extreme values I introduced (very high quantities and very high prices), so one column caught both.
- **Discretization.** I used `qcut` to split `Total_Sales` into Low / Medium / High tiers so the three groups come out roughly balanced instead of lopsided.
- **Library version quirk.** On the newer Pandas version, resampling by month uses `"ME"` (month-end) instead of the older `"M"`, which I switched to after a deprecation warning.
- **Keeping the work original.** Building my own dataset was a deliberate choice to avoid any plagiarism and to guarantee the notebook has real missing values and outliers to work through.

## Repository structure

```
MSCS_634_Lab_1/
├── MSCS_634_Lab_1.ipynb     # the main notebook (with outputs)
├── sales_data.csv           # the self-created dataset
├── generate_data.py         # script used to create the dataset
├── README.md                 # current file
└── screenshots/             # exported charts + suggested screenshots
```

## How to run

1. Make sure Python has `pandas`, `numpy`, `matplotlib`, and `seaborn` installed or can load the file in Gooogle colab with Dataset and execute it.
2. Open `MSCS_634_Lab_1.ipynb` in Jupyter Notebook or JupyterLab.

## A note on the screenshots

The notebook is submitted with all cell outputs already saved, and the charts are exported into the
`screenshots/` folder. For the assignment's required screenshots, run the notebook yourself and
capture the relevant cells.
