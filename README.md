# 🔬 ClustaSplit

**Cluster-aware ARFF dataset splitter for QSAR model development**

ClustaSplit is a Streamlit web application that takes clustered WEKA ARFF files and automatically splits compounds into proportional **Training**, **Prediction**, and **External** sets — respecting cluster boundaries to ensure unbiased, reproducible machine learning workflows.

---

## ✨ Features

- **Cluster-proportional splitting** — each cluster is split independently so that every cluster is represented in all three sets
- **Reproducible splits** — fixed random seed (`random_state=42`) ensures identical results on every run
- **Dual-dataset support** — upload Active and Inactive compound files simultaneously
- **Live summary tables** — per-cluster breakdown with Training / Prediction / External counts
- **Combined dataset output** — merges Active + Inactive into a single set per split
- **One-click ARFF downloads** — exports valid WEKA ARFF files preserving the original header and `@relation` name
- **Summary CSV export** — download a combined breakdown as a CSV file

---

## 📐 Split Ratios

| Set | Ratio | Description |
|---|---|---|
| Training | 65% | Used to build the QSAR model |
| Prediction | 25% | Used for internal validation |
| External | 10% | Held-out set for independent evaluation |

Allocation is done per cluster using `round()`, with any remainder assigned to External.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/clustasplit.git
cd clustasplit

# Install dependencies
pip install streamlit pandas numpy
```

### Run the App

```bash
streamlit run clustasplit.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 📂 Input Format

ClustaSplit accepts **WEKA ARFF** files (`.arff` or `.txt`).

The file must contain:
- A valid `@relation` declaration
- One or more `@attribute` declarations
- A `@data` section with comma-separated rows
- **A column whose name contains `cluster`** (case-insensitive) — this is used to group compounds before splitting

Example header:

```
@relation my_dataset

@attribute MolWeight NUMERIC
@attribute LogP NUMERIC
@attribute cluster {0,1,2,3}

@data
312.4,2.1,0
...
```

---

## 🖥️ Usage

1. **Upload Active ARFF** — drag and drop or browse for your active compounds file
2. **Upload Inactive ARFF** *(optional)* — do the same for inactive compounds
3. ClustaSplit instantly displays:
   - Per-cluster split table for each dataset
   - Pill summary showing total Training / Prediction / External counts
4. **Download split files** — three ARFF files per dataset (training, prediction, external)
5. **Download combined files** — three merged ARFF files combining Active + Inactive
6. **Download summary CSV** — a tabular overview of the full split

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| Python 3.x | Core language |
| Streamlit | Web UI framework |
| Pandas | DataFrame manipulation and CSV export |
| NumPy | Numerical utilities |
| `re` | ARFF CSV-aware line parsing |
| `io` | In-memory string buffers for downloads |
| WEKA ARFF | Input/output file format |
| Google Fonts | UI typography (Plus Jakarta Sans, JetBrains Mono) |

---

## 📁 Project Structure

```
clustasplit/
├── clustasplit.py   # Main application (single-file Streamlit app)
└── README.md
```

---

## ⚙️ Core Functions

| Function | Description |
|---|---|
| `parse_weka_arff(text)` | Parses raw ARFF text into a Pandas DataFrame; detects the cluster column |
| `allocate_splits(n)` | Computes Training / Prediction / External counts for a group of `n` compounds |
| `split_dataframe(df, cluster_col)` | Splits a DataFrame per cluster and concatenates results |
| `df_to_arff(df, relation, orig_text)` | Serialises a DataFrame back to a valid ARFF string |
| `build_cluster_table(df, cluster_col)` | Builds a per-cluster summary table for display |
| `render_section(label, file, acc_class)` | Renders the full upload → parse → display → download workflow for one dataset |

---

## 📄 License

© 2024 Md. Nabiul Hoque. All rights reserved. Unauthorized reproduction or distribution is prohibited.
