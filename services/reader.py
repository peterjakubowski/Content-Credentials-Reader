from c2pa import C2paError, Reader
import json
import streamlit as st
import c2pa
import urllib.request


# This example shows how to read a C2PA manifest embedded in a media file, and validate
# that it is trusted according to the official trust anchor certificate list.
# The output is printed as prettified JSON.

TRUST_ANCHORS_URL = "https://contentcredentials.org/trust/anchors.pem"


def load_trust_anchors():
    try:
        with urllib.request.urlopen(TRUST_ANCHORS_URL) as response:
            anchors = response.read().decode('utf-8')
        settings = {
            "verify": {
                "verify_trust": False,
                "verify_cert_anchors": True
            },
            "trust": {
                "trust_anchors": anchors
            }
        }
        c2pa.load_settings(settings)
    except Exception as e:
        print(f"Warning: Could not load trust anchors from {TRUST_ANCHORS_URL}: {e}")


def read_content_credentials(file) -> bool:
    try:
        load_trust_anchors()
        with Reader(file.type, file) as reader:
            # read the manifest store and load as dictionary
            st.session_state['manifest_store'] = json.loads(reader.json())
        return True
    except C2paError as ce:
        if ce.message.startswith("ManifestNotFound"):
            st.error("Manifest not found. Try uploading an image with Content Credentials.")
        else:
            st.error(f"Error: {ce.message}")
    except Exception as e:
        st.error(e)
    return False
