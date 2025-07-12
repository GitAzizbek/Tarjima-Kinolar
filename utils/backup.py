import os
import shutil
from pathlib import Path
from datetime import datetime

def backup_file(file_path: str):
    try:
        path = Path(file_path)
        if not path.exists():
            return
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = Path("backup")
        backup_dir.mkdir(exist_ok=True)

        backup_path = backup_dir / f"{path.stem}.{timestamp}{path.suffix}.bak"
        shutil.copy(path, backup_path)
    except Exception as e:
        print(f"⚠️ Backupda xatolik: {e}")
