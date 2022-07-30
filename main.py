from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize
from threading import Thread
import logging


def handle_images(filename: Path, target_folder: Path):
    if filename.exists():
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize(filename.name))


def handle_music(filename: Path, target_folder: Path):
    if filename.exists():
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize(filename.name))


def handle_video(filename: Path, target_folder: Path):
    if filename.exists():
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize(filename.name))


def handle_documents(filename: Path, target_folder: Path):
    if filename.exists():
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    if filename.exists():
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path):
    if filename.exists():
        # Создаем папку для архивов
        target_folder.mkdir(exist_ok=True, parents=True)
        #  Создаем папку куда распаковываем архив
        # Берем суффикс у файла и убираем replace(filename.suffix, '')
        folder_for_file = target_folder / \
                          normalize(filename.name.replace(filename.suffix, ''))
        #  создаем папку для архива с именем файла

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
    for i in range(1, 4):
        thread = Thread(target=parser.connect, args=(folder,))
        thread.start()
        logging.debug(f'Start thread {i} in folder {folder.resolve()}')

    for file in parser.JPEG_IMAGES:
        handle_images(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_images(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_images(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_images(file, folder / 'images' / 'SVG')
    for file in parser.MP3_AUDIO:
        handle_music(file, folder / 'audio' / 'MP3')
    for file in parser.OGG_AUDIO:
        handle_music(file, folder / "audio" / 'OGG')
    for file in parser.WAV_AUDIO:
        handle_music(file, folder / "audio" / 'WAV')
    for file in parser.AMR_AUDIO:
        handle_music(file, folder / "audio" / 'AMR')
    for file in parser.AVI_VIDEO:
        handle_video(file, folder / "video" / 'AVI')
    for file in parser.MP4_VIDEO:
        handle_video(file, folder / "video" / 'MP4')
    for file in parser.MOV_VIDEO:
        handle_video(file, folder / "video" / 'MOV')
    for file in parser.MKV_VIDEO:
        handle_video(file, folder / "video" / 'MKV')
    for file in parser.DOC_DOCUMENTS:
        handle_documents(file, folder / "documents" / 'DOC')
    for file in parser.DOCX_DOCUMENTS:
        handle_documents(file, folder / "documents" / 'DOCX')
    for file in parser.TXT_DOCUMENTS:
        handle_documents(file, folder / "documents" / 'TXT')
    for file in parser.PDF_DOCUMENTS:
        handle_documents(file, folder / "documents" / 'PDF')
    for file in parser.XLSX_DOCUMENTS:
        handle_documents(file, folder / "documents" / 'XLSX')
    for file in parser.PPTX_DOCUMENTS:
        handle_documents(file, folder / "documents" / 'PPTX')

    for file in parser.OTHER:
        handle_other(file, folder / 'OTHERS')
    for file in parser.ARCHIVES:
        handle_archive(file, folder / 'archives')

    # Выполняем реверс списка для того, чтобы все папки удалить.
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


if __name__ == '__main__':
    if sys.argv[1]:
        logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())
