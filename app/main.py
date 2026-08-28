"""
NiceGUI web application to extract specific file types from an uploaded archive (zip).

EN-ZA documentation and strings.
"""
from nicegui import ui, Client, app
from extractor.archiver import extract_and_rename


def _on_process(file, allowed_types, status):
    # file is a TemporaryUploadedFile-like object from NiceGUI
    if not file:
        status.set_text('No file uploaded.')
        return
    status.set_text('Reading uploaded archive...')
    data = file.read()
    status.set_text('Processing archive...')
    try:
        result_bytes, result_name = extract_and_rename(data, allowed_types)
    except Exception as e:
        status.set_text(f'Error: {e}')
        return
    status.set_text('Finished. Preparing download...')

    # create a downloadable link
    ui.link(result_name, on_click=lambda: Client().download(result_bytes, result_name)).props('target=_self')
    status.set_text(f'Ready — download {result_name}')


with ui.card().tight():
    ui.label('D2L ARC Extractor').classes('text-h5')
    ui.markdown(
        'Upload a zip archive. The app will search all subfolders, extract only the selected file types, '
        'rename each file using a cleaned subfolder middle part and re-archive the extracted files into a new zip.'
    )

    upload = ui.upload(auto_upload=False).props('max-files=1').accept('.zip')

    types = ui.row()
    pdf_cb = ui.checkbox('PDF (.pdf)', value=True)
    docx_cb = ui.checkbox('DOCX (.docx)', value=True)
    pptx_cb = ui.checkbox('PPTX (.pptx)', value=False)
    types.add(pdf_cb); types.add(docx_cb); types.add(pptx_cb)

    status = ui.label('Ready')

    def on_click_process():
        uploaded = upload.value
        if not uploaded:
            status.set_text('Please upload a zip file first.')
            return
        file = uploaded[0]
        allowed = []
        if pdf_cb.value: allowed.append('pdf')
        if docx_cb.value: allowed.append('docx')
        if pptx_cb.value: allowed.append('pptx')
        _on_process(file, allowed, status)

    ui.button('Process archive', on_click=on_click_process)


if __name__ == '__main__':
    ui.run(title='D2L ARC Extractor')
