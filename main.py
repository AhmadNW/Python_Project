import os
import stat
import getpass
import datetime
from colorama import Fore, Style, init

# הפעלת הצבעים במסך
init()

def format_size(size_bytes):
    """המרת גודל לפורמט קריא"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def format_permissions(mode):
    """המרת הרשאות """
    perms = ''
    for who in ['USR', 'GRP', 'OTH']:
        for what in ['R', 'W', 'X']:
            if mode & getattr(stat, f'S_I{what}{who}'):
                perms += what.lower()
            else:
                perms += '-'
    return perms

def list_directory(path='.', recursive=False, human_readable=False, filter_ext=None):
    """פונקציית ls מותאמת"""
    total_files = 0
    total_size = 0

    for root, dirs, files in os.walk(path):
        entries = dirs + files

        if filter_ext:
            entries = [e for e in entries if e.endswith(filter_ext)]

        for entry in entries:
            full_path = os.path.join(root, entry)
            try:
                stats = os.stat(full_path)
                mode = stats.st_mode
                size = stats.st_size
                owner = getpass.getuser()  # שם המשתמש הנוכחי
                group = stats.st_gid       # ב-Windows מציגים GID כמספר
                mod_time = datetime.datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M")
                perms = format_permissions(mode)
                size_str = format_size(size) if human_readable else f"{size} B"

                # הצגת שם הקובץ בצבע (תיקיות בכחול)
                if stat.S_ISDIR(mode):
                    print(Fore.BLUE + f"{entry}/" + Style.RESET_ALL, end=' ')
                else:
                    print(entry, end=' ')

                # הצגת המידע
                print(f"- Size: {size_str}, Permissions: {perms}, Owner: {owner}, Group ID: {group}, Modified: {mod_time}")

                total_files += 1
                total_size += size

            except FileNotFoundError:
                print(f"Cannot access: {entry}")

        if not recursive:
            break

    print(f"\nTotal Files: {total_files}")
    print(f"Total Size: {format_size(total_size) if human_readable else f'{total_size} B'}")

# הרצת הפונקציה אם קובץ זה הופעל ישירות
if __name__ == "__main__":
    list_directory(
        path=".",             # תיקייה נוכחית
        recursive=True,       # כמו ls -R
        human_readable=True,  # כמו ls -h
        filter_ext=".txt"     # כמו ls -e txt
    )
