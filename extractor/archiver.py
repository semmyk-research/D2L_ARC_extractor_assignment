"""
Extractor package for archive handling.

Functions to parse zip archives, select files by extension, rename using subfolder middle part,
and produce a new zip archive containing only the extracted renamed files.

Follow DRY principles and keep pure functions to ease testing.
"""
from io import BytesIO
import zipfile
from pathlib import Path
import re
from .utils import clean_subfolder_middle_part, sanitize_zip_name


def extract_and_rename(zip_bytes: bytes, allowed_exts: list[str]) -> tuple[bytes, str]:
    """Process an input zip (as bytes), extract only files whose extension is in allowed_exts,
    rename extracted files according to the rule: originalname_middlepart.ext and
    return a new zip file as bytes and the suggested output filename.

    Parameters
    - zip_bytes: bytes of the uploaded zip file
    - allowed_exts: list of lowercase extensions without dot, e.g. ['pdf','docx']

    Returns
    - tuple(result_zip_bytes, result_zip_name)
    """
    # Normalise allowed extensions
    allowed = set(e.lower().lstrip('.') for e in allowed_exts)

    in_buf = BytesIO(zip_bytes)
    with zipfile.ZipFile(in_buf, 'r') as zin:
        # Collect candidate files
        files_to_write = []  # list of tuples (new_name, data_bytes)
        name_counts: dict[str, int] = {}

        for zi in zin.infolist():
            if zi.is_dir():
                continue
            filename = Path(zi.filename).name
            if not filename:
                continue
            ext = Path(filename).suffix.lstrip('.').lower()
            if ext not in allowed:
                continue

            # Determine subfolder (the directory part containing the file)
            parent = Path(zi.filename).parent
            dirpath = '' if str(parent) == '.' else str(parent)
            middle = clean_subfolder_middle_part(dirpath)

            base = Path(filename).stem
            new_base = f"{base}_{middle}" if middle else base
            # Avoid collisions
            count = name_counts.get(new_base, 0)
            if count:
                new_name = f"{new_base}_{count}.{ext}"
            else:
                new_name = f"{new_base}.{ext}"
            name_counts[new_base] = count + 1

            data = zin.read(zi.filename)
            files_to_write.append((new_name, data))

        # Try to obtain original archive filename (may be absent when reading bytes)
        try:
            original_name = zin.filename if hasattr(zin, 'filename') and zin.filename else 'extracted'
        except Exception:
            original_name = 'extracted'

    cleaned = sanitize_zip_name(original_name)
    result_name = f"{cleaned}_extracted.zip"

    out_buf = BytesIO()
    with zipfile.ZipFile(out_buf, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for new_name, data in files_to_write:
            zout.writestr(new_name, data)

    out_buf.seek(0)
    return out_buf.read(), result_name
