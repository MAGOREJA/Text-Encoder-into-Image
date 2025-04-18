import os
import shutil

QUARANTINE_FOLDER = "quarantine"
QUARANTINE_LOG = "quarantine_log.txt"

def quarantine_file(file_path):
    """Move an infected file to the quarantine folder."""
    if not os.path.exists(QUARANTINE_FOLDER):
        os.makedirs(QUARANTINE_FOLDER)

    file_name = os.path.basename(file_path)
    quarantined_path = os.path.join(QUARANTINE_FOLDER, file_name)

    try:
        shutil.move(file_path, quarantined_path)
        with open(QUARANTINE_LOG, "a") as log_file:
            log_file.write(f"{file_path} -> {quarantined_path}\n")
        return quarantined_path
    except Exception as e:
        raise Exception(f"Error quarantining file {file_path}: {e}")