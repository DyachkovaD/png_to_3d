from PIL import Image
import numpy as np
import timeit


def image_to_obj(input_image_path, output_obj_path, depth):
    """
    Преобразует чёрно-белое изображение в 3D объект на платформе в формате .obj.
    Объект формируется из чёрных пикселей.

    input_image_path - путь к входному файлу
    output_obj_path - путь к выходному файлу
    depth - высота объекта и платформы
    """

    # Открываем изображение и преобразуем его в массив numpy
    try:
        image = Image.open(input_image_path).convert('L')  # Открываем в оттенках серого
    except:
        print('Невозможно открыть изображение')

    pixels = np.array(image)

    # Получаем размеры изображения
    height, width = pixels.shape

    # Открываем файл для записи .obj
    with open(output_obj_path, 'w') as f:
        # Записываем ссылку на файл материалов
        f.write("mtllib materials.mtl\n")

        # Определяем координаты платформы
        platform_height = depth
        platform_vertices = [
            (0, 0, -platform_height),
            (width, 0, -platform_height),
            (width, height, -platform_height),
            (0, height, -platform_height),
            (0, 0, 0),
            (width, 0, 0),
            (width, height, 0),
            (0, height, 0),
        ]

        # Записываем вершины платформы
        for vertex in platform_vertices:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

        # Записываем грани платформы
        f.write("usemtl white\n")
        f.write("f 1 2 3 4\n")
        f.write("f 5 6 7 8\n")
        f.write("f 5 6 2 1\n")
        f.write("f 6 7 3 2\n")
        f.write("f 7 8 4 3\n")
        f.write("f 8 5 1 4\n")


        # Начальный индекс для вершин платформы
        vertex_index = 9

        # Проходим по каждому пикселю изображения
        for y in range(height):
            for x in range(width):
                pixel_value = pixels[y, x]
                if pixel_value == 0:  # Если пиксель черный
                    # Записываем вершины для куба
                    cube_vertices = [
                        (x, y, 0),
                        (x + 1, y, 0),
                        (x + 1, y + 1, 0),
                        (x, y + 1, 0),
                        (x, y, depth),
                        (x + 1, y, depth),
                        (x + 1, y + 1, depth),
                        (x, y + 1, depth)
                    ]

                    for vertex in cube_vertices:
                        f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

                    # Записываем грани куба
                    f.write("usemtl black\n")
                    f.write(f"f {vertex_index} {vertex_index + 1} {vertex_index + 2} {vertex_index + 3}\n")
                    f.write(f"f {vertex_index + 4} {vertex_index + 5} {vertex_index + 6} {vertex_index + 7}\n")
                    f.write(f"f {vertex_index} {vertex_index + 1} {vertex_index + 5} {vertex_index + 4}\n")
                    f.write(f"f {vertex_index + 1} {vertex_index + 2} {vertex_index + 6} {vertex_index + 5}\n")
                    f.write(f"f {vertex_index + 2} {vertex_index + 3} {vertex_index + 7} {vertex_index + 6}\n")
                    f.write(f"f {vertex_index + 3} {vertex_index} {vertex_index + 4} {vertex_index + 7}\n")

                    vertex_index += 8

    print('.obj файл создан')

# Пример использования
input_image_path = 'input.png'
output_obj_path = 'output.obj'

exec_time = timeit.timeit(lambda: image_to_obj(input_image_path, output_obj_path, 10), number=1)
print(f"Время выполнения: {exec_time:.10f} секунд")