# Read the IPTC Digital Source Type Controlled Vocabulary
# https://cv.iptc.org/newscodes/digitalsourcetype/
#

import json
import os
import requests

NEWSCODES_URL = "https://cv.iptc.org/newscodes/digitalsourcetype/?lang=en-GB&format=json"

NEWSCODES_PATH = "./schema/cptall-en-GB.json"


def download_newscodes_json():
    try:
        # request newscodes json
        response = requests.get(NEWSCODES_URL)
        # check if the request was successful
        response.raise_for_status()
        # parse the JSON content into a dictionary
        data = response.json()
        # create the schema directory if it doesn't exist
        os.makedirs("./schema", exist_ok=True)
        # writte the data to the JSON file
        with open(NEWSCODES_PATH, 'w') as f:
            json.dump(data, f, indent=4)

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except IOError as e:
        print(f"Error writing to file: {e}")


if not os.path.exists("./schema/cptall-en-GB.json"):
    print("Downloading schema from IPTC web")
    download_newscodes_json()


with open("./schema/cptall-en-GB.json", "r") as file:
    news_codes = json.load(file)

NEWS_CODES_MAP = {}

for concept_set in news_codes.get("conceptSet", {}):
    NEWS_CODES_MAP[concept_set.get("uri")] = concept_set.get("prefLabel", {}).get("en-GB")

NEWS_CODES_DESCRIPTION_MAP = {}

for concept_set in news_codes.get("conceptSet", {}):
    NEWS_CODES_DESCRIPTION_MAP[concept_set.get("uri")] = concept_set.get("definition", {}).get("en-GB")
