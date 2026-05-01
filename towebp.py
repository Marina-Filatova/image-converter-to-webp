import os
import sys
from PIL import Image
import argparse

def convert_images_to_webp(folder_path, quality=80):
    """
    Конвертирует все JPG и PNG изображения в папке в формат WebP
    """
    # Проверяем существование папки
    if not os.path.exists(folder_path):
        print(f"Ошибка: Папка '{folder_path}' не существует!")
        return False
    
    if not os.path.isdir(folder_path):
        print(f"Ошибка: '{folder_path}' не является папкой!")
        return False
    
    # Получаем список всех файлов в папке
    files = os.listdir(folder_path)
    
    # Фильтруем JPG и PNG файлы
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("В указанной папке не найдено JPG или PNG изображений!")
        return False
    
    # Разделяем файлы по типам для статистики
    jpg_files = [f for f in image_files if f.lower().endswith(('.jpg', '.jpeg'))]
    png_files = [f for f in image_files if f.lower().endswith('.png')]
    
    print(f"Найдено {len(image_files)} изображений для конвертации:")
    print(f"  - JPG: {len(jpg_files)} файлов")
    print(f"  - PNG: {len(png_files)} файлов")
    
    converted_count = 0
    
    for image_file in image_files:
        try:
            # Формируем полные пути к файлам
            image_path = os.path.join(folder_path, image_file)
            
            # Создаем имя для WebP файла (то же имя, но с расширением .webp)
            name_without_ext = os.path.splitext(image_file)[0]
            webp_file = f"{name_without_ext}.webp"
            webp_path = os.path.join(folder_path, webp_file)
            
            # Проверяем, не существует ли уже WebP файл
            if os.path.exists(webp_path):
                print(f"Файл {webp_file} уже существует, пропускаем...")
                continue
            
            # Открываем и конвертируем изображение
            with Image.open(image_path) as img:
                file_ext = os.path.splitext(image_file)[1].lower()
                
                # Обработка PNG изображений с прозрачностью
                if file_ext == '.png' and img.mode in ('RGBA', 'LA', 'P'):
                    # Для PNG с прозрачностью сохраняем прозрачность в WebP
                    if img.mode == 'P' and 'transparency' in img.info:
                        img = img.convert('RGBA')
                    elif img.mode == 'LA':
                        img = img.convert('RGBA')
                    
                    # Если изображение имеет прозрачность, сохраняем с поддержкой прозрачности
                    if img.mode == 'RGBA':
                        img.save(webp_path, 'WEBP', quality=quality, lossless=False)
                    else:
                        # PNG без прозрачности конвертируем в RGB
                        img = img.convert('RGB')
                        img.save(webp_path, 'WEBP', quality=quality)
                
                # Обработка JPG изображений
                elif file_ext in ('.jpg', '.jpeg'):
                    # Конвертируем в RGB если изображение в другом формате
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.save(webp_path, 'WEBP', quality=quality)
                
                else:
                    print(f"Неизвестный формат для файла {image_file}, пропускаем...")
                    continue
            
            print(f"Конвертирован: {image_file} -> {webp_file}")
            converted_count += 1
            
        except Exception as e:
            print(f"Ошибка при конвертации файла {image_file}: {str(e)}")
    
    print(f"\nКонвертация завершена! Успешно конвертировано {converted_count} файлов.")
    return True

def main():
    parser = argparse.ArgumentParser(description='Конвертирует JPG и PNG изображения в WebP формат')
    parser.add_argument('folder', help='Путь к папке с изображениями')
    parser.add_argument('--quality', '-q', type=int, default=80, 
                       help='Качество WebP изображения (0-100, по умолчанию 80)')
    
    args = parser.parse_args()
    
    # Проверяем корректность значения качества
    if args.quality < 0 or args.quality > 100:
        print("Ошибка: Качество должно быть в диапазоне от 0 до 100!")
        sys.exit(1)
    
    convert_images_to_webp(args.folder, args.quality)

if __name__ == "__main__":
    # Если скрипт запущен без аргументов, показываем справку
    if len(sys.argv) == 1:
        print("Использование: python towebp.py <путь_к_папке> [--quality ЧИСЛО]")
        print("Пример: python towebp.py /path/to/images/folder")
        print("Пример: python towebp.py /path/to/images/folder --quality 90")
        sys.exit(1)
    
    main()