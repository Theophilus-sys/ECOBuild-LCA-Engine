import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import ArcGIS
import spacy

# ==========================================
# 1. APPLICATION GRAPHICS & PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="EcoBuild Spatial LCA Dashboard", 
    layout="wide", 
    page_icon="🌱"
)

st.title("🌱 EcoBuild Spatial LCA Recommendation Engine")
st.caption(
    "\nTransforming narrative project parameters into location-aware, "
    "\nlow-impact environmental compliance strategies."
)

# ==========================================
# 2. CACHED RESOURCE LOADING (NLP Optimization)
# ==========================================
@st.cache_resource
def load_spatial_nlp():
    try:
        return spacy.load("en_core_web_md")
    except OSError:
        os.system("python -m spacy download en_core_web_md")
        return spacy.load("en_core_web_md")

#Load model cleanly using streamlit's resource cache
nlp = load_spatial_nlp()

# Configure global multi-dimensional evaluation vectors
CONCEPT_DOCS = {
    "commercial_industrial": nlp("commercial industrial factory warehouse office skyscraper manufacturing enterprise production facility"),
    "residential_private": nlp("residential private house home apartment villa duplex cottage living space domestic bungalow"),

    "structure": nlp("building materials structural framework concrete steel foundation architecture framing"),
    "energy": nlp("electricity power grid solar wind heating hvac utilities electrical"),
    "logistics": nlp("shipping transport freight shipping container truck train ocean carrier cargo hauling"),
    "chemicals": nlp("chemical manufacturing plant hydrogen ammonia refining methanol urea industrial synthesis"),
    "ccu": nlp("carbon capture utilization greenhouse gas emissions offsets smokestack factory pollution co2 sequestration")
}

# Regional Database Parameters (Directly from your template architecture)
regional_lca = {
    "US-MRO": {
        "grid_name": "market for electricity, medium voltage {US-MRO}",
        "GWP_kgCO2e": 0.1369,
        "Wind_GWP": 0.0081,
        "advice": "Your project domain sits inside the US Midwest power pool area where the baseline utility grid relies heavily on regional fossil parameters."
    },
    "Non US MRO": {
        "grid_name": "Rest of World Mix {RoW}",
        "GWP_kgCO2e": 0.2040, 
        "Wind_GWP": 0.0004,
        "advice": "Your project domain is situated outside the US Midwest MRO zone. Applying generalized global Rest of World (RoW) inventory factors."
    }
}

# ==========================================
# 3. SIDEBAR PARAMETER SELECTION & CAPTURE
# ==========================================
st.sidebar.header("Project Desccription Section")
USER_DESCRIPTION = st.sidebar.text_area(
    "Narrative Project Description:", 
    placeholder="e.g., Constructing a small private bungalow home for my family using classic concrete framing...",
    height=200
)
USER_LOCATION = st.sidebar.text_input(
    "Project Geographic Location:", 
    placeholder="e.g., Chicago, IL or Paris, France"
)
EXECUTE_ENGINE = st.sidebar.button("Run Spatial LCA Analysis", type="primary")

