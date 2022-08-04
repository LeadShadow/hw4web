from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import shutil
import file_parser as parser
from normalize import normalize
import logging


def handle_file(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / \
                          normalize(filename.name.replace(filename.suffix, ''))

    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                                  str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Обман - это не архив {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Не удалось удалить папку {folder}')


def main(folder: Path):
    for file in parser.JPEG_IMAGES:
        handle_file(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_file(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_file(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_file(file, folder / 'images' / 'SVG')
    for file in parser.MP3_AUDIO:
        handle_file(file, folder / 'audio' / 'MP3')
    for file in parser.OGG_AUDIO:
        handle_file(file, folder / "audio" / 'OGG')
    for file in parser.WAV_AUDIO:
        handle_file(file, folder / "audio" / 'WAV')
    for file in parser.AMR_AUDIO:
        handle_file(file, folder / "audio" / 'AMR')
    for file in parser.AVI_VIDEO:
        handle_file(file, folder / "video" / 'AVI')
    for file in parser.MP4_VIDEO:
        handle_file(file, folder / "video" / 'MP4')
    for file in parser.MOV_VIDEO:
        handle_file(file, folder / "video" / 'MOV')
    for file in parser.MKV_VIDEO:
        handle_file(file, folder / "video" / 'MKV')
    for file in parser.DOC_DOCUMENTS:
        handle_file(file, folder / "documents" / 'DOC')
    for file in parser.DOCX_DOCUMENTS:
        handle_file(file, folder / "documents" / 'DOCX')
    for file in parser.TXT_DOCUMENTS:
        handle_file(file, folder / "documents" / 'TXT')
    for file in parser.PDF_DOCUMENTS:
        handle_file(file, folder / "documents" / 'PDF')
    for file in parser.XLSX_DOCUMENTS:
        handle_file(file, folder / "documents" / 'XLSX')
    for file in parser.PPTX_DOCUMENTS:
        handle_file(file, folder / "documents" / 'PPTX')

    for file in parser.OTHER:
        handle_other(file, folder / 'OTHERS')
    for file in parser.ARCHIVES:
        handle_archive(file, folder / 'archives')

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


def scan_folder(folder: Path):
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(parser.connect, folder)]

        for _ in as_completed(futures):
            pass


def get_value(*args):
    if len(args) < 1:
        return 'Please enter a folder name'

    if args[0]:
        parser.FOLDERS = []
        parser.work_folder = Path(args[0])
        logging.debug(f'Scan {parser.work_folder}')
        if not parser.work_folder.exists():
            logging.debug('Folder not exist')

        scan_folder(parser.work_folder.resolve())
        logging.debug(f'Successful in {parser.work_folder.resolve()}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    folder_for_scan = Path(input(">>> "))
    logging.debug(f'Start in folder {folder_for_scan.resolve()}')
    get_value(folder_for_scan)
