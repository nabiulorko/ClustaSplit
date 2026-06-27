import streamlit as st
import pandas as pd
import numpy as np
import io
import re
from collections import defaultdict

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ClustaSplit",
    page_icon="🔬",
    layout="wide",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ── Page background ── */
.stApp {
    background: linear-gradient(160deg, #f8f6ff 0%, #eef4ff 35%, #e8f9f5 70%, #fef6ff 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f3f0ff 100%);
    border-right: 1px solid #e5e0ff;
}

/* ════════════════════════════════════
   HERO HEADER
════════════════════════════════════ */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(125deg, #7c3aed 0%, #4f8ef7 45%, #06b6d4 80%, #10b981 100%);
    border-radius: 24px;
    padding: 42px 44px 36px;
    margin-bottom: 32px;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 40%;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    color: rgba(255,255,255,0.95);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.25);
    margin-bottom: 16px;
}
.hero-title {
    font-size: 46px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
    margin: 0 0 6px 0;
    line-height: 1.05;
    text-shadow: 0 2px 20px rgba(0,0,0,0.12);
}
.hero-title span {
    background: linear-gradient(90deg, #ffffff, rgba(255,255,255,0.75));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 15.5px;
    color: rgba(255,255,255,0.82);
    font-weight: 400;
    margin: 0 0 22px 0;
    line-height: 1.5;
    max-width: 600px;
}
.hero-rule {
    height: 1px;
    background: rgba(255,255,255,0.22);
    border: none;
    margin: 0 0 18px 0;
}
.hero-desc {
    font-size: 13.5px;
    color: rgba(255,255,255,0.75);
    line-height: 1.65;
    margin: 0;
    max-width: 680px;
}
.hero-desc strong { color: rgba(255,255,255,0.95); font-weight: 600; }

/* ════════════════════════════════════
   UPLOAD ZONE
════════════════════════════════════ */
.upload-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #5b5f8a;
    margin-bottom: 8px;
}
.upload-dot {
    width: 9px; height: 9px;
    border-radius: 50%;
    display: inline-block;
}
.dot-active   { background: linear-gradient(135deg, #4f8ef7, #7c3aed); }
.dot-inactive { background: linear-gradient(135deg, #f97316, #ef4444); }

/* ════════════════════════════════════
   SECTION HEADER
════════════════════════════════════ */
.sec-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 11.5px;
    font-weight: 800;
    color: #4b5380;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    padding-bottom: 12px;
    border-bottom: 2px solid #e8ecff;
    margin-bottom: 20px;
}
.sec-accent {
    width: 4px; height: 18px;
    border-radius: 4px;
}
.acc-blue  { background: linear-gradient(180deg, #4f8ef7, #7c3aed); }
.acc-orange{ background: linear-gradient(180deg, #f97316, #ef4444); }
.acc-green { background: linear-gradient(180deg, #10b981, #06b6d4); }

/* ════════════════════════════════════
   PILLS
════════════════════════════════════ */
.pill-row { display: flex; gap: 10px; flex-wrap: wrap; margin: 14px 0 6px; }
.pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 30px;
    font-size: 12.5px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    border: 1.5px solid transparent;
}
.pill-train {
    background: linear-gradient(white,white) padding-box,
                linear-gradient(90deg,#4f8ef7,#7c3aed) border-box;
    color: #3b5fc7;
}
.pill-pred {
    background: linear-gradient(white,white) padding-box,
                linear-gradient(90deg,#f97316,#ef4444) border-box;
    color: #c2410c;
}
.pill-ext {
    background: linear-gradient(white,white) padding-box,
                linear-gradient(90deg,#10b981,#06b6d4) border-box;
    color: #047857;
}
.pill-dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }
.pd-train { background: #4f8ef7; }
.pd-pred  { background: #f97316; }
.pd-ext   { background: #10b981; }

/* ════════════════════════════════════
   SUMMARY CARDS
════════════════════════════════════ */
.summary-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 16px 0 8px;
}
.s-card {
    border-radius: 18px;
    padding: 22px 20px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.s-card::before {
    content: '';
    position: absolute;
    bottom: -20px; right: -20px;
    width: 80px; height: 80px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
}
.sc-total  { background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%); }
.sc-train  { background: linear-gradient(135deg, #1d4ed8 0%, #4f8ef7 100%); }
.sc-pred   { background: linear-gradient(135deg, #c2410c 0%, #f97316 100%); }
.sc-ext    { background: linear-gradient(135deg, #047857 0%, #10b981 100%); }

.s-card .sc-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.65);
    margin-bottom: 8px;
}
.s-card .sc-value {
    font-size: 34px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 4px;
}
.s-card .sc-pct {
    font-size: 12px;
    color: rgba(255,255,255,0.5);
    font-weight: 500;
}

/* ════════════════════════════════════
   THIN DIVIDER
════════════════════════════════════ */
.thin-div {
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #c4b5fd 30%, #93c5fd 70%, transparent 100%);
    margin: 30px 0;
    border: none;
}

/* ════════════════════════════════════
   DOWNLOAD LABEL
════════════════════════════════════ */
.dl-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #6b7280;
    margin: 20px 0 8px;
}

/* ════════════════════════════════════
   FOOTER
════════════════════════════════════ */
.footer-wrap {
    margin-top: 52px;
    border-radius: 22px;
    background: linear-gradient(135deg, #fafaff 0%, #f0f4ff 50%, #f0fdf8 100%);
    border: 1.5px solid #e0e7ff;
    overflow: hidden;
}
.footer-top {
    padding: 28px 34px 22px;
    border-bottom: 1px solid #e8eeff;
    display: flex;
    align-items: center;
    gap: 16px;
}
.footer-icon {
    width: 46px; height: 46px;
    border-radius: 14px;
    background: linear-gradient(135deg, #7c3aed, #4f8ef7);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}
.footer-author {
    font-size: 18px;
    font-weight: 800;
    color: #1e2140;
    line-height: 1.2;
}
.footer-app {
    font-size: 12px;
    color: #8b92b5;
    font-weight: 500;
    margin-top: 2px;
}
.footer-body {
    padding: 22px 34px 26px;
}
.footer-tech-title {
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8b92b5;
    margin-bottom: 14px;
}
.tech-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 22px;
}
.tech-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 13px;
    border-radius: 30px;
    font-size: 12.5px;
    font-weight: 600;
    border: 1.5px solid;
}
.tp-python  { background: #fef9ec; color: #92400e; border-color: #fcd34d; }
.tp-st      { background: #fff0f0; color: #9b1c1c; border-color: #fca5a5; }
.tp-pandas  { background: #eff6ff; color: #1e40af; border-color: #93c5fd; }
.tp-numpy   { background: #f0fdf4; color: #14532d; border-color: #6ee7b7; }
.tp-regex   { background: #fdf4ff; color: #6b21a8; border-color: #d8b4fe; }
.tp-io      { background: #f0f9ff; color: #0c4a6e; border-color: #7dd3fc; }
.tp-weka    { background: #fff7ed; color: #7c2d12; border-color: #fdba74; }
.tp-fonts   { background: #fafaf9; color: #292524; border-color: #d6d3d1; }

.footer-rights {
    padding: 14px 34px;
    background: linear-gradient(90deg, #f5f3ff, #eff6ff);
    border-top: 1px solid #e8eeff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
}
.rights-text {
    font-size: 12px;
    color: #8b92b5;
    font-weight: 500;
}
.rights-copy {
    font-size: 12px;
    font-weight: 700;
    color: #6d5bd0;
}
</style>
""", unsafe_allow_html=True)


# ── WEKA parser ────────────────────────────────────────────────────────────────
def parse_weka_arff(text: str):
    lines = text.splitlines()
    attrs, data_lines = [], []
    in_data = False

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        low = stripped.lower()
        if low.startswith("@relation"):
            pass
        elif low.startswith("@attribute"):
            parts = stripped.split(None, 2)
            if len(parts) >= 2:
                attrs.append(parts[1])
        elif low.startswith("@data"):
            in_data = True
        elif in_data:
            data_lines.append(stripped)

    if not data_lines:
        return None, None, "No @data section found."

    rows = []
    for dl in data_lines:
        parts = re.split(r",(?=(?:[^'\"]*['\"][^'\"]*['\"])*[^'\"]*$)", dl)
        parts = [p.strip().strip("'\"") for p in parts]
        rows.append(parts)

    n = len(attrs)
    rows = [r[:n] + ["?"] * (n - len(r)) for r in rows]
    df = pd.DataFrame(rows, columns=attrs)

    cluster_col = None
    for col in df.columns:
        if "cluster" in col.lower():
            cluster_col = col
            break

    return df, cluster_col, None


def allocate_splits(n: int):
    train = round(n * 0.65)
    pred  = round(n * 0.25)
    ext   = n - train - pred
    return train, pred, ext


def split_dataframe(df: pd.DataFrame, cluster_col: str):
    train_frames, pred_frames, ext_frames = [], [], []
    for _, grp in df.groupby(cluster_col, sort=False):
        grp = grp.sample(frac=1, random_state=42).reset_index(drop=True)
        n = len(grp)
        t, p, _ = allocate_splits(n)
        train_frames.append(grp.iloc[:t])
        pred_frames.append(grp.iloc[t:t + p])
        ext_frames.append(grp.iloc[t + p:])
    df_train = pd.concat(train_frames, ignore_index=True) if train_frames else pd.DataFrame(columns=df.columns)
    df_pred  = pd.concat(pred_frames,  ignore_index=True) if pred_frames  else pd.DataFrame(columns=df.columns)
    df_ext   = pd.concat(ext_frames,   ignore_index=True) if ext_frames   else pd.DataFrame(columns=df.columns)
    return df_train, df_pred, df_ext


def df_to_arff(df: pd.DataFrame, relation: str, orig_text: str) -> str:
    lines = orig_text.splitlines()
    header_lines = []
    for line in lines:
        if line.strip().lower().startswith("@data"):
            break
        header_lines.append(line)
    new_header = []
    for line in header_lines:
        if line.strip().lower().startswith("@relation"):
            new_header.append(f"@relation {relation}")
        else:
            new_header.append(line)
    data_rows = [",".join(str(v) for v in row) for _, row in df.iterrows()]
    return "\n".join(new_header) + "\n@data\n" + "\n".join(data_rows) + "\n"


def build_cluster_table(df: pd.DataFrame, cluster_col: str):
    rows = []
    for cluster_val, grp in df.groupby(cluster_col, sort=False):
        n = len(grp)
        train, pred, ext = allocate_splits(n)
        rows.append({
            "Cluster": str(cluster_val),
            "Total": n,
            "Training (65%)": train,
            "Prediction (25%)": pred,
            "External (10%)": ext,
        })
    summary = pd.DataFrame(rows)
    try:
        summary["_sort"] = summary["Cluster"].astype(int)
        summary = summary.sort_values("_sort").drop(columns="_sort")
    except Exception:
        summary = summary.sort_values("Cluster")
    return summary.reset_index(drop=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🔬 QSAR · WEKA · ML Dataset Tool</div>
    <div class="hero-title">Clusta<span>Split</span></div>
    <div class="hero-sub">Cluster-aware ARFF dataset splitter for QSAR model development</div>
    <hr class="hero-rule">
    <p class="hero-desc">
        Upload your clustered WEKA ARFF files and ClustaSplit automatically allocates compounds into
        <strong>Training (65%)</strong>, <strong>Prediction (25%)</strong>, and <strong>External (10%)</strong>
        sets — respecting cluster proportions to ensure unbiased, reproducible machine learning workflows.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Upload zone ────────────────────────────────────────────────────────────────
col_a, col_b = st.columns(2, gap="large")

with col_a:
    st.markdown("""
    <div class="upload-label">
        <span class="upload-dot dot-active"></span>
        Active Compounds — ARFF File
    </div>""", unsafe_allow_html=True)
    active_file = st.file_uploader("Upload active ARFF", type=["arff","txt"], key="active", label_visibility="collapsed")

with col_b:
    st.markdown("""
    <div class="upload-label">
        <span class="upload-dot dot-inactive"></span>
        Inactive Compounds — ARFF File
    </div>""", unsafe_allow_html=True)
    inactive_file = st.file_uploader("Upload inactive ARFF", type=["arff","txt"], key="inactive", label_visibility="collapsed")

st.markdown("<div class='thin-div'></div>", unsafe_allow_html=True)

if not active_file and not inactive_file:
    st.info("⬆️  Upload one or both ARFF files above to generate your split report.")
    st.stop()


# ── Render section ─────────────────────────────────────────────────────────────
def render_section(label: str, uploaded_file, acc_class: str):
    text = uploaded_file.read().decode("utf-8", errors="replace")
    df, cluster_col, err = parse_weka_arff(text)

    if err:
        st.error(f"{label}: {err}")
        return None
    if df is None or cluster_col is None:
        st.warning(f"{label}: Could not detect a 'cluster' attribute. Ensure your ARFF has a column with 'cluster' in its name.")
        return None

    summary = build_cluster_table(df, cluster_col)
    n_clusters   = len(summary)
    total_n      = summary["Total"].sum()
    total_train  = summary["Training (65%)"].sum()
    total_pred   = summary["Prediction (25%)"].sum()
    total_ext    = summary["External (10%)"].sum()

    st.markdown(
        f"""<div class="sec-header">
            <span class="sec-accent {acc_class}"></span>
            {label} Dataset &nbsp;·&nbsp; {n_clusters} Clusters &nbsp;·&nbsp; {total_n:,} Compounds
        </div>""",
        unsafe_allow_html=True,
    )

    styled = (
        summary.style
        .format({"Total":"{:,}","Training (65%)":"{:,}","Prediction (25%)":"{:,}","External (10%)":"{:,}"})
        .set_properties(**{"text-align":"right"}, subset=["Total","Training (65%)","Prediction (25%)","External (10%)"])
        .set_properties(**{"font-weight":"600"}, subset=["Cluster"])
        .bar(subset=["Total"], color="#ede9fe", vmin=0)
    )
    st.dataframe(styled, use_container_width=True, hide_index=True)

    st.markdown(
        f"""<div class="pill-row">
            <span class="pill pill-train"><span class="pill-dot pd-train"></span>Training &nbsp;<strong>{total_train:,}</strong></span>
            <span class="pill pill-pred"><span class="pill-dot pd-pred"></span>Prediction &nbsp;<strong>{total_pred:,}</strong></span>
            <span class="pill pill-ext"><span class="pill-dot pd-ext"></span>External &nbsp;<strong>{total_ext:,}</strong></span>
        </div>""",
        unsafe_allow_html=True,
    )

    df_train, df_pred, df_ext = split_dataframe(df, cluster_col)
    slug = label.lower()
    arff_train = df_to_arff(df_train, f"{slug}_training",   text)
    arff_pred  = df_to_arff(df_pred,  f"{slug}_prediction", text)
    arff_ext   = df_to_arff(df_ext,   f"{slug}_external",   text)

    st.markdown("<div class='dl-label'>⬇ Download Split ARFF Files</div>", unsafe_allow_html=True)
    dl1, dl2, dl3 = st.columns(3)
    with dl1:
        st.download_button(f"⬇ {label} — Training",   data=arff_train, file_name=f"{slug}_training.arff",   mime="text/plain", use_container_width=True, key=f"dl_train_{slug}")
    with dl2:
        st.download_button(f"⬇ {label} — Prediction", data=arff_pred,  file_name=f"{slug}_prediction.arff", mime="text/plain", use_container_width=True, key=f"dl_pred_{slug}")
    with dl3:
        st.download_button(f"⬇ {label} — External",   data=arff_ext,   file_name=f"{slug}_external.arff",   mime="text/plain", use_container_width=True, key=f"dl_ext_{slug}")

    return {
        "train": int(total_train), "pred": int(total_pred), "ext": int(total_ext), "total": int(total_n),
        "df_train": df_train, "df_pred": df_pred, "df_ext": df_ext,
        "orig_text": text,
    }


# ── Process files ──────────────────────────────────────────────────────────────
results = {}
if active_file:
    results["active"] = render_section("Active", active_file, "acc-blue")
    st.markdown("<div class='thin-div'></div>", unsafe_allow_html=True)
if inactive_file:
    results["inactive"] = render_section("Inactive", inactive_file, "acc-orange")
    st.markdown("<div class='thin-div'></div>", unsafe_allow_html=True)


# ── Combined summary ───────────────────────────────────────────────────────────
valid = {k: v for k, v in results.items() if v is not None}

if len(valid) >= 1:
    grand_train = sum(v["train"] for v in valid.values())
    grand_pred  = sum(v["pred"]  for v in valid.values())
    grand_ext   = sum(v["ext"]   for v in valid.values())
    grand_total = grand_train + grand_pred + grand_ext

    def pct(n): return f"{n/grand_total*100:.1f}%" if grand_total else "—"

    st.markdown("""<div class="sec-header">
        <span class="sec-accent acc-green"></span>
        Combined Dataset Summary
    </div>""", unsafe_allow_html=True)

    st.markdown(
        f"""<div class="summary-grid">
            <div class="s-card sc-total">
                <div class="sc-label">Total</div>
                <div class="sc-value">{grand_total:,}</div>
                <div class="sc-pct">compounds</div>
            </div>
            <div class="s-card sc-train">
                <div class="sc-label">Training</div>
                <div class="sc-value">{grand_train:,}</div>
                <div class="sc-pct">{pct(grand_train)}</div>
            </div>
            <div class="s-card sc-pred">
                <div class="sc-label">Prediction</div>
                <div class="sc-value">{grand_pred:,}</div>
                <div class="sc-pct">{pct(grand_pred)}</div>
            </div>
            <div class="s-card sc-ext">
                <div class="sc-label">External</div>
                <div class="sc-value">{grand_ext:,}</div>
                <div class="sc-pct">{pct(grand_ext)}</div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    breakdown_rows = []
    if "active" in valid:
        r = valid["active"]
        breakdown_rows.append({"Class":"Active","Total":r["total"],"Training":r["train"],"Prediction":r["pred"],"External":r["ext"]})
    if "inactive" in valid:
        r = valid["inactive"]
        breakdown_rows.append({"Class":"Inactive","Total":r["total"],"Training":r["train"],"Prediction":r["pred"],"External":r["ext"]})
    breakdown_rows.append({"Class":"Combined","Total":grand_total,"Training":grand_train,"Prediction":grand_pred,"External":grand_ext})

    bd_df = pd.DataFrame(breakdown_rows)
    st.dataframe(
        bd_df.style
            .format({c:"{:,}" for c in ["Total","Training","Prediction","External"]})
            .set_properties(**{"font-weight":"700"}, subset=pd.IndexSlice[bd_df.index[-1:], :])
            .set_properties(**{"text-align":"right"}, subset=["Total","Training","Prediction","External"]),
        use_container_width=True,
        hide_index=True,
    )

    csv_buf = io.StringIO()
    bd_df.to_csv(csv_buf, index=False)
    st.download_button("⬇ Download Summary CSV", data=csv_buf.getvalue(), file_name="clustasplit_summary.csv", mime="text/csv")

    if len(valid) >= 1:
        st.markdown("<div class='thin-div'></div>", unsafe_allow_html=True)
        st.markdown("""<div class="sec-header">
            <span class="sec-accent acc-blue"></span>
            Download Combined ARFF Files (Active + Inactive)
        </div>""", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px;color:#9ba3bf;margin-top:-12px;margin-bottom:18px;'>Each file merges active and inactive compounds for that split set.</p>", unsafe_allow_html=True)

        ref_text = valid.get("active", valid.get("inactive", {})).get("orig_text", "")

        def concat_split(key):
            frames = [v[key] for v in valid.values() if key in v and v[key] is not None]
            return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

        combined_train = concat_split("df_train")
        combined_pred  = concat_split("df_pred")
        combined_ext   = concat_split("df_ext")

        arff_all_train = df_to_arff(combined_train, "combined_training",   ref_text)
        arff_all_pred  = df_to_arff(combined_pred,  "combined_prediction", ref_text)
        arff_all_ext   = df_to_arff(combined_ext,   "combined_external",   ref_text)

        ca1, ca2, ca3 = st.columns(3)
        with ca1:
            st.download_button(f"⬇ Combined Training ({grand_train:,})",   data=arff_all_train, file_name="combined_training.arff",   mime="text/plain", use_container_width=True, key="dl_combined_train")
        with ca2:
            st.download_button(f"⬇ Combined Prediction ({grand_pred:,})",  data=arff_all_pred,  file_name="combined_prediction.arff",  mime="text/plain", use_container_width=True, key="dl_combined_pred")
        with ca3:
            st.download_button(f"⬇ Combined External ({grand_ext:,})",     data=arff_all_ext,   file_name="combined_external.arff",    mime="text/plain", use_container_width=True, key="dl_combined_ext")


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("<div class='thin-div'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="footer-wrap">

    <div class="footer-top">
        <div class="footer-icon">🔬</div>
        <div>
            <div class="footer-author">Md. Nabiul Hoque</div>
            <div class="footer-app">ClustaSplit &nbsp;·&nbsp; QSAR Dataset Splitter</div>
        </div>
    </div>

    <div class="footer-body">
        <div class="footer-tech-title">Built with</div>
        <div class="tech-pills">
            <span class="tech-pill tp-python">🐍 Python 3.x</span>
            <span class="tech-pill tp-st">⚡ Streamlit</span>
            <span class="tech-pill tp-pandas">🐼 Pandas</span>
            <span class="tech-pill tp-numpy">🔢 NumPy</span>
            <span class="tech-pill tp-regex">🔍 Regex (re)</span>
            <span class="tech-pill tp-io">📦 io</span>
            <span class="tech-pill tp-weka">🧬 WEKA ARFF</span>
            <span class="tech-pill tp-fonts">✏️ Google Fonts</span>
        </div>
    </div>

    <div class="footer-rights">
        <span class="rights-text">All rights reserved. Unauthorized reproduction or distribution is prohibited.</span>
        <span class="rights-copy">© 2024 Md. Nabiul Hoque</span>
    </div>

</div>
""", unsafe_allow_html=True)
