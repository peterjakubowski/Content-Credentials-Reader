import streamlit as st


def streamlit_main_section():

    # get the manifest store from the session state
    manifest_store = st.session_state.get("manifest_store")
    # # check the validation state
    validation_state = manifest_store.get('validation_state')
    # reference the manifests
    manifests = manifest_store.get('manifests', {})
    # reference the active manifest by its label
    active_manifest = manifests.get(manifest_store.get('active_manifest'), {})
    # get the signature info
    signature_info = active_manifest.get('signature_info')
    # MAIN SECTION - 2 COLUMNS
    col1, col2 = st.columns([0.5, 0.5], border=False)
    # show validation state and signature information
    with col2:
        with st.container(border=True, width="stretch"):
            # st.markdown("Validation State")
            if validation_state == "Valid":
                st.markdown(f"**Validation State**: :green-badge[:material/check: {validation_state}]")
            elif validation_state == "Invalid":
                st.markdown(f"**Validation State**: :red-badge[:material/block: {validation_state}]")
        with st.container(border=True):
            st.subheader("Signature Info", help="Signature information from active manifest.", anchor=False)
            # st.markdown(f"**alg**: {signature_info.get('alg')}")
            st.markdown(f"**Issuer**: {signature_info.get('issuer')}")
            st.markdown(f"**Name**: {signature_info.get('common_name')}")
            st.markdown(f"**Time**: {signature_info.get('time')}")
    # display the image
    with col1:
        st.image(st.session_state.get('upload'))
