"""
Модуль для автоматического архивирования старых файлов.
"""

import os
import zipfile
import tarfile
from datetime import datetime, timedelta


def archive_old_files(
    dir_path: str,
    day_threshold: int = 30,
    archive_format: str = 'zip'
) -> str | None:
    """
    Архивирует файлы старше day_threshold дней.
    
    Args:
        dir_path: Путь к директории с файлами
        day_threshold: Порог в днях (по умолчанию 30)
        archive_format: Формат архива 'zip' или 'tar' (по умолчанию 'zip')
        
    Returns:
        Путь к созданному архиву или None, если файлов для архивации нет
        
    Example:
        >>> archive_old_files("./logs", day_threshold=30, archive_format='zip')
    """
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"Директория '{dir_path}' не существует.")
    
    if not os.path.isdir(dir_path):
        raise NotADirectoryError(f"'{dir_path}' — не директория.")
    
    if archive_format not in ['zip', 'tar']:
        raise ValueError(f"Неподдерживаемый формат: '{archive_format}'. Используйте 'zip' или 'tar'.")
    
    cutoff_date = datetime.now() - timedelta(days=day_threshold)
    files_to_archive = []
    
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        
        if os.path.isfile(file_path):
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if mod_time < cutoff_date:
                files_to_archive.append((filename, file_path))
    
    if not files_to_archive:
        print(f"✅ Нет файлов старше {day_threshold} дней.")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if archive_format == 'zip':
        archive_name = f"archive_{timestamp}.zip"
        archive_path = os.path.join(dir_path, archive_name)
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename, file_path in files_to_archive:
                zipf.write(file_path, filename)
                print(f"📦 Добавлен: {filename}")
    
    else:
        archive_name = f"archive_{timestamp}.tar.gz"
        archive_path = os.path.join(dir_path, archive_name)
        
        with tarfile.open(archive_path, 'w:gz') as tar:
            for filename, file_path in files_to_archive:
                tar.add(file_path, arcname=filename)
                print(f"📦 Добавлен: {filename}")
    
    print(f"\n📁 Создан архив: {archive_name}")
    print(f"📊 Архивировано файлов: {len(files_to_archive)}")
    
    return archive_path


if __name__ == "__main__":
    directory = "./logs"
    archive_path = archive_old_files(directory, day_threshold=30, archive_format='zip')