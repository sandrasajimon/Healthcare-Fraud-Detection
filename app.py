import streamlit as st
import pandas as pd
import plotly.express as px
import time
import re

# Minimal CSS for root background, sidebar, input, button, and animations
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0a1a2f 0%, #1a2a44 100%) !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', 'Helvetica Neue', sans-serif !important;
        min-height: 100vh !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1a2a44 0%, #0a1a2f 100%) !important;
        padding: 20px !important;
    }
    div[data-testid="stTextInput"] input {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #1a2a44 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #93c5fd !important;
        opacity: 0.7 !important;
    }
    div[data-testid="stSelectbox"] select {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    div[data-testid="stButton"] button {
        background: linear-gradient(90deg, #14b8a6 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    div[data-testid="stButton"] button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    .st-emotion-cache-1wmy9hl,
    .st-emotion-cache-1r4qj8v,
    .st-emotion-cache-1v0mbdj,
    .st-emotion-cache-1cypcdb {
        padding: 0 !important;
        margin: 0 !important;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .fade-in {
        animation: fadeIn 1s ease-in-out;
    }
    .search-card {
        background: linear-gradient(135deg, rgba(20, 184, 166, 0.1), rgba(59, 130, 246, 0.1));
        backdrop-filter: blur(15px);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 500px;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_parquet("your_dataset_enhanced.parquet")  # Using the pre-calculated dataset for now

df = load_data()

# Prepare unique names for autocomplete
unique_names = sorted(df["Prscrbr_Full_Name"].unique())

def normalize_name(name):
    """Normalize name for flexible matching."""
    titles = ["Dr.", "Mr.", "Ms.", "Mrs.", "MD", "PhD"]
    name = name.strip()
    for title in titles:
        name = name.replace(title, "").strip()
    name = re.sub(r'\s+', ' ', name)
    if "," in name:
        last, first = name.split(",", 1)
        return f"{first.strip()} {last.strip()}"
    return name

def search_name_in_dataset(name, dataset):
    """Search for a name in the dataset with flexible matching."""
    prescriber = dataset[dataset['Prscrbr_Full_Name'].str.contains(name, case=False, na=False)]
    if not prescriber.empty:
        return prescriber
    
    normalized_input = normalize_name(name)
    prescriber = dataset[dataset['Prscrbr_Full_Name'].str.contains(normalized_input, case=False, na=False)]
    if not prescriber.empty:
        return prescriber
    
    name_parts = normalized_input.split()
    if len(name_parts) >= 2:
        part1, part2 = name_parts[0], name_parts[1]
        prescriber = dataset[
            (dataset['Prscrbr_Full_Name'].str.contains(part1, case=False, na=False)) &
            (dataset['Prscrbr_Full_Name'].str.contains(part2, case=False, na=False))
        ]
        if not prescriber.empty:
            return prescriber
    
    reverse_name = f"{name_parts[1]} {name_parts[0]}"
    prescriber = dataset[dataset['Prscrbr_Full_Name'].str.contains(reverse_name, case=False, na=False)]
    if not prescriber.empty:
        return prescriber
    
    return pd.DataFrame()

def clear_search_input():
    """Callback function to clear only the search input, not the results."""
    st.session_state.input_value = ""
    st.session_state.search_type = "NPI"

def main():
    # Initialize session state
    if 'input_value' not in st.session_state:
        st.session_state.input_value = ""
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'search_type' not in st.session_state:
        st.session_state.search_type = "NPI"

    # Header with card design
    st.markdown("""
        <div style="background: linear-gradient(90deg, rgba(20, 184, 166, 0.1), rgba(59, 130, 246, 0.1)); backdrop-filter: blur(15px); padding: 30px; text-align: center; border-bottom: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 8px 20px rgba(0,0,0,0.3); margin-bottom: 50px; border-radius: 0 0 20px 20px; position: relative;">
            <p style="color: #f8fafc; font-size: 44px; font-weight: 700; margin: 0; text-shadow: 0 2px 10px rgba(255, 255, 255, 0.2);">Prescriber Analyzer</p>
            <p style="color: #93c5fd; font-size: 18px; font-weight: 300; margin: 10px 0;">Insights into Medicare Part D Data</p>
            <div style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 120px; height: 3px; background: linear-gradient(90deg, #14b8a6, #3b82f6); border-radius: 2px;"></div>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown("<h2 style='color: #f8fafc;'>Control Center</h2>", unsafe_allow_html=True)
    state_filter = st.sidebar.multiselect("Filter by State", options=sorted(df["Prscrbr_State_Abrvtn"].unique()), default=[])

    # Filter dataset
    filtered_df = df
    if state_filter:
        filtered_df = filtered_df[filtered_df["Prscrbr_State_Abrvtn"].isin(state_filter)]

    # Search Bar in Original Position (Centered)
    st.markdown('<div class="search-card fade-in">', unsafe_allow_html=True)
    st.markdown('<p style="color: #14b8a6; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 8px; margin-top: 15px; display: block;">Search Prescriber</p>', unsafe_allow_html=True)
    search_type = st.selectbox("Search by", ["NPI", "Name"], label_visibility="collapsed", key="search_type_selectbox")

    # Update search type in session state
    st.session_state.search_type = search_type

    if search_type == "NPI":
        search_input = st.text_input("", placeholder="e.g., 1003000530", label_visibility="collapsed", key="search_input", value=st.session_state.input_value)
    else:
        search_input = st.text_input("", placeholder="e.g., Semonche, Amanda", label_visibility="collapsed", key="search_input", value=st.session_state.input_value)

    # Update the input value in session state
    st.session_state.input_value = search_input

    # Create two columns for the buttons
    btn_col1, btn_col2 = st.columns([1, 1])
    
    with btn_col1:
        if st.button("Analyze"):
            if search_input:
                with st.spinner("Analyzing prescriber profile..."):
                    time.sleep(1)  # Simulate processing time to make it look dynamic
                    if search_type == "NPI":
                        try:
                            npi = int(search_input)
                            prescriber = df[df['Prscrbr_NPI'] == npi]
                            if prescriber.empty:
                                st.error("Prescriber not found in the dataset! Please check the NPI.")
                                st.session_state.search_results = None
                            else:
                                prescriber_filtered = filtered_df[filtered_df['Prscrbr_NPI'] == npi]
                                if prescriber_filtered.empty:
                                    st.warning("Prescriber found in the dataset but filtered out by current filters (e.g., state). Showing results from the full dataset.")
                                result = prescriber.groupby('Prscrbr_NPI').agg({
                                    'Prscrbr_Full_Name': 'first',
                                    'Tot_Clms': 'sum',
                                    'Tot_Drug_Cst': 'sum',
                                    'Is_Fraudulent': 'max',
                                    'Prscrbr_City': 'first',
                                    'Prscrbr_State_Abrvtn': 'first'
                                }).iloc[0]
                                npi = result.name
                                is_fraudulent = result['Is_Fraudulent']
                                st.session_state.search_results = (result, npi, is_fraudulent, prescriber)
                        except ValueError:
                            st.error("Invalid NPI format! Enter a numeric value.")
                            st.session_state.search_results = None
                    else:
                        prescriber = search_name_in_dataset(search_input, df)
                        if prescriber.empty:
                            st.error("Prescriber not found in the dataset! Please check the spelling or try a different name.")
                            st.session_state.search_results = None
                        else:
                            prescriber_filtered = search_name_in_dataset(search_input, filtered_df)
                            if prescriber_filtered.empty:
                                st.warning("Prescriber found in the dataset but filtered out by current filters (e.g., state). Showing results from the full dataset.")
                            if len(prescriber['Prscrbr_NPI'].unique()) > 1:
                                st.warning("Multiple prescribers found with this name. Showing the first match.")
                                prescriber = prescriber.groupby('Prscrbr_NPI').first().reset_index()
                            result = prescriber.groupby('Prscrbr_NPI').agg({
                                'Prscrbr_Full_Name': 'first',
                                'Tot_Clms': 'sum',
                                'Tot_Drug_Cst': 'sum',
                                'Is_Fraudulent': 'max',
                                'Prscrbr_City': 'first',
                                'Prscrbr_State_Abrvtn': 'first'
                            }).iloc[0]
                            npi = result.name
                            is_fraudulent = result['Is_Fraudulent']
                            st.session_state.search_results = (result, npi, is_fraudulent, prescriber)

    with btn_col2:
        if st.button("Clear", type="secondary", on_click=clear_search_input):
            pass

    st.markdown('</div>', unsafe_allow_html=True)

    # Display search results if they exist
    if st.session_state.search_results:
        result, npi, is_fraudulent, prescriber = st.session_state.search_results
        display_results(result, npi, is_fraudulent, prescriber)

    # Summary (only Total Prescribers)
    st.markdown('<div style="padding: 20px; margin: 20px 0;" class="fade-in">', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #f8fafc; font-size: 18px; font-weight: 500; margin: 0 0 10px 0; line-height: 1.4; display: flex; align-items: center;"><i class="fas fa-users" style="margin-right: 10px; font-size: 20px; color: #14b8a6;"></i>Total Prescribers: {len(filtered_df["Prscrbr_NPI"].unique()):,.0f}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Interactive Map for Geographical Insights
    st.markdown('<div style="padding: 20px; margin: 20px 0;" class="fade-in">', unsafe_allow_html=True)
    st.markdown('<p style="color: #14b8a6; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 8px;">Geographical Distribution of Prescribers</p>', unsafe_allow_html=True)
    state_counts = filtered_df.groupby("Prscrbr_State_Abrvtn").agg({
        "Prscrbr_NPI": "nunique"
    }).reset_index()
    state_counts.columns = ["State", "Number of Prescribers"]
    fig_map = px.choropleth(
        state_counts,
        locations="State",
        locationmode="USA-states",
        color="Number of Prescribers",
        hover_data=["Number of Prescribers"],
        scope="usa",
        color_continuous_scale="Teal",
        labels={"Number of Prescribers": "Prescribers"}
    )
    fig_map.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc'),
        title_font=dict(size=18, color='#14b8a6'),
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(bgcolor='rgba(0,0,0,0)')
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Table of Filtered Prescribers (Expandable)
    with st.expander("View Filtered Prescribers", expanded=False):
        st.markdown('<div style="padding: 20px; margin: 20px 0;" class="fade-in">', unsafe_allow_html=True)
        prescriber_list = filtered_df.groupby("Prscrbr_NPI").agg({
            "Prscrbr_Full_Name": "first",
            "Prscrbr_City": "first",
            "Prscrbr_State_Abrvtn": "first"
        }).reset_index()
        prescriber_list = prescriber_list[["Prscrbr_NPI", "Prscrbr_Full_Name", "Prscrbr_City", "Prscrbr_State_Abrvtn"]]
        st.dataframe(prescriber_list, use_container_width=True)
        csv = prescriber_list.to_csv(index=False)
        st.download_button("Download Filtered Prescribers", csv, "filtered_prescribers.csv", "text/csv")
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 25px; color: #93c5fd; font-size: 14px; margin-top: 40px; border-top: 1px solid rgba(255, 255, 255, 0.05); position: relative;">
            Powered by xAI | <a href="https://xai.company" style="color: #14b8a6; text-decoration: none;">Discover Our Vision</a>
            <div style="position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%); width: 80px; height: 2px; background: linear-gradient(90deg, #14b8a6, #3b82f6); border-radius: 1px;"></div>
        </div>
    """, unsafe_allow_html=True)

def display_results(result, npi, is_fraudulent, prescriber):
    # Results Section
    st.markdown('<div style="padding: 20px; margin: 20px 0;" class="fade-in">', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #f8fafc; font-size: 18px; font-weight: 500; margin: 0 0 10px 0; line-height: 1.4; display: flex; align-items: center;"><i class="fas fa-user-md" style="margin-right: 10px; font-size: 20px; color: #14b8a6;"></i>{result["Prscrbr_Full_Name"]} (NPI: {npi})</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #f8fafc; font-size: 18px; font-weight: 500; margin: 0 0 10px 0; line-height: 1.4; display: flex; align-items: center;"><i class="fas fa-map-marker-alt" style="margin-right: 10px; font-size: 20px; color: #14b8a6;"></i>{result["Prscrbr_City"]}, {result["Prscrbr_State_Abrvtn"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #f8fafc; font-size: 18px; font-weight: 500; margin: 0 0 10px 0; line-height: 1.4; display: flex; align-items: center;"><i class="fas fa-file-medical" style="margin-right: 10px; font-size: 20px; color: #14b8a6;"></i>Total Claims: {result["Tot_Clms"]:,.0f}</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #f8fafc; font-size: 18px; font-weight: 500; margin: 0 0 10px 0; line-height: 1.4; display: flex; align-items: center;"><i class="fas fa-dollar-sign" style="margin-right: 10px; font-size: 20px; color: #14b8a6;"></i>Total Drug Cost: ${result["Tot_Drug_Cst"]:,.2f}</p>', unsafe_allow_html=True)
    fraud_class = "color: #f472b6; font-weight: 700; font-size: 20px;" if is_fraudulent else "color: #34d399; font-weight: 700; font-size: 20px;"
    fraud_icon = "fas fa-exclamation-circle" if is_fraudulent else "fas fa-check-circle"
    st.markdown(f'<p style="color: #f8fafc; font-size: 18px; font-weight: 500; margin: 0 0 10px 0; line-height: 1.4; display: flex; align-items: center;"><i class="{fraud_icon}" style="margin-right: 10px; font-size: 20px; color: #14b8a6;"></i>Flagged as Fraud: <span style="{fraud_class}">{ "Yes" if is_fraudulent else "No" }</span></p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Raw Data and Export
    with st.expander("View Detailed Insights", expanded=False):
        st.write(prescriber[['Prscrbr_Full_Name', 'Tot_Clms', 'Tot_Drug_Cst']])
    csv = prescriber.to_csv(index=False)
    st.download_button("Download Results", csv, f"prescriber_{npi}_results.csv", "text/csv")

if __name__ == "__main__":
    main()
