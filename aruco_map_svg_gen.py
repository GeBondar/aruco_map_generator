import cv2
import svgwrite
import numpy as np

def parse_txt_file(file_path):
    """Считывает файл и возвращает список маркеров."""
    markers = []
    with open(file_path, "r") as file:
        for line in file:
            # Пропускаем пустые строки и заголовок
            if line.strip() and not line.startswith("#"):
                parts = line.split()
                markers.append({
                    "id": int(parts[0]),
                    "length": float(parts[1]),
                    "x": float(parts[2]),
                    "y": float(parts[3]),
                    "z": float(parts[4]),  # Не используется для 2D-карты, но сохраняем
                    "rot_z": float(parts[5]),  # Не используется в данном скрипте
                    "rot_y": float(parts[6]),  # Не используется в данном скрипте
                    "rot_x": float(parts[7])   # Не используется в данном скрипте
                })
    return markers

def generate_aruco_marker(dictionary, marker_id, marker_size):
    """Генерирует ArUco маркер как NumPy-массив."""
    marker_image = np.zeros((marker_size, marker_size), dtype=np.uint8)
    cv2.aruco.generateImageMarker(dictionary, marker_id, marker_size, marker_image, 1)
    return marker_image

def draw_marker_on_svg_optimized(dwg, marker_image, position, size):
    """Добавляет маркер в SVG-документ, группируя черные пиксели."""
    x, y = position
    scale = size / marker_image.shape[0]

    # Добавляем фон
    dwg.add(dwg.rect(
        insert=(x, y),
        size=(size, size),
        fill="white"
    ))

    # Объединяем черные пиксели в группы
    visited = np.zeros(marker_image.shape, dtype=bool)
    for i in range(marker_image.shape[0]):
        for j in range(marker_image.shape[1]):
            if marker_image[i, j] == 0 and not visited[i, j]:  # Черный пиксель
                # Определяем размер прямоугольника
                rect_width = 1
                rect_height = 1

                # Проверяем ширину
                while j + rect_width < marker_image.shape[1] and marker_image[i, j + rect_width] == 0 and not visited[i, j + rect_width]:
                    rect_width += 1

                # Проверяем высоту
                is_rect_valid = True
                while is_rect_valid and i + rect_height < marker_image.shape[0]:
                    for k in range(rect_width):
                        if marker_image[i + rect_height, j + k] != 0 or visited[i + rect_height, j + k]:
                            is_rect_valid = False
                            break
                    if is_rect_valid:
                        rect_height += 1

                # Помечаем пиксели как посещенные
                for m in range(rect_height):
                    for n in range(rect_width):
                        visited[i + m, j + n] = True

                # Добавляем прямоугольник
                dwg.add(dwg.rect(
                    insert=(x + j * scale, y + i * scale),
                    size=(rect_width * scale, rect_height * scale),
                    fill="black"
                ))

def main(input_file, output_file):
    # Параметры
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    marker_size = 100  # Размер маркера в пикселях для генерации (высокое разрешение)
    scale = 1000  # Коэффициент для преобразования координат в пиксели
    svg_size = 2000  # Размер SVG-документа
    offset_x, offset_y = svg_size / 2, svg_size / 2

    # Считываем маркеры из файла
    markers = parse_txt_file(input_file)

    # Настройка SVG
    dwg = svgwrite.Drawing(output_file, size=(svg_size, svg_size), profile="tiny")

    # Генерация и добавление маркеров в SVG
    for marker in markers:
        marker_id = marker["id"]
        marker_length = marker["length"] * scale  # Преобразуем длину из метров в пиксели
        x = marker["x"] * scale + offset_x
        y = -marker["y"] * scale + offset_y
        marker_image = generate_aruco_marker(aruco_dict, marker_id, marker_size)
        draw_marker_on_svg_optimized(dwg, marker_image, (x - marker_length / 2, y - marker_length / 2), marker_length)

    # Сохранение SVG
    dwg.save()
    print(f"SVG файл успешно создан: {output_file}")

# Пример использования
if __name__ == "__main__":
    input_file = "C:\\Users\\George\\Desktop\\aruco_map.txt"  # Путь к текстовому файлу
    output_file = "C:\\Users\\George\\Desktop\\aruco_field_optimized.svg"  # Имя выходного SVG-файла
    main(input_file, output_file)
