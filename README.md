# Content Credentials Reader

A Streamlit application designed to inspect, summarize, and visualize Content Credentials (C2PA) embedded in digital files.

This tool goes beyond simple metadata extraction; it traverses the manifest store to determine the true origin of an asset, identifying whether it was created by a camera, artificial intelligence, software, or a composite of multiple sources.

## Features

* **Deep Origin Traversal**: Navigates the C2PA "ingredient" graph to find the original creation events, not just the most recent edit.
* **Human-Readable Summaries**: Maps complex technical URIs (like http://cv.iptc.org/newscodes/digitalsourcetype/algorithmicMedia) to clear descriptions (e.g., "Created by Artificial Intelligence") using the IPTC Digital Source Type vocabulary.
* **Visual Metrics**: Displays key metrics such as the number of ingredients, signing validations, and specific AI usage indicators.
* **Detailed Inspection**: Provides a raw view of the manifest actions and assertions for deeper technical analysis.

## How It Works

Content Credentials (C2PA) store data in a graph structure (Manifest Store). A single file might have a long history of edits (crops, filters, re-encodings), each represented as a "manifest".

This application performs a Breadth-First Search (BFS) starting from the active manifest of the uploaded file. It looks backwards through the chain of "ingredients" (parent files) to find actions tagged as c2pa.created.

By aggregating these creation events, the tool answers the fundamental question: "Where did this content actually come from?"

## Installation

### Prerequisites

* Python 3.10+
* pip


### Setup

1. Clone the repository:

    ```commandline
    git clone https://github.com/peterjakubowski/Content-Credentials-Reader.git
    cd content-credentials-reader
    ```

2. Create a virtual environment (optional but recommended):
    ```commandline
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```commandline
    pip install -r requirements.txt
    ```

### Usage

1. Run the Streamlit app:
    ```commandline
   streamlit run app.py
   ```

2. Open your browser:

    The application will typically be available at http://localhost:8501.

3. Upload a file:

    Drag and drop an image (JPEG, PNG, WEBP, AVIF) or other supported file types to see its credentials.

### Technology Stack

* [Streamlit](https://docs.streamlit.io/): For the interactive web interface.
* [c2pa-python](https://github.com/contentauth/c2pa-python): The core library for parsing and validating C2PA manifests.
* Python 3: Backend logic for graph traversal and summarization.

