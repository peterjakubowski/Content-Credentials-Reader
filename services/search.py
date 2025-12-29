from collections import deque
from newscodes import NEWS_CODES_MAP


def find_asset_origin(active_manifest_label, manifests) -> list[dict]:
    res = []
    visited = {active_manifest_label}
    queue = deque([active_manifest_label])
    while queue:
        cur_label = queue.popleft()
        cur_manifest = manifests.get(cur_label)
        for assertion in cur_manifest.get('assertions', []):
            for action in assertion.get('data', {}).get('actions', []):
                if action.get("action") == "c2pa.created":
                    data = {"action": action.get("action"),
                            "digitalSourceType": action.get("digitalSourceType"),
                            "description": action.get("description")}
                    res.append(data)
        for ingredient in cur_manifest.get('ingredients', []):
            active_manifest = ingredient.get('active_manifest')
            if active_manifest and active_manifest in manifests:
                if active_manifest not in visited:
                    queue.append(active_manifest)
                    visited.add(active_manifest)

    return res


def get_recent_actions(active_manifest_label, manifests) -> list[dict]:
    res = []

    assertions = manifests.get(active_manifest_label, {}).get('assertions')

    for ass in assertions:
        actions = ass.get('data', {}).get('actions', [])
        for act in actions:
            data = {"action": act.get("action"),
                    "digitalSourceType": NEWS_CODES_MAP.get(act.get("digitalSourceType")),
                    "description": act.get("description")}
            # if data not in res:
            res.append(data)

    return res


def get_actions_history(active_manifest_label, manifests) -> list[dict]:
    res = []
    visited = {active_manifest_label}
    queue = deque([active_manifest_label])
    while queue:
        cur_label = queue.popleft()
        cur_manifest = manifests.get(cur_label)
        for assertion in cur_manifest.get('assertions', []):
            for action in assertion.get('data', {}).get('actions', []):
                data = {"action": action.get("action"),
                        "digitalSourceType": action.get("digitalSourceType"),
                        "description": action.get("description")}
                res.append(data)
        for ingredient in cur_manifest.get('ingredients', []):
            active_manifest = ingredient.get('active_manifest')
            if active_manifest and active_manifest in manifests:
                if active_manifest not in visited:
                    queue.append(active_manifest)
                    visited.add(active_manifest)

    return res