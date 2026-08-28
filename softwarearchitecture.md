# Software architecture

This document explains the high-level design of the D2L ARC Extractor.

Components

- app/main.py
  - The NiceGUI application user interface.
  - Presents a file-upload control, type selection checkboxes and a process button.
  - Delegates archive processing to extractor.archiver.

- extractor/archiver.py
  - Contains the main logic `extract_and_rename` which:
    - Opens the uploaded zip archive (from bytes) using the standard `zipfile` module.
    - Iterates over entries and selects files matching the allowed extensions.
    - Uses helpers from `extractor.utils` to determine the cleaned subfolder middle token and a safe output zip name.
    - Writes all selected files into a new zip in-memory and returns its bytes and name.

- extractor/utils.py
  - Small utility functions for string cleaning and name sanitisation.

Data flow

1. User uploads a zip in the UI.
2. The UI reads the file bytes and calls `extract_and_rename` with a list of allowed extensions.
3. `extract_and_rename` processes the archive and returns a new zip as bytes.
4. The UI offers the resulting archive for download.

Notes on naming and rules

- Subfolder name extraction tries to be heuristic: split on hyphens, pick the token with alphabetic characters closest to the middle, then remove non-alphanumeric characters and spaces.
- Output zip names are sanitised by replacing non-alphanumeric sequences with underscores and appending `_extracted`.

Testing and extensibility

- The pure functions in extractor can be unit-tested easily by feeding sample zip bytes and verifying outputs.
- Adding new rules for name extraction (e.g. locale-aware name detection) can be done by modifying `clean_subfolder_middle_part`.

Security considerations

- The current implementation reads the uploaded zip file into memory. For very large archives this may use significant memory; for production deployments streaming or temporary-file-backed approaches are recommended.
- The app only supports `.zip` uploads; other archive formats (tar, 7z) are not implemented.

Deployment

- This is a small web app suitable for deployment on a server or container. The NiceGUI documentation has deployment guides for uvicorn/gunicorn.
