import numpy as np
import cv2
import os
import shutil
import sys
from constants import PROGRAM_DIRECTORY, FRAMES_FOLDER_NAME, FRAMES_COUNT


def ask_choice():
    answer = input('Делаем GIF или видео?.. (введите 1 или 2 или 0 для выхода)... ')
    while answer not in (['0', '1', '2', '\n']):
        answer = input('Делаем GIF или видео?.. (введите 1 или 2 или 0 для выхода)... ')

    return answer


def ask_user(message: str, correct_answers: list):

    if 'exit' not in correct_answers:
        correct_answers.append('exit')

    answer = input(message)

    while answer not in correct_answers:
        answer = input(message)

    return answer


def get_video_filename(path_to_file: str = False):

    path_to_file = input('Введите путь к файлу...') if not path_to_file else path_to_file

    while not is_video_file(path_to_file):

        if path_to_file == 'exit':
            sys.exit()

        path_to_file = input('Введите путь к файлу...')

    return path_to_file


def is_video_file(path: str):

    video_ext = [
        '.mp4',
    ]

    return os.path.splitext(path)[1] in video_ext


def get_frames(file_name):

    cap = cv2.VideoCapture(file_name)
    frames = []

    flag, frame = cap.read()
    while flag:
        frames.append(frame)
        flag, frame = cap.read()

    return frames


def create_frames_folder():
    try:
        os.mkdir(FRAMES_FOLDER_NAME)
    except FileExistsError:
        shutil.rmtree(FRAMES_FOLDER_NAME)
        os.mkdir(FRAMES_FOLDER_NAME)


def save_frames(frames):
    """
    Сохраняет фреймы в папку. количество фреймов указано в константе FRAMES_COUNT
    :return:
    """
    len_frames = len(frames)
    step = len(frames) // FRAMES_COUNT

    for index, frame in enumerate(range(1, len_frames + 1, step), 1):
        cv2.imwrite(FRAMES_FOLDER_NAME + r"\frame" + str(index) + ".jpg", frames[frame])


def main():

    # video_filename = get_video_filename()
    video_filename = get_video_filename(r"E:\myfiles\Учебные файлы\20210108_194515.mp4")

    create_frames_folder()

    frames = get_frames(video_filename)

    save_frames(frames)


if __name__ == "__main__":
    main()

