import streamlit as st
import pandas as pd
import os # Used to check if file exists

# --- App Configuration ---
st.set_page_config(page_title="Establishment Search", layout="wide")

# --- Load Data ---
# Define the path to your CSV file
CSV_FILE = "barkatpura-establishments.csv"

@st.cache_data # Cache the data loading step for better performance
def load_data(filepath):
    """Loads the establishment data from a CSV file."""
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            # Ensure relevant columns are treated as strings for searching
            df['EST_ID'] = df['EST_ID'].astype(str)
            df['EST_NAME'] = df['EST_NAME'].astype(str)
            df['NEW OFFICE'] = df['NEW OFFICE'].astype(str)
            df['NEW TASK ID'] = df['NEW TASK ID'].astype(str)
            df['NEW ENF TASK'] = df['NEW ENF TASK'].astype(str)
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return pd.DataFrame() # Return empty DataFrame on error
    else:
        st.error(f"Error: File not found at {filepath}")
        st.info("Please make sure the CSV file is in the same directory as the script.")
        return pd.DataFrame() # Return empty DataFrame if file not found

df = load_data(CSV_FILE)

# --- App UI ---
st.title("Establishment Search App- Post Rationalisation")
st.write("Search for establishments by Establishment ID or Name.")
st.write("Easy search for establishments which have been transferred out or retained/transferred in to Barkatpura.")

# Search input
search_term = st.text_input("Enter Establishment ID or Name:", key="search_input")

# --- Search Logic ---
if not df.empty: # Only proceed if data was loaded successfully
    if search_term:
        # Perform case-insensitive search
        search_term_lower = search_term.lower()
        # Filter based on EST_ID OR EST_NAME containing the search term
        results_df = df[
            df['EST_ID'].str.lower().str.contains(search_term_lower, na=False) |
            df['EST_NAME'].str.lower().str.contains(search_term_lower, na=False)
        ]
    else:
        # Show all data initially or when search box is empty (optional, can be removed)
        # results_df = df
        # Or show nothing until search is performed:
        results_df = pd.DataFrame(columns=df.columns) # Empty dataframe with same columns

    # --- Display Results ---
    if not results_df.empty:
        st.subheader(f"Search Results ({len(results_df)} found):")

        # Prepare data for display (making NEW OFFICE bold using Markdown)
        # Select and reorder columns for display
        display_df = results_df[['EST_NAME', 'EST_ID', 'NEW OFFICE', 'NEW TASK ID', 'NEW ENF TASK']].copy()

        # Format the 'NEW OFFICE' column to be bold using Markdown
        display_df['NEW OFFICE'] = display_df['NEW OFFICE'].apply(lambda x: f"**{x}**")

        # Display using st.markdown to render the bold text
        st.markdown(display_df.to_markdown(index=False), unsafe_allow_html=True)

        # Alternative simpler display using st.dataframe (doesn't easily support bolding specific cells):
        # st.dataframe(results_df[['EST_NAME', 'EST_ID', 'NEW OFFICE', 'NEW TASK ID', 'NEW ENF TASK']], hide_index=True, use_container_width=True)

    elif search_term:
        st.info("No establishments found matching your search term.")
    # else: (Optional: message when search is empty and nothing is shown)
        # st.info("Enter a search term above to find establishments.")

elif os.path.exists(CSV_FILE):
     st.warning("Data could not be loaded, please check the file format or content.")
# else: (Error message already shown by load_data if file not found)

# --- Footer/Info ---
st.divider()
st.caption("Data sourced from: barkatpura-establishments.csv")