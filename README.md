# D2L ARC Extractor

A NiceGUI web application that reads an uploaded archive (zip), parses all subfolders and extracts only specific file types (e.g. PDF, DOCX). Each extracted file is renamed using a cleaned part of its enclosing subfolder and all extracted files are re-archived into a new zip file.

This repository follows EN-ZA (English - South Africa) spelling conventions (which align with EN-GB for our purposes).

Usage

1. Install dependencies:

   python -m pip install -r requirements.txt

2. Run the app:

   python -m app.main

3. Open the UI at http://localhost:8080 and upload a zip file. Choose the file types to extract and press "Process archive". When ready, a download link appears.

How it works

- The app reads the uploaded zip file into memory.
- It iterates through all entries in the archive and selects files whose extensions match the chosen types.
- For each selected file the application determines a subfolder 'middle part' (attempting to pick the token that looks like a person's name), cleans it (removes spaces and non-alphanumeric characters) and appends it to the original filename, separated by an underscore. Example: `ITPP5112_ICE03_ITRolesTraits_ST10524387.pdf` inside `110328-506377 - Athobe Ntshonga - 14 August 2026 438 PM` becomes `ITPP5112_ICE03_ITRolesTraits_ST10524387_AthobeNtshonga.pdf`.
- All extracted files are written into a new zip archive and a download link is presented.

Design and code quality

- The code follows DRY principles by centralising archive logic in the `extractor` package.
- Pure functions are used where feasible and documented with docstrings.
- See `softwarearchitecture.md` for higher-level documentation.
