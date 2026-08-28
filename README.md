---
title: D2L ARC Extractor
license: mit
sdk: docker
app_port: 7860
---

# D2L ARC Extractor

A NiceGUI web application that reads an uploaded archive (zip), parses all subfolders and extracts only specific file types (e.g. PDF, DOCX). Each extracted file is renamed using a cleaned part of its enclosing subfolder and all extracted files are re-archived into a new zip file.

This repository follows EN-ZA (English - South Africa) spelling conventions (which align with EN-GB for our purposes).

Usage

1. Install dependencies:

   python -m pip install -r requirements.txt

2. Run the app:

   python -m app.main

3. Open the UI at http://localhost:7860 and upload a zip file. Choose the file types to extract and press "Process archive". When ready, a download link appears.

CI / Deployment

This repository contains a GitHub Actions workflow that runs unit tests and (on successful tests) deploys the app to a HuggingFace Space at semmyk-research/D2L_ARC_extractor_assignment. To enable deployment, add a repository secret called `HF_TOKEN` containing a HuggingFace token with repo write permissions.

How it works

- The app reads the uploaded zip file into memory for small uploads, and switches to a disk-backed temporary file when archives exceed a configurable threshold (default 50 MiB). This keeps fast in-memory operation for small files while preventing excessive memory use for larger archives.
- It iterates through all entries in the archive and selects files whose extensions match the chosen types.
- For each selected file the application determines a subfolder 'middle part' (attempting to pick the token that looks like a person's name), cleans it (removes spaces and non-alphanumeric characters) and appends it to the original filename, separated by an underscore. Example: `ModuleCode_ICE00_ICETopic_ST12345678.pdf` inside `110328-506377 - Any Ntshonga - 14 August 2026 438 PM` becomes `ModuleCode_ICE0#_ICETopic_ST12345678_AnyNtshonga.pdf`.
- All extracted files are written into a new zip archive and a download link is presented.

HuggingFace Spaces Docker

This repository is prepared for deployment to a HuggingFace Space using the Docker SDK. The workflow will sync the repository to the configured Space and the included Dockerfile defines the container entrypoint.

To enable automatic deployment on push to `main` ensure you have created the target Space and added an HF token with write permissions as the repository secret `HF_TOKEN`.
