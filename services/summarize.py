import streamlit as st
from collections import defaultdict
from newscodes import NEWS_CODES_DESCRIPTION_MAP


def summarize_origin_info(actions: list[dict]) -> str:

    res = []

    counts = defaultdict(int)

    for act in actions:
        counts[act.get('digitalSourceType')] += 1

    # st.write(counts)

    if len(counts) > 1:
        res.append("Created from multiple source types")

    for news_code, val in counts.items():
        res.append(NEWS_CODES_DESCRIPTION_MAP.get(news_code))

    return "/n".join(res)
