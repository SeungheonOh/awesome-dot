"""Bounded POSIX regular-file reads; reject symlinks in every path component."""
import hashlib,os,stat
from pathlib import Path
class FileIssue(ValueError):pass

def regular_bytes(root,relative,limit):
    relative=Path(relative)
    if relative.is_absolute() or not relative.parts or any(x in {'..','.'} for x in relative.parts):
        raise FileIssue('Invalid relative artifact path')
    root=Path(root).absolute()
    directory_flags=os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW
    fd=None;file_fd=None
    try:
        fd=os.open('/',directory_flags)
        for component in root.parts[1:]+relative.parts[:-1]:
            next_fd=os.open(component,directory_flags,dir_fd=fd)
            os.close(fd);fd=next_fd
        file_fd=os.open(relative.parts[-1],os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
        info=os.fstat(file_fd)
        if not stat.S_ISREG(info.st_mode):raise FileIssue('Not a regular file: '+str(relative))
        if info.st_size>limit:raise FileIssue('File exceeds public safe-read byte limit: '+str(relative))
        data=bytearray()
        while len(data)<=limit:
            part=os.read(file_fd,min(65536,limit+1-len(data)))
            if not part:break
            data.extend(part)
        if len(data)>limit:raise FileIssue('File grew beyond public safe-read byte limit: '+str(relative))
        return bytes(data)
    except OSError as exc:
        raise FileIssue('Cannot read regular non-symlink file '+str(relative)+': '+type(exc).__name__) from exc
    finally:
        if file_fd is not None:os.close(file_fd)
        if fd is not None:os.close(fd)

def regular_text(root,relative,limit=1048576):return regular_bytes(root,relative,limit).decode('utf-8')
def hash_check(root,relative,expected):
    try:
        actual=hashlib.sha256(regular_bytes(root,relative,1048576)).hexdigest()
        return actual==expected,('Original SHA-256 matches' if actual==expected else 'Original SHA-256 differs')
    except (FileIssue,UnicodeError,ValueError) as exc:return False,str(exc)

def directory_names(root):
    flags=os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW
    fd=None
    try:
        fd=os.open('/',flags)
        for component in Path(root).absolute().parts[1:]:
            next_fd=os.open(component,flags,dir_fd=fd);os.close(fd);fd=next_fd
        return set(os.listdir(fd))
    except OSError as exc:raise FileIssue('Cannot list regular non-symlink output directory: '+type(exc).__name__) from exc
    finally:
        if fd is not None:os.close(fd)
