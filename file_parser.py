import sys
from pathlib import Path
from main import main

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
OTHER = []
ARCHIVES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []


REGISTER_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,
    'ZIP': ARCHIVES,
    "GZ": ARCHIVES,
    "TAR": ARCHIVES,
    "OGG": OGG_AUDIO,
    "WAV": WAV_AUDIO,
    "AMR": AMR_AUDIO,
    "AVI": AVI_VIDEO,
    "MP4": MP4_VIDEO,
    "MOV": MOV_VIDEO,
    "MKV": MKV_VIDEO,
    "DOC": DOC_DOCUMENTS,
    "DOCX": DOCX_DOCUMENTS,
    "TXT": TXT_DOCUMENTS,
    "PDF": PDF_DOCUMENTS,
    "XLSX": XLSX_DOCUMENTS,
    "PPTX": PPTX_DOCUMENTS
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()
work_folder = Path('.')


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def connect(folder: Path):
    fullname = ''
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'OTHERS'):
                FOLDERS.append(item)
                connect(item)
            continue
        print(item.name)
        ext = get_extension(item.name)
        fullname = folder / item.name
        if not ext:
            OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(fullname)
            except KeyError:
                UNKNOWN.add(ext)
                OTHER.append(fullname)

    return main(folder)
