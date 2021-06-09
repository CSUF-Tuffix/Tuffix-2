import os
import pathlib
import re
import unittest

tests = [
    ["tuffix", "background", "user-submitted"],
    ["tuffix", "background", "https://images.wallpapersden.com/image/download/linux-retro_bGpqbmuUmZqaraWkpJRmbmdlrWZlbWU.jpg"],  # from the internet
    ["tuffix", "background", "/tmp/background.png"],  # from disk
    ["tuffix", "background", "FAIL"],  # from disk
]

matches = {
    "user": re.compile("user-submitted", re.IGNORECASE),
    "disk": re.compile("(?P<path>.*)\.(?P<extension>[A-Za-z]+)", re.IGNORECASE)
}

_re = re.compile('(?P<path>.*)\.(?P<extension>[A-Za-z]+)')
wallpaper_dir = pathlib.Path(f'{pathlib.Path.home()}/Pictures/Wallpapers')


def parse(container: list[str]) -> bool:
    if not(isinstance(container, list) and
           all([isinstance(_, str) for _ in container])):
        raise ValueError(f'expecting list[str]')

    if((_len := len(container)) != 3):
        raise Exception(f'insufficient arguments received: {_len} obtained')
    path = container[2]
    _pass = []

    for name, expression in matches.items():
        _expression_match = expression.match(path)

        match _expression_match:
            case re.Match() if (name == "user"):
                # getting user submitted wallpaper
                # print("getting user submitted wallpaper")
                _pass.append(True)
            case re.Match() if(name == "disk"):
                _re_match = _re.match(os.path.basename(path)).groups()
                if("http" not in path):
                    # print("getting from disk")
                    _pass.append(True)
                    break
                match _re_match:
                    case[filename, extension]:
                        # download and use this as valid path
                        destination: pathlib.Path = wallpaper_dir / \
                            pathlib.Path(f'{filename}.{extension}')
                        # print(destination)
                        pass
                        # f'{wallpaper_dir}/{filename}.{extension}')
                    case _:
                        raise Exception('parsing error')
                _pass.append(True)
            case None:
                _pass.append(False)

    return any(_pass)


class BackgroundParsingTest(unittest.TestCase):
    """
    The first three tests should return true
    and the last one should return false
    """

    def test_user_submitted(self):
        _ = parse(tests[0])
        if not(isinstance(_, bool) or
               not _):
            self.assertTrue(False)

    def test_url(self):
        _ = parse(tests[1])
        if not(isinstance(_, bool) or
               not _):
            self.assertTrue(False)

    def test_file(self):
        _ = parse(tests[2])
        if not(isinstance(_, bool) or
               not _):
            self.assertTrue(False)

    def test_failure(self):
        _ = parse(tests[3])
        if not(isinstance(_, bool) or _):
            self.assertTrue(False)


if (__name__ == '__main__'):
    unittest.main()