# ==========================================
# 4. STREAMLIT APP RUNTIME ROUTING PIPELINE
# ==========================================
if EXECUTE_ENGINE and USER_LOCATION and USER_DESCRIPTION:

    # A. Execute Enterprise Geolocation Call
    geolocator = ArcGIS()
    location = geolocator.geocode(USER_LOCATION, timeout=15)

    if location is not None:
        lat = location.latitude
        lon = location.longitude
        full_address = location.address

        # Parse textual address components lineally
        address_parts = [part.strip() for part in full_address.split(",")]
        country = address_parts[-1] if len(address_parts) > 0 else "Unknown"
        state = address_parts[-2] if len(address_parts) > 1 else "Unknown"

        # Route baseline grid pools using text pattern evaluations
        mro_states = ["IL", "Illinois", "MN", "Minnesota", "WI", "Wisconsin", "IA", "Iowa", "ND", "North Dakota", "SD", "South Dakota", "NE", "Nebraska"]
        if any(state_id in full_address for state_id in mro_states):
            region_name = f"US Midwest Grid Area ({state})"
            profile = regional_lca["US-MRO"]
        else:
            region_name = f"Global Grid Area ({country})"
            profile = regional_lca["Non US MRO"]

        # B. Split Content Interface Layout (Metrics & Mapping)
        col1, col2 = st.columns([3, 2])

        with col1:
            st.subheader("🌲 Operational Geocontext Matrix")
            st.success(f"**Verified Target Site:** {full_address}")

            # Display real-time dynamic metric data comparisons
            metric1, metric2 = st.columns(2)
            metric1.metric(label="Active Regional Grid Model", value=profile["grid_name"].split("{")[-1].replace("}", ""))
            metric2.metric(label="Base Grid Carbon Intensity", value=f"{profile['GWP_kgCO2e']} kg CO2e/MJ")

        with col2:
            # Interactive Map Display Panel
            m = folium.Map(location=[lat, lon], zoom_start=12, control_scale=True)
            folium.Marker(
                [lat, lon], 
                popup=f"Project Domain: {region_name}", 
                icon=folium.Icon(color="green", icon="leaf")
            ).add_to(m)
            st_folium(m, width="100%", height=220, key="streamlit_lca_map")

        # C. NLP Semantic Multi-Label Matrix Evaluation
        user_doc = nlp(USER_DESCRIPTION.lower())

        # Exclusive scale selection verification step
        commercial_score = user_doc.similarity(CONCEPT_DOCS["commercial_industrial"])
        residential_score = user_doc.similarity(CONCEPT_DOCS["residential_private"])
        project_scale = "residential_private" if residential_score > commercial_score else "commercial_industrial"

        # Map additional LCA impact criteria targets
        lca_categories = ["structure", "ccu", "energy","logistics","chemicals"]
        matching_categories = [cat for cat in lca_categories if user_doc.similarity(CONCEPT_DOCS[cat]) >= 0.55]
        matching_categories.append(project_scale)

        # D. Dynamic Personalized Visualization Generation
        st.write("---")
        st.subheader("💡 Personalized Strategic Compliance Roadmap")

        # Render Exclusive Project Scale Profile Information
        if project_scale == "commercial_industrial":
            st.info("🏢 **PROJECT SCALE CLASSIFICATION: COMMERCIAL / INDUSTRIAL**\n\n"
                    f"This infrastructure scope has been classified as an enterprise/industrial deployment context for **{full_address}**. "
                    "Large footprints introduce rigorous baseline requirements. Early chemical selection, infrastructure volume, and structural sourcing profiles are critical parameters during primary LCA development stages.")
        else:
            st.info("🏡 **PROJECT SCALE CLASSIFICATION: PRIVATE RESIDENTIAL / DOMESTIC**\n\n"
                    f"This project configuration has been matched to a private domestic living profile. "
                    "Residential frameworks favor high operational performance curves. Focus efforts heavily on insulation thresholds, passive thermal cooling barriers, and reducing long-term extraction strains from standard local utilities.")

        # Render Core Environmental Impact Subsystems
        if "ccu" in matching_categories:
            with st.expander("🛢️ Carbon Capture & Utilization (CCU) Integration", expanded=True):
                st.warning("**Point-Source Emissions Allocation Framework Triggered**")
                st.markdown(f"""
                * **Baseline Context Analysis:** Sourcing operational electricity for processing gear against the local **{profile['grid_name']}** draws directly from a carbon factor of **{profile['GWP_kgCO2e']} kg CO2e**.
                * **Personalized Structural Strategy:** For industrial process systems, your custom spreadsheet models advise routing any point-source stack or biogenic emissions directly back into the 'Main CCU Process' array to actively turn greenhouse outflows into functional market inputs.
                """)

        if "structure" in matching_categories:
            with st.expander("🏗️ Structural Component & Embodied Carbon Framework", expanded=True):
                st.markdown(f"""
                * **Logistical Transport Warning:** Transporting bulky assets like traditional Portland Concrete or Finished Cold Rolled Steel shapes to localized coordinate pin **({round(lat, 4)}, {round(lon, 4)})** introduces heavy ton-kilometer (tkm) transport penalties.
                * **LCA Action Recommendation:** Blend supplementary cementitious raw metrics (like recycled fly ash or slag) into the structural binder mix or transition framing elements over to structural mass timber assemblies where local safety codes permit.
                """)

        if "energy" in matching_categories:
            saved_carbon = round(profile["GWP_kgCO2e"] - profile["Wind_GWP"], 4)
            with st.expander("⚡ Local Utility Infrastructure & Operational Grids", expanded=True):
                st.markdown(f"""
                * **Regional Baseline Metric Evaluation:** {profile['advice']} Sourcing continuous operational power directly from standard grid infrastructure generates a consistent carbon footprint profile of **{profile['GWP_kgCO2e']} kg CO2e** per unit of energy work.
                * **Personalized Optimization Value:** Swapping operational dependency configurations to a dedicated alternative profile (like Onshore Wind at **{profile['Wind_GWP']} kg CO2e**) slashes your system's lifetime carbon burden by exactly **{saved_carbon} kg CO2e** per unit work cycle!
                """)
