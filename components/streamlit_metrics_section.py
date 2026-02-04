import streamlit as st


def streamlit_metrics_section():

    # get the manifest store from the session state
    manifest_store = st.session_state.get("manifest_store")
    manifests = manifest_store.get('manifests', {})

    # METRICS SECTION - 3 COLUMNS
    col1, col2, col3 = st.columns([0.3, 0.3, 0.3], border=False)

    # count manifests
    with col1:
        st.metric("Manifests",
                  len(manifests),
                  border=True,
                  help="Content Credentials are kept in a C2PA manifest store. "
                       "A manifest store consists of one or more individual manifests, "
                       "each containing information about the asset. "
                       "The most recently-added manifest is called the active manifest."
                  )

    # count ingredients
    with col2:
        st.metric("Ingredients", sum([len(m.get("ingredients", [])) for _, m in manifests.items()]), border=True,
                  help="Ingredients are other assets used in the creation of the current asset.")

    # count actions
    with col3:
        st.metric("Actions",
                  sum([sum([len(a.get("data", {}).get("actions", [])) for a in m.get("assertions", [])]) for _, m in
                       manifests.items()]),
                  border=True,
                  help="An operation that an actor performs on an asset. "
                       """For example, created, edited, opened, or converted.""")
