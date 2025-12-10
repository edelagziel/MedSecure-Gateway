# import tempfile
# import shutil
# import pathlib

# def stage_file_temporarily(file):
#     """
#     Saves the uploaded file to a temporary file on disk.
#     Returns the path of the temp file.
#     """
#     suffix = pathlib.Path(file.filename).suffix if file.filename else ""

#     # Create a temporary file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#         shutil.copyfileobj(file.file, tmp)
#         temp_path = tmp.name

#     # Reset file pointer so other validations can still read the stream
#     file.file.seek(0)

#     return temp_path



# no need any mpre we have not temp an real file 