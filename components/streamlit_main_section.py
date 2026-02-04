import streamlit as st
from datetime import datetime


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
            if validation_state == "Valid":
                st.markdown(f"**Validation State**: :green-badge[:material/check: {validation_state}]")
            elif validation_state == "Invalid":
                validation_status = manifest_store.get("validation_status", [])
                st.markdown(f"**Validation State**: :red-badge[:material/block: {validation_state}]")
                for status in validation_status:
                    st.markdown(f"**Code**: {status.get("code")}")
                    st.markdown(f"**Explanation**: {status.get("explanation")}")

        with st.container(border=True):
            st.subheader("Signature Info", help="Signature information from active manifest.", anchor=False)
            # st.markdown(f"**alg**: {signature_info.get('alg')}")
            st.markdown(f"**Issuer**: {signature_info.get('issuer')}")
            st.markdown(f"**Name**: {signature_info.get('common_name')}")
            date_time = datetime.strptime(signature_info.get('time'), "%Y-%m-%dT%H:%M:%S%z")
            st.markdown(f"**Date**: {date_time.date().strftime("%b %-d, %Y")}")
    # display the image
    with col1:
        st.image(st.session_state.get('upload'))
