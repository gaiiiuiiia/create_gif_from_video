import numpy as np
import cv2
import os
import shutil


def ask_choice():
    answer = input('Делаем GIF или видео?.. (введите 1 или 2 или 0 для выхода)... ')
    while answer not in (['0', '1', '2', '\n']):
        answer = input('Делаем GIF или видео?.. (введите 1 или 2 или 0 для выхода)... ')

    return answer


PROGRAM_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
FRAMES_FOLDER_NAME = PROGRAM_DIRECTORY + r"\created_frames"

VIDEO_FILE = PROGRAM_DIRECTORY + "\\" + input('Введите название видео файла (напр. video123.mp4)...')

# поиск индекса последнего кадра
cap = cv2.VideoCapture(VIDEO_FILE)
i = 0
ret = cap.read()[0]
while ret:
    i += 1
    ret = cap.read()[0]
LAST_FRAME = i  # последний кадр

cap = cv2.VideoCapture(VIDEO_FILE)

frames = [cap.read()[1] for i in range(LAST_FRAME)]

# создание папки, в кот будут сохранены фреймы.
# если она уже существует, то будет пересоздана
try:
    os.mkdir(FRAMES_FOLDER_NAME)
except FileExistsError:
    shutil.rmtree(FRAMES_FOLDER_NAME)
    os.mkdir(FRAMES_FOLDER_NAME)

for n, frame in enumerate(frames, 1):
    cv2.imwrite(FRAMES_FOLDER_NAME + r"\frame" + str(n) + ".jpg", frame)

print('Посмотрите и выберите в папке' + FRAMES_FOLDER_NAME + '\n'
      'первый и последний кадры')

START_FRAME = int(input('Первый фрейм... '))
END_FRAME = int(input('Последний фрейм... '))

answer = ask_choice()

if answer == '1':
    # делаем gif
    import imageio
    with imageio.get_writer(PROGRAM_DIRECTORY + r"\gif_image.gif",
                            mode = 'I',
                            duration = 0.2,
                            ) as writer:
        images = [imageio.imread(FRAMES_FOLDER_NAME + r"\frame" + str(frame_num) + ".jpg") for
                                 frame_num in range(START_FRAME, END_FRAME + 1)]
        for im in images:
            writer.append_data(im)
elif answer == '2':
    # делаем видео
    images = [cv2.imread(FRAMES_FOLDER_NAME + r"\frame" + str(frame_num) + ".jpg") for
                         frame_num in range(START_FRAME, END_FRAME + 1)]
    writer = cv2.VideoWriter(PROGRAM_DIRECTORY + r"\video.avi",
                             cv2.VideoWriter_fourcc(*'XVID'),  # codec
                             10.0,  # fps
                             (images[0].shape[1], images[0].shape[0]),
                             isColor = True,
                             )
    for im in images:
        writer.write(im)
        
    writer.release()
else:
    shutil.rmtree(FRAMES_FOLDER_NAME)
    print('Выход из программы.')
    sys.exit()

print('Успешно завершено! \n'
      'результат в \n ',
      PROGRAM_DIRECTORY)

shutil.rmtree(FRAMES_FOLDER_NAME)  # удаление папки с кадрами
