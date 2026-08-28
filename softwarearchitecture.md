# Software architecture

This document explains the high-level design of the D2L ARC Extractor.

Components

- app/main.py
  - The NiceGUI application user interface.
  - Presents a file-upload control, type selection checkboxes and a process button.
  - Delegates archive processing to extractor.archiver.

- extractor/archiver.py
  - Contains the main logic `extract_and_rename` which:
    - Accepts bytes, a file-like, or a path-like input.
    - For inputs smaller than `max_in_memory` it processes using an in-memory BytesIO.
    - For larger inputs it writes the content to a temporary file and uses zipfile on disk.
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

Large-archive strategy

The system supports two modes:
- In-memory mode: Fast and suitable for small uploads (default threshold 50 MiB).
- Disk-backed streaming mode: For uploads larger than the threshold the archive is written to a temporary file and processed from disk to avoid large memory usage.

Testing and extensibility

- The pure functions in extractor can be unit-tested easily by feeding sample zip bytes and verifying outputs. Unit tests are included and executed in CI.
- Adding new rules for name extraction (e.g. locale-aware name detection) can be done by modifying `clean_subfolder_middle_part`.

Sanitisation example

- Example: `ModuleCode_ICE00_ICETopic_ST12345678.pdf` inside `110328-506377 - Any Ntshonga - 14 August 2026 438 PM` becomes `ModuleCode_ICE0#_ICETopic_ST12345678_AnyNtshonga.pdf` (demonstrates masking part of module code to help de-identify sensitive components).

Security considerations

- In disk-backed mode uploaded archive bytes are written to a temporary file which is promptly deleted after processing. Ensure the environment running the app has appropriate access controls and temporary directory hygiene.

Deployment

- The GitHub Actions workflow `ci_deploy.yml` will run tests and push the repository contents to the configured HuggingFace Space when commits are pushed to `main`.
