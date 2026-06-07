"""
Модуль для массового переименования файлов по шаблону.
"""

import os


def rename_files(dir_path: str, old_pattern: str, new_pattern: str) -> dict:
    """
    Переименовывает файлы в директории, заменяя old_pattern на new_pattern.
    
    Args:
        dir_path: Путь к директории с файлами
        old_pattern: Паттерн для поиска в именах файлов
        new_pattern: Паттерн для замены
        
    Returns:
        dict: Статистика {'renamed': int, 'skipped': int, 'errors': int}
        
    Example:
        >>> rename_files("./photos", "IMG_", "Vacation_")
    """
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"Директория '{dir_path}' не существует.")
    
    if not os.path.isdir(dir_path):
        raise NotADirectoryError(f"'{dir_path}' — не директория.")
    
    renamed_count = 0
    skipped_count = 0
    error_count = 0
    
    for filename in os.listdir(dir_path):
        if old_pattern in filename:
            new_filename = filename.replace(old_pattern, new_pattern)
            old_path = os.path.join(dir_path, filename)
            new_path = os.path.join(dir_path, new_filename)
            
            if os.path.exists(new_path):
                print(f"⚠️  Пропущен: '{new_filename}' уже существует.")
                skipped_count += 1
                continue
            
            try:
                os.rename(old_path, new_path)
                print(f"✅ {filename}  →  {new_filename}")
                renamed_count += 1
            except Exception as e:
                print(f"❌ Ошибка при переименовании '{filename}': {e}")
                error_count += 1
    
    print(f"\n📊 Итого: переименовано — {renamed_count}, "
          f"пропущено — {skipped_count}, ошибок — {error_count}")
    
    return {
        'renamed': renamed_count,
        'skipped': skipped_count,
        'errors': error_count
    }


if __name__ == "__main__":
    old_prefix = "IMG_"
    new_prefix = "Vacation_Photo_"
    directory = "./my_photos"
    
    stats = rename_files(directory, old_prefix, new_prefix)