import streamlit as st
from services.search import get_actions_history
import pandas as pd
from newscodes import NEWS_CODES_MAP


def streamlit_actions_section():
    # get the manifest store from the session state
    manifest_store = st.session_state.get("manifest_store")
    # reference the manifests
    manifests = manifest_store.get('manifests', {})
    # reference the active manifest by its label
    active_manifest_label = manifest_store.get('active_manifest')

    actions = get_actions_history(active_manifest_label, manifests)

    df = pd.DataFrame(actions)

    df['digitalSourceType'] = df['digitalSourceType'].map(NEWS_CODES_MAP)


    # RECENT ACTIONS SECTION - 1 COLUMN
    with st.container(border=True):
        st.subheader("Actions History", help="History of all actions from the manifests in the manifest store.", anchor=False)
        st.dataframe(df, hide_index=True)

    # st.write(manifest_store)
