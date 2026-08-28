"""
Utility helpers for name cleaning and sanitisation.
"""
import re
import os


def clean_subfolder_middle_part(dirpath: str) -> str:
    """Given a directory path from inside the archive, attempt to extract a 'middle part'
    that typically contains a person's name or distinguishing text.

    Strategy:
    - Split the last directory component by hyphen '-' and by ' - ' and pick a token that contains
      alphabetic characters and is not purely numeric. Prefer tokens in the middle of the split.
    - Remove non-alphanumeric characters and collapse spaces.
    - Return an empty string if nothing reasonable is found.

    Examples:
    - "110328-506377 - Athobe Ntshonga - 14 August 2026 438 PM" -> "AthobeNtshonga"
    - "some/other/folder" -> "folder"
    """
    if not dirpath:
        return ''
    # Use the last directory part
    last = os.path.basename(dirpath.rstrip('/\\'))
    if not last:
        return ''

    # Split on hyphen and choose a middle token which has letters
    tokens = [t.strip() for t in re.split(r"[-–—]", last) if t.strip()]
    # If tokens look like date/time segments, prefer tokens containing letters
    candidates = [t for t in tokens if re.search(r"[A-Za-z]", t)]
    chosen = ''
    if len(candidates) >= 1:
        # If there's a clear 'middle' token, choose it; else choose the first candidate
        mid_index = len(tokens) // 2
        # Find nearest candidate to the middle
        best = None
        best_dist = None
        for c in candidates:
            try:
                idx = tokens.index(c)
            except ValueError:
                continue
            dist = abs(idx - mid_index)
            if best is None or dist < best_dist:
                best = c
                best_dist = dist
        chosen = best or candidates[0]
    else:
        # fallback to the last token
        chosen = tokens[-1] if tokens else last

    # Clean chosen token: keep letters and digits only, remove spaces
    cleaned = re.sub(r"[^0-9A-Za-z]", '', chosen)
    return cleaned


def sanitize_zip_name(name: str) -> str:
    """Sanitise a filename (without forcing extension) for use as a zip name.
    Replace non-alphanumeric sequences with underscore and collapse multiples.
    """
    base = os.path.splitext(name)[0]
    # Replace any sequence of non-alphanumeric with underscore
    s = re.sub(r"[^0-9A-Za-z]+", '_', base)
    s = re.sub(r"_+", '_', s).strip('_')
    return s or 'extracted'
