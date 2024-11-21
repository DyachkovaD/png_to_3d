import numpy as np
from PIL import Image
from stl import mesh
import timeit


def png_qr_to_slt(input_image_path, depth, floor) -> None:
    """
    Преобразует чёрно-белое изображение в 3D объект на платформе в формате .stl.
    Объект формируется из чёрных пикселей.

    png_file - путь к входному файлу
    output_obj_path - путь к выходному файлу
    depth - высота объекта и платформы
    """

    # Загрузите изображение QR-кода в 2D формате
    try:
        img = Image.open(input_image_path).convert('L')  # конвертируем в черно-белый формат
    except:
        print('Невозможно открыть изображение')

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
        m.save('output.stl')
    except Exception:
        print('Не удалось создать модель')
    else:
        print(f".stl файл создан")


input_image_path = 'input.png'

exec_time = timeit.timeit(lambda: png_qr_to_slt(input_image_path, 10, 10), number=1)
print(f"Время выполнения: {exec_time:.10f} секунд")

