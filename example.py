import os
import pathlib

def update_alternative(link: str, name: str, path: pathlib.Path, priority: int, slave_components):
        for slave in slave_components:
            slave_link, slave_name, slave_path = slave
            command = f"update-alternatives --install {link} {name} {path} {priority} --slave {slave_link} {slave_name} {slave_path}"
            os.system(command)


_gcc_11 = [
    ('/usr/bin/g++',         'g++',         '/usr/bin/g++-11'),
    ('/usr/bin/gcc-ar',      'gcc-ar',      '/usr/bin/gcc-ar-11'),
    ('/usr/bin/gcc-nm',      'gcc-nm',      '/usr/bin/gcc-nm-11'),
    ('/usr/bin/gcc-ranlib',  'gcc-ranlib',  '/usr/bin/gcc-ranlib-11'),
    ('/usr/bin/gcov',        'gcov',        '/usr/bin/gcov-11'),
    ('/usr/bin/gcov-dump',   'gcov-dump',   '/usr/bin/gcov-dump-11'),
    ('/usr/bin/gcov-tool',   'gcov-tool',   '/usr/bin/gcov-tool-11')
]

_gcc_9 = [
    ('/usr/bin/g++',         'g++',         '/usr/bin/g++-9'),
    ('/usr/bin/gcc-ar',      'gcc-ar',      '/usr/bin/gcc-ar-9'),
    ('/usr/bin/gcc-nm',      'gcc-nm',      '/usr/bin/gcc-nm-9'),
    ('/usr/bin/gcc-ranlib',  'gcc-ranlib',  '/usr/bin/gcc-ranlib-9'),
    ('/usr/bin/gcov',        'gcov',        '/usr/bin/gcov-9'),
    ('/usr/bin/gcov-dump',   'gcov-dump',   '/usr/bin/gcov-dump-9'),
    ('/usr/bin/gcov-tool',   'gcov-tool',   '/usr/bin/gcov-tool-9')
]

_gcc_12 = [
    ('/usr/bin/clang++'            'clang++'            '/usr/bin/clang++-12'),
    ('/usr/bin/clang-format'       'clang-format'       '/usr/bin/clang-format-12'),
    ('/usr/bin/clang-format-diff'  'clang-format-diff'  '/usr/bin/clang-format-diff-12'),
    ('/usr/bin/clang-tidy'         'clang-tidy'         '/usr/bin/clang-tidy-12'),
    ('/usr/bin/clang-tidy-diff'    'clang-tidy-diff'    '/usr/bin/clang-tidy-diff-12.py')
]

_gcc_10 = [
    ('/usr/bin/clang++',            'clang++',            '/usr/bin/clang++-10'),
    ('/usr/bin/clang-format',       'clang-format',       '/usr/bin/clang-format-10'),
    ('/usr/bin/clang-format-diff',  'clang-format-diff',  '/usr/bin/clang-format-diff-10'),
    ('/usr/bin/clang-tidy',         'clang-tidy',        '/usr/bin/clang-tidy-10'),
    ('/usr/bin/clang-tidy-diff'    'clang-tidy-diff',    '/usr/bin/clang-tidy-diff-10.py')
]

update_alternative('/usr/bin/gcc', 'gcc', '/usr/bin/gcc-11', 11, _gcc_11)
