import logging
import requests
import shutil
from subprocess import check_output
import platform
from jdk_map import JDK_MAP
import math
import enlighten
from pathlib import Path
from logging import getLogger
import os


class JavaBuilder:
    LOGGER = getLogger('PyCASCLib')
    LOGGER.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    log_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(log_formatter)
    LOGGER.addHandler(handler)

    def __init__(self):
        self.version = None
        self.jdk_path = None
        self.architecture = int(platform.architecture()[0][0:2])
        self.platform = platform.system().lower()

    def load(self, jdk_path=None, java_version=16):
        if jdk_path is None or jdk_path == '':
            if self.architecture == 32:
                self.LOGGER.warning("openjdk doesn't support 32 bit version on non-windows systems")
                self.LOGGER.warning("32 bit version is experimental and may not work")
            url = self.get_jdk_url(self.platform, self.architecture, java_version)
            self.version = java_version
            self.jdk_path = Path(os.getcwd(), 'jdk')
            self.download_jdk(url)
            self.download_jcasc()
            JavaBuilder.remove_src_dirs()
            JavaBuilder.move_jdk()
            JavaBuilder.move_casc()
            JavaBuilder.remove_casc_dir()
            JavaBuilder.write_path('**')
        else:
            self.jdk_path = jdk_path
            self.version = java_version
            self.download_jcasc()
            JavaBuilder.remove_casc_src()
            JavaBuilder.move_casc()
            JavaBuilder.remove_casc_dir()
            if Path(self.jdk_path).exists():
                JavaBuilder.write_path(Path(self.jdk_path))
            else:
                raise FileNotFoundError('JDK path does not exist')

    def get_jdk_url(self, platform_name: str, architecture: int, java_version: int):
        if platform_name not in JDK_MAP:
            raise ValueError('Platform not supported')
        else:
            if java_version not in JDK_MAP[platform_name]:
                raise ValueError('Java version not supported')
            else:
                if architecture not in JDK_MAP[platform_name][java_version]:
                    raise ValueError('Architecture not supported')
                else:
                    return JDK_MAP[platform_name][java_version][architecture]

    def download_jdk(self, url: str):
        self.LOGGER.info('Downloading JDK')
        filename = f'jdk.zip' if platform.system().lower() == 'windows' else f'jdk.tar.gz '
        manager = enlighten.get_manager()
        req = requests.get(url, stream=True)
        assert req.status_code == 200, req.status_code
        dlen = int(req.headers.get('Content-Length', 0)) or None
        with manager.counter(color='green', total=dlen and math.ceil(dlen / 2 ** 20), unit='MiB', leave=False,
                             desc='Downloading Jdk Binaries') as ctr, open(filename, 'wb', buffering=2 ** 24) as f:
            for chunk in req.iter_content(chunk_size=2 ** 20):
                f.write(chunk)
                ctr.update()
        dest = Path(filename)
        dest_name = dest.name
        for s in dest.suffixes:
            dest_name = dest_name.rsplit(s)[0]
        self.extract_jdk(filename, dest_name)

    def download_jcasc(self):
        self.LOGGER.info('Downloading JCASC')
        filename = 'JCASC.zip'
        manager = enlighten.get_manager()
        req = requests.get('https://github.com/DrSuperGood/JCASC/archive/refs/heads/master.zip', stream=True)
        assert req.status_code == 200, req.status_code
        dlen = int(req.headers.get('Content-Length', 0)) or None
        with manager.counter(color='green', total=dlen and math.ceil(dlen / 2 ** 20), unit='MiB', leave=False,
                             desc='Downloading JCASC') as ctr, open(filename, 'wb', buffering=2 ** 24) as f:
            for chunk in req.iter_content(chunk_size=2 ** 20):
                f.write(chunk)
                ctr.update()
        self.extract_jcasc()

    def extract_jdk(self, filename: str, dest_name: str):
        self.LOGGER.info('Extracting JDK')
        shutil.unpack_archive(filename, dest_name)
        for sub_dir in os.listdir(dest_name):
            path = Path(dest_name, sub_dir)
            for child_dir in os.listdir(path):
                shutil.move(Path(path, child_dir), dest_name)
            path.rmdir()

    def extract_jcasc(self):
        self.LOGGER.info('Extracting JCASC')
        filename = 'JCASC.zip'
        dest_name = 'JCASC'
        shutil.unpack_archive(filename, dest_name)
        for sub_dir in os.listdir(dest_name):
            if Path(sub_dir).resolve().name == '.gitignore' or Path(sub_dir).resolve().name == '.classpath' \
                    or Path(sub_dir).resolve().name == '.project':
                os.remove(Path(dest_name, sub_dir))
                continue
            path = Path('JCASC', sub_dir)
            for child_dir in os.listdir(path):
                if Path(child_dir).resolve().name == '.gitignore' or Path(child_dir).resolve().name == '.classpath' \
                        or Path(child_dir).resolve().name == '.project':
                    os.remove(Path(dest_name, sub_dir, child_dir))
                    continue
                shutil.move(Path(path, child_dir), dest_name)
            path.rmdir()
        root = Path('JCASC')
        for child in root.iterdir():
            if child.name == 'JCASC Lab':
                shutil.move(child.joinpath('src', 'com', 'hiveworkshop', 'labs'),
                            root.joinpath('JCASC', 'src', 'com', 'hiveworkshop'))
                shutil.rmtree(child)
        self.generate_path_files()

    def generate_path_files(self):
        self.LOGGER.info('Generating Path Files')
        root = Path('JCASC').joinpath('JCASC', 'src')
        path_list = []
        for path in root.rglob('*.java'):
            if path.resolve().parts[-1] == 'NewCASCExtractLab.java':
                pass
            else:
                path_list.append(str("/".join(path.parts[3:])))
        with open(root.joinpath('source_path.txt'), 'w') as f:
            f.write('\n'.join(path_list))
            f.write('\n')
        self.compile_jcasc()

    def compile_jcasc(self):
        self.LOGGER.info('Compiling Java Files')
        args = [Path(self.jdk_path, 'bin', 'javac'), '-sourcepath', '.', '@source_path.txt',
                '-d',
                'bin']
        process = check_output(f'"{args[0]}" {args[1]} {args[2]} {args[3]} {args[4]} {args[5]}', cwd=Path(os.getcwd(),
                                                                                                          'JCASC',
                                                                                                          'JCASC',
                                                                                                          'src'))
        self.LOGGER.info(process)
        self.build_jar()

    def build_jar(self):
        self.LOGGER.info('Building Jar')
        args = [Path(self.jdk_path, 'bin', 'jar.exe'), 'cfe', 'JCASC.jar',
                "com.hiveworkshop.labs.WC3CASCExtractor",
                '.']
        process = check_output(f'"{args[0]}" {args[1]} {args[2]} {args[3]} {args[4]}',
                               cwd=Path(os.getcwd(), 'JCASC', 'JCASC', 'src', 'bin'))
        self.LOGGER.info(process)

    @classmethod
    def move_casc(cls):
        cls.LOGGER.info('Moving Casc')
        os.replace(Path(os.getcwd(), 'JCASC', 'JCASC', 'src', 'bin', 'JCASC.jar'), Path(os.getcwd(), 'PyCASCLib',
                                                                                        'JCASC.jar'))

    @classmethod
    def move_jdk(cls):
        cls.LOGGER.info('Moving JDK')
        root = Path('PyCASCLib')
        shutil.move('jdk', root)

    @classmethod
    def remove_src_dirs(cls):
        os.remove('JCASC.zip')
        os.remove(f'jdk.zip')

    @classmethod
    def remove_casc_src(cls):
        os.remove('JCASC.zip')

    @classmethod
    def remove_casc_dir(cls):
        shutil.rmtree('JCASC', ignore_errors=True)

    @classmethod
    def write_path(cls, path):
        with open(Path('PyCASCLib', 'jdk_path.txt'), 'w') as f:
            f.write(str(path))
