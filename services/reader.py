from c2pa import C2paError, Reader
import json
import streamlit as st


def read_content_credentials(file) -> bool:
    try:
        with Reader(file.type, file) as reader:
            # read the manifest store and load as dictionary
            st.session_state['manifest_store'] = json.loads(reader.json())
        return True
    except C2paError as ce:
        if ce.message.startswith("ManifestNotFound"):
            st.error("Manifest not found. Try uploading an image with Content Credentials.")
        else:
            st.error(ce)
    except Exception as e:
        st.error(e)
    return False
