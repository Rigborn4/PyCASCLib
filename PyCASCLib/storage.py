import io
import os
from subprocess import check_output
from pathlib import Path
import atexit
import shutil
from PIL import Image

root = Path(__file__).resolve().parents[0]
jcasc_path = Path(root, 'JCASC.jar')
jdk_path = None
java_cmd = None

with open(Path(__file__).resolve().parent.joinpath('jdk_path.txt'), 'r') as f:
    jdk_path = f.read()
    java_cmd = Path(jdk_path, 'bin', 'java')

if jdk_path is None:
    raise Exception('jdk_path.txt not found')
elif jdk_path == '**':
    jdk_path = Path(root, 'jdk')
    java_cmd = Path(__file__).resolve().parent.joinpath('jdk', 'bin', 'java')


def extract(storage_path, _in, _out, is_hd=None):
    if is_hd is None:
        command = f'"{java_cmd}" -jar "{jcasc_path}" "{storage_path}" -e "{str(_in)}" "{_out}"'
    elif is_hd:
        _in = os.path.join('war3.w3mod\\_hd.w3mod\\', _in)
        command = f'"{java_cmd}" -jar "{jcasc_path}" "{storage_path}" -e "{str(_in)}" "{_out}"'
    elif not is_hd:
        _in = os.path.join('war3.w3mod\\', _in)
        command = f'"{java_cmd}" -jar "{jcasc_path}" "{storage_path}" -e "{str(_in)}" "{_out}"'
    out = check_output(command, cwd=os.getcwd())
    data = os.path.join(_out, _in)
    return data


def read_file(storage_path, _in, _out, is_hd=None):
    out = extract(storage_path, _in, _out, is_hd)
    buffer = None
    with open(out, 'rb') as f:
        buffer = f.read()
    os.remove(out)
    return buffer


def read_temp(storage_path, _in, is_hd=None):
    temp_path = os.path.join(os.getcwd(), 'temp')
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
        os.system(f'attrib +h {temp_path}')
    out = read_file(storage_path, _in, temp_path, is_hd)
    return out


def open_image(storage_path, _in, is_hd=None):
    file = read_temp(storage_path, _in, is_hd)
    return Image.open(io.BytesIO(file))


def open_file(storage_path, _in, is_hd=None):
    file = read_temp(storage_path, _in, is_hd)
    return file


def read_text(storage_path, _in, is_hd=None):
    file = read_temp(storage_path, _in, is_hd)
    return file.decode('utf-8')


def flush_temp():
    temp_path = os.path.join(os.getcwd(), 'temp')
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)


atexit.register(flush_temp)
