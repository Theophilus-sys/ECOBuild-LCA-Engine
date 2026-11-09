# 🌱 EcoBuild: Spatial LCA Recommendation Engine

A dynamic, spatial-intelligence decision tool that transforms narrative construction and manufacturing project descriptions into localized, low-impact environmental compliance strategies. 

By extracting multi-dimensional parameters from text inputs, this engine maps global project sites in real time, routes regional grid data, and solves multi-objective optimization constraints to minimize climate and water footprints without environmental burden-shifting.

---

## 🎯 Core Capabilities

The engine executes six primary functional dimensions derived directly from standardized Life Cycle Assessment (LCA) matrices:

*   **Geospatial Pinpointing:** Utilizes enterprise spatial geocoders to resolve global text inputs (cities, zip codes, countries) into live coordinates, displaying interactive maps natively.
*   **Regional Infrastructure Routing:** Automatically maps location contexts to specific background datasets, alternating between localized power grids (such as the US Midwest `{US-MRO}` pool) and global `{RoW}` (Rest of World) inventories.
*   **Semantic Scale Deciphering:** Leverages natural language processing (NLP) word embeddings to evaluate text descriptions, automatically distinguishing between commercial/industrial enterprises and private residential developments.
*   **Multi-Objective Footprint Co-Optimization:** Minimizes Global Warming Potential (GWP) and Water Scarcity Footprints simultaneously, preventing traditional "greenhouse-to-watershed" burden-shifting traps.
*   **Logistical Supply Chain Auditing:** Tracks transportation-related vocabulary to calculate ton-kilometer (tkm) carbon adjustments based on diesel truck, train, or ocean freight parameters.
*   **Low-TRL Data Risk Mapping:** Identifies low-maturity laboratory or R&D system configurations (such as emerging Carbon Capture & Utilization loops) and deploys pedigree matrix indicators to highlight data volatility.

---

## 🛠️ Tech Stack & Requirements

The system is built entirely on a free, lightweight, open-source Python ecosystem:

*   **Framework UI:** Streamlit (via `streamlit` & `streamlit-folium`)
*   **Spatial Mapping:** Folium & GeoPy (ArcGIS Enterprise Engine)
*   **Natural Language Processing:** spaCy (`en_core_web_md` medium vector model)
*   **Data Processing:** Pandas 

### Installation
Run the following installation command in your terminal environment:
```bash
pip install pandas geopy folium streamlit streamlit-folium spacy
python -m spacy download en_core_web_md
```

---
## 📊 Data & Allocation Framework

The background calculations inside this model are grounded in hardcoded impact indicators from the U.S. National Energy Technology Laboratory (NETL) and global ecoinvent inventory balances:
*   **Baseline Grid vs. Renewable Transition:** Evaluates standard medium-voltage utility extraction models against direct 1-3MW Onshore Wind turbine profiles.
*   **Carbon Circularity (CCU):** Integrates multi-stage system boundaries to capture fossil, biogenic, and atmospheric CO2 inflows, converting point-source stack outflows into upstream technosphere materials.
*   **Data Quality Assessment:** Integrates reliability, completeness, and geographical data matrix factors to compute reliable Geometric Standard Deviations (GSD) across low technology readiness levels (TRL).
