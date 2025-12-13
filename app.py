import streamlit as st
import c2pa
from c2pa import C2paError
import json
from collections import deque


def read_content_credentials(_file) -> dict | None:
    try:
        with c2pa.Reader(file.type, _file) as reader:
            # read the manifest store and load as dictionary
            return json.loads(reader.json())
    except C2paError as ce:
        st.error(ce)
    except Exception as e:
        st.error(e)
    return None


def find_asset_origin(_active_manifest_label, _manifests) -> list[dict]:
    originals = []
    visited = {_active_manifest_label}
    q = deque([_active_manifest_label])
    while q:
        cur_label = q.popleft()
        cur_manifest = _manifests.get(cur_label)
        ingredients = cur_manifest.get('ingredients', [])
        if ingredients:
            for ingredient in ingredients:
                manifest = ingredient.get('active_manifest')
                if manifest and manifest in _manifests:
                    if manifest not in visited:
                        q.append(manifest)
                        visited.add(manifest)
                else:
                    originals.append(cur_label)  # this manifest likely contains a c2pa.created action
        else:
            originals.append(cur_label)

    res = []

    for ori in originals:
        assertions = _manifests.get(ori, {}).get('assertions')
        for ass in assertions:
            actions = ass.get('data', {}).get('actions', [])
            for act in actions:
                if act.get("action") == "c2pa.created":
                    data = {"action": act.get("action"),
                            "digitalSourceType": act.get("digitalSourceType"),
                            "description": act.get("description")}
                    if data not in res:
                        res.append(data)

    return res


def get_recent_actions(_active_manifest_label, _manifests) -> list[dict]:
    res = []

    assertions = _manifests.get(_active_manifest_label, {}).get('assertions')

    for ass in assertions:
        actions = ass.get('data', {}).get('actions', [])
        for act in actions:
            if act not in res:
                res.append(act)

    return res


st.title("Content Credentials Reader")

file = st.file_uploader(
    label="upload",
    label_visibility="hidden",
    accept_multiple_files=False,
    type=["jpg", "jpeg", "png", "tif"]
)

if file:
    manifest_store = read_content_credentials(file)
    # # check the validation state
    validation_state = manifest_store.get('validation_state')
    # reference the manifests
    manifests = manifest_store.get('manifests', {})
    # reference the active manifest by its label
    active_manifest_label = manifest_store.get('active_manifest')
    active_manifest = manifests.get(active_manifest_label, {})
    # get the signature info
    signature_info = active_manifest.get('signature_info')

    col1, col2, col3 = st.columns([0.3, 0.3, 0.3], border=False)

    with col1:
        st.metric("Manifests",
                  len(manifests),
                  border=True,
                  help="Content Credentials are kept in a C2PA manifest store. "
                  "A manifest store consists of one or more individual manifests, "
                  "each containing information about the asset. "
                  "The most recently-added manifest is called the active manifest."
                  )
    with col2:
        st.metric("Ingredients", sum([len(m.get("ingredients", [])) for _, m in manifests.items()]), border=True,
                  help="Total number of ingredients in all manifests.")
    with col3:
        st.metric("Actions",
                  sum([sum([len(a.get("data", {}).get("actions", [])) for a in m.get("assertions", [])]) for _, m in
                       manifests.items()]),
                  border=True,
                  help="An operation that an actor performs on an asset. "
                  """For example, "create," "embed," or "change contrast.""""")

    col1, col2 = st.columns([0.6, 0.4], border=False)

    with col2:
        # show the image
        st.image(file)

        with st.container(border=True, width="stretch"):
            # st.markdown("Validation State")
            if validation_state == "Valid":
                st.markdown(f"**Validation State**: :green-badge[:material/check: {validation_state}]",
                            help="Validation state")
            elif validation_state == "Invalid":
                st.markdown(f"**Validation State**: :red-badge[:material/block: {validation_state}]",
                            help="Validation state")
        with st.container(border=True):
            st.subheader("Signature Info", help="Signature information from active manifest.", anchor=False)
            # st.markdown(f"**alg**: {signature_info.get('alg')}")
            st.markdown(f"**Issuer**: {signature_info.get('issuer')}")
            st.markdown(f"**Name**: {signature_info.get('common_name')}")
            st.markdown(f"**Time**: {signature_info.get('time')}")

    with col1:

        with st.container(border=True):
            st.subheader("Origin Info", help="Information about the origins of the asset and how it was created.",
                         anchor=False)
            origin = find_asset_origin(active_manifest_label, manifests)
            for ori in origin:
                with st.container(border=True):
                    if 'action' in ori:
                        st.markdown(f"**Action**: {ori.get('action')}")
                    if 'digitalSourceType' in ori:
                        st.markdown(f"**Digital Source Type**: {ori.get('digitalSourceType')}")
                    if 'description' in ori:
                        st.markdown(f"**Description**: {ori.get('description')}")

        with st.container(border=True):
            st.subheader("Recent Actions", help="Recent actions from the active manifest.")
            actions = get_recent_actions(active_manifest_label, manifests)
            for act in actions:
                with st.container(border=True):
                    if act.get('action'):
                        st.markdown(f"**Action**: {act.get('action')}")
                    if act.get('digitalSourceType'):
                        st.markdown(f"**Digital Source Type**: {act.get('digitalSourceType')}")
                    if act.get('description'):
                        st.markdown(f"**Description**: {act.get('description')}")
    st.write(active_manifest)
