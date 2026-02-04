import streamlit as st
from services.search import find_asset_origin
from services.summarize import summarize_origin_info
from newscodes import NEWS_CODES_MAP
import pandas as pd


def streamlit_origin_section():

    # get the manifest store from the session state
    manifest_store = st.session_state.get("manifest_store")
    # reference the manifests
    manifests = manifest_store.get('manifests', {})
    # reference the active manifest by its label
    active_manifest_label = manifest_store.get('active_manifest')
    # search through the manifests for the moment of origin
    origin = find_asset_origin(active_manifest_label, manifests)
    # summarize the origin information
    origin_summary = summarize_origin_info(origin)
    df = pd.DataFrame(origin)
    if 'digitalSourceType' in df.columns:
        df['digitalSourceType'] = df['digitalSourceType'].map(NEWS_CODES_MAP)

    # ORIGIN SECTION - 1 COLUMN
    with st.container(border=True):
        st.subheader("Origin Summary", help="Information about the origins of the asset and how it was created.",
                     anchor=False)
        st.write(origin_summary)
        st.dataframe(df, hide_index=True)
