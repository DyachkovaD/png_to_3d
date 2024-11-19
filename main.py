import numpy as np
from PIL import Image
from stl import mesh
import segno
import timeit


def make_qr(url: str, scale=10, border=0) -> None:
    """
    Делает QR-код в формате png из строки
    url - строка для кодирования
    scale - размер QR изображения
    border - границы QR кода
    """

    qr = segno.make_qr(url)
    qr.save(
        'qr_code.png',
        scale=scale,
        border=border,
    )

    print('QR-код создан')


def png_qr_to_slt(png_file, depth, floor) -> None:
    """
    Преобразует QR-код в формате png
    в документ в формате slt с высотой QR-кода depth
    """

    # Загрузите изображение QR-кода в 2D формате
    img = png_file.convert('L')  # конвертируем в черно-белый формат

    # Определите размеры изображения
    width, height = img.size

    # Создайте массив для хранения треугольников
    faces = []

    # Итерируемся по пикселям изображения
    for x in range(width):
        for y in range(height):

            # Создаем подложку
            v1 = np.array([x, y, 0])
            v2 = np.array([x + 1, y, 0])
            v3 = np.array([x, y + 1, 0])
            v4 = np.array([x + 1, y + 1, 0])
            v5 = np.array([x, y, -floor])
            v6 = np.array([x + 1, y, -floor])
            v7 = np.array([x, y + 1, -floor])
            v8 = np.array([x + 1, y + 1, -floor])
            base_triangles = np.array([
                [v1, v2, v3],
                [v2, v4, v3],
                [v5, v6, v7],
                [v6, v8, v7],
                [v1, v2, v6],
                [v1, v6, v5],
                [v1, v3, v7],
                [v1, v7, v5],
                [v2, v4, v8],
                [v2, v8, v6],
                [v3, v4, v8],
                [v3, v8, v7],
            ])
            faces.extend(base_triangles)

            # Если пиксель тёмный, выдвигаем его на заданную высоту
            if img.getpixel((x, y)) < 128:
                # Добавляем вершины для треугольников
                v1 = np.array([x, y, 0])
                v2 = np.array([x+1, y, 0])
                v3 = np.array([x, y+1, 0])
                v4 = np.array([x+1, y+1, 0])
                v5 = np.array([x, y, depth])
                v6 = np.array([x+1, y, depth])
                v7 = np.array([x, y+1, depth])
                v8 = np.array([x+1, y+1, depth])

                # Добавляем треугольники
                triangles = np.array([
                    [v1, v2, v3],
                    [v2, v4, v3],
                    [v5, v6, v7],
                    [v6, v8, v7],
                    [v1, v2, v6],
                    [v1, v6, v5],
                    [v1, v3, v7],
                    [v1, v7, v5],
                    [v2, v4, v8],
                    [v2, v8, v6],
                    [v3, v4, v8],
                    [v3, v8, v7],
                ])

                # Добавляем треугольники в массив
                faces.extend(triangles)

    try:
        # Создаем 3D-модель на основе массива вершин
        m = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
        m.vectors = faces

        # Сохраняем 3D-модель в формате STL
        m.save('qr_code_3d.stl')
    except Exception:
        print('Не удалось создать модель')
    else:
        print(f".stl файл создан")


make_qr('https://www.python.org/')
img = Image.open('qr_code.png')

exec_time = timeit.timeit(lambda: png_qr_to_slt(img, 10, 10), number=1)
print(f"Время выполнения: {exec_time:.10f} секунд")

