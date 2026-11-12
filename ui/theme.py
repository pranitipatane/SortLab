"""App-wide styling that Streamlit's theme options cannot express (Clean Studio design)."""

CSS = """
<style>
/* Page */
.block-container {padding-top: .75rem; max-width: 1240px;}
.block-container h2 {font-size: 1.875rem; font-weight: 700; letter-spacing: -.015em; padding: 0 0 .1rem;}
[data-testid="stHeaderActionElements"] {display: none;}
[data-testid="stImage"] img {border-radius: 14px;}

/* Buttons: one accent, with clear hover and press feedback */
button[data-testid="stBaseButton-primary"] {font-weight: 600; border: 0;
    box-shadow: 0 1px 2px rgba(29, 95, 214, .3); transition: background .12s ease, box-shadow .12s ease, transform .08s ease;}
button[data-testid="stBaseButton-primary"]:hover {background: #174CAB; color: #FFFFFF;
    box-shadow: 0 6px 16px -6px rgba(29, 95, 214, .6);}
button[data-testid="stBaseButton-primary"]:active {transform: translateY(1px);}
button[data-testid="stBaseButton-secondary"] {background: #FFFFFF; border: 1px solid #DDE1E8; font-weight: 500;
    box-shadow: 0 1px 2px rgba(22, 25, 29, .05); transition: background .12s ease, border-color .12s ease, color .12s ease;}
button[data-testid="stBaseButton-secondary"]:hover {background: #F3F7FE; border-color: #1D5FD6; color: #174CAB;}
button[data-testid="stBaseButton-secondary"]:active {background: #E7EEFB;}
.st-key-begin_visualizing button {min-height: 3.25rem; font-size: 1.02rem;
    box-shadow: 0 8px 20px -8px rgba(29, 95, 214, .65);}

/* Input type choices: separate chips, with the selected one solid blue */
button[data-variant="segmented_control"] {min-height: 2.6rem; margin: 0 .35rem .35rem 0 !important;
    padding-inline: .55rem !important; white-space: nowrap;
    border: 1px solid #DDE1E8 !important; border-radius: 8px !important; background: #FFFFFF !important;
    font-weight: 500; transition: background .12s ease, border-color .12s ease;}
button[data-variant="segmented_control"]:hover {background: #F3F7FE !important; border-color: #1D5FD6 !important;}
button[data-variant="segmented_control"][data-selected],
button[data-variant="segmented_control"][data-selected]:hover {background: #1D5FD6 !important; border-color: #1D5FD6 !important;}
button[data-variant="segmented_control"][data-selected] p {color: #FFFFFF !important; font-weight: 600;}

/* Streamlit pulls markdown up by 1rem, which clips custom HTML inside padded boxes */
[class*="st-key-algo_row_"] [data-testid="stMarkdownContainer"],
.st-key-step_panel [data-testid="stMarkdownContainer"],
.st-key-learn_page [data-testid="stMarkdownContainer"] {margin-bottom: 0 !important;}

/* Sidebar brand: the empty header strip floats, so the logo can sit at the top */
[data-testid="stSidebarHeader"] {position: absolute !important; top: 0; right: 0; height: auto; padding: .5rem; z-index: 1;}
[data-testid="stSidebarUserContent"] {padding-top: 1.5rem !important;}
.sl-brand {display: flex; align-items: center; gap: .7rem; padding: 0 .4rem; margin-bottom: 1.5rem;}
.sl-logo {flex: none; width: 38px; height: 38px; box-sizing: border-box; display: flex; align-items: flex-end;
    justify-content: center; gap: 3px; padding-bottom: 9px; background: #1D5FD6; border-radius: 10px;}
.sl-logo span {width: 4px; background: #FFFFFF; border-radius: 2px;}
.sl-logo span:nth-child(1) {height: 9px;}
.sl-logo span:nth-child(2) {height: 20px;}
.sl-logo span:nth-child(3) {height: 14px;}
.sl-brand-name {font-size: 1.25rem; font-weight: 700; letter-spacing: -.01em; line-height: 1.15; color: #16191D;}
.sl-brand-tag {font-size: .81rem; color: #5A6270;}

/* Sidebar navigation: Streamlit shrinks each option to its text, so stretch them to full width */
[data-testid="stSidebar"] [data-testid="stRadioGroup"] {align-items: stretch; gap: .25rem;}
[data-testid="stSidebar"] [data-testid="stRadioOption"] {display: block; width: 100%; box-sizing: border-box;
    padding: .65rem .75rem; border-radius: 8px; cursor: pointer;}
[data-testid="stSidebar"] [data-testid="stRadioOption"] p {font-size: .94rem; font-weight: 500;}
[data-testid="stSidebar"] [data-testid="stRadioOption"] > :not(:has(input)) > :first-child {display: none;}
[data-testid="stSidebar"] [data-testid="stRadioOption"]:hover {background: #ECEEF2;}
[data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected] {background: #E7EEFB;}
[data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected] p {color: #174CAB; font-weight: 600;}

/* Metric tiles */
[data-testid="stMetric"] {background: #F6F7F9; border-radius: 10px; padding: .6rem .9rem;}

/* Algorithm rows: the invisible Streamlit button is stretched over the whole row */
[class*="st-key-algo_row_"] {position: relative; gap: 0; padding: .5rem .9rem; border: 1px solid #DDE1E8;
    border-radius: 8px; background: #FFFFFF; box-shadow: 0 1px 2px rgba(22, 25, 29, .06);
    transition: border-color .12s ease, box-shadow .12s ease; justify-content: center;
    min-height: min(4.5rem, clamp(3.9rem, calc((100vh - 8.75rem) / 6), 6rem));}
/* Rows keep a natural height; spare window height goes between them so the list still fills its column */
.st-key-algo_list {gap: max(.25rem, calc(clamp(3.9rem, calc((100vh - 8.75rem) / 6), 6rem) - 4.25rem)) !important;}
[class*="st-key-algo_row_"]:hover {border-color: #1D5FD6; box-shadow: 0 6px 16px -8px rgba(29, 95, 214, .45);}
[class*="st-key-algo_row_"]:has(button:focus-visible) {outline: 2px solid #1D5FD6; outline-offset: 1px;}
[class*="st-key-algo_row_"] div:has(button) {position: static !important;}
[class*="st-key-algo_row_"] button {position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer;}
.st-key-algo_row_selected, .st-key-algo_row_selected:hover {border: 1.5px solid #1D5FD6; background: #F3F7FE;
    box-shadow: 0 0 0 3px rgba(29, 95, 214, .12);}
.sl-row {display: flex; justify-content: space-between; align-items: center; gap: .75rem;}
.sl-row-name {font-size: 1rem; font-weight: 600;}
.sl-row-tag {font-size: .82rem; color: #5A6270;}
.sl-row-badge {padding: .3rem .7rem; border-radius: 999px; font-size: .82rem; font-weight: 600; white-space: nowrap;}
.sl-row-badge-slow {background: #FFF0E6; color: #A83A00;}
.sl-row-badge-fast {background: #E4F6EC; color: #05704A;}

/* Preview grows and shrinks with the window; the matching background hides any side gaps */
.st-key-setup_preview img {width: 100%; height: clamp(15rem, calc(100vh - 20rem), 25rem); object-fit: contain;
    background: #F6F7F9;}

/* Facts under the preview */
.sl-facts {display: flex; flex-wrap: wrap; gap: .4rem 2.5rem; font-size: .88rem; color: #5A6270;}
.sl-facts strong {color: #16191D; font-weight: 600;}

/* Step panel beside the chart */
.sl-panel-label {font-size: .78rem; font-weight: 500; color: #5A6270;}
.sl-step-title {font-size: 1.35rem; font-weight: 700; line-height: 1.2; letter-spacing: -.01em;
    margin-top: .3rem; min-height: 2.4em;}
.sl-step-body {font-size: .98rem; line-height: 1.5; color: #3C4450; margin-top: .4rem; min-height: 4.5em;}
.sl-note {margin-top: .75rem; padding: .75rem .85rem; background: #F3F7FE; border-radius: 10px; min-height: 6.9rem;
    box-sizing: border-box;}
.sl-note-label {font-size: .86rem; font-weight: 600; color: #174CAB;}
.sl-note-text {font-size: .88rem; line-height: 1.5; color: #3C4450; margin-top: .2rem;}
.sl-stats {display: grid; grid-template-columns: repeat(3, 1fr); gap: .5rem; margin: .75rem 0 .15rem;
    padding: .6rem 0; border-top: 1px solid #E6E8EC;}
.sl-stat-value {font-size: 1.3rem; font-weight: 700; font-variant-numeric: tabular-nums;}
.sl-stat-label {font-size: .76rem; color: #5A6270;}

/* How it works tab */
.sl-learn-title {font-size: 1.875rem; font-weight: 700; letter-spacing: -.015em;}
.sl-learn-lead {font-size: 1.15rem; line-height: 1.4; color: #3C4450; margin: .35rem 0 1.25rem;}
.sl-learn-heading {font-size: 1.05rem; font-weight: 700; margin-bottom: .65rem;}
.sl-learn-steps {list-style: none; margin: 0; padding: 0;}
.sl-learn-steps li {display: flex; gap: .75rem; margin: 0 0 .95rem; padding: 0;}
.sl-learn-num {flex: none; width: 1.75rem; height: 1.75rem; display: flex; align-items: center; justify-content: center;
    border-radius: 50%; background: #E7EEFB; color: #174CAB; font-size: .875rem; font-weight: 700;}
.sl-learn-step {font-size: 1rem; font-weight: 600; line-height: 1.4; padding-top: .12rem;}
.sl-learn-detail {font-size: .94rem; line-height: 1.5; color: #3C4450; margin-top: .1rem;}
.sl-learn-use {margin-top: .4rem; padding: .9rem 1rem; background: #F3F7FE; border-radius: 12px;}
.sl-learn-use-text {font-size: 1rem; line-height: 1.45; color: #3C4450; margin-top: .15rem;}
.sl-learn-tiles {display: grid; grid-template-columns: repeat(3, 1fr); gap: .75rem;}
.sl-learn-tile {padding: 1rem; background: #F6F7F9; border-radius: 12px;}
.sl-learn-big {font-size: 1.45rem; font-weight: 700; margin-top: .1rem; white-space: nowrap;}
.sl-speed-slow, .sl-speed-fast {font-size: .875rem; font-weight: 500; margin-top: .1rem;}
.sl-speed-slow {color: #A83A00;}
.sl-speed-fast {color: #05704A;}
.sl-learn-note {font-size: .94rem; line-height: 1.45; color: #3C4450; margin: .75rem 0 1.1rem;}
.sl-learn-rows {border-block: 1px solid #E6E8EC; margin-bottom: 1.25rem;}
.sl-learn-rows > div {display: flex; justify-content: space-between; gap: 1rem; padding: .7rem 0; font-size: .98rem;}
.sl-learn-rows > div + div {border-top: 1px solid #E6E8EC;}
.sl-learn-rows span {color: #3C4450;}
.sl-learn-rows strong {font-weight: 600; text-align: right;}
.sl-learn-lists {display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem;}
.sl-learn-list {list-style: none; margin: 0; padding: 0;}
.sl-learn-list li {position: relative; margin: 0 0 .6rem; padding: 0 0 0 1.5rem; font-size: .94rem; line-height: 1.4; color: #3C4450;}
.sl-learn-list li::before {position: absolute; left: 0; font-weight: 700;}
.sl-good li::before {content: "✓"; color: #05704A;}
.sl-bad li::before {content: "✕"; color: #A83A00;}
.sl-learn-code-title {font-size: 1.25rem; font-weight: 700;}
</style>
"""
