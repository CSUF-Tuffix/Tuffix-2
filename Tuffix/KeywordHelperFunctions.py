"""
Changing the system during keyword add/remove
AUTHOR: Kevin Wortman, Jared Dyreson
"""

from Tuffix.Exceptions import UsageError
from functools import partial

import apt
import dataclasses
import pathlib
import pickle
import psutil
import re
import requests

@dataclasses.dataclass
class LinkPacket:
    link: str
    is_git: bool


class LinkChecker:
    def __init__(self):
        self._re = re.compile("(?P<content>.*)\\.git")

    def link_up(self, link: str):
        request = requests.head(link)
        status = ((request.status_code >= 200)
                  and (request.status_code <= 299) or request.status_code == 302)
        return (status, request.status_code)

    def check_links(self, manifest: dict) -> None:
        for name, container in manifest.items():
            link, is_git = dataclasses.astuple(container)
            if(is_git):
                link = self._re.match(link).group("content")

            status, code = self.link_up(link)
            if not(status):
                raise UsageError(
                    f'[INTERNAL ERROR] Could not reach link {link}, received code: {code}')

def edit_deb_packages(package_names, is_installing):
    if not (isinstance(package_names, list) and
            all(isinstance(name, str) for name in package_names) and
            isinstance(is_installing, bool)):
        raise ValueError
    print(
        f'[INFO] Adding all packages to the APT queue ({len(package_names)})')
    cache = apt.cache.Cache()
    cache.update()
    cache.open()

    for name in package_names:
        print(
            f'[INFO] {"Installing" if is_installing else "Removing"} package: {name}')
        try:
            cache[name].mark_install() if(
                is_installing) else cache[name].mark_delete()
        except KeyError:
            raise EnvironmentError(
                f'[ERROR] Debian package "{name}" not found, is this Ubuntu?')
    try:
        cache.commit()
    except OSError:
        DEFAULT_PROCESS_HANDLER.remove_process("apt")
        raise EnvironmentError(
            '[FATAL] Could not continue, apt was holding resources. Processes were killed, please try again.')
    except Exception as e:
        cache.close()
        raise EnvironmentError(f'[ERROR] Could not install {name}: {e}.')
    finally:
        # unittest complains there is an open file but I have tried closing it in every avenue
        # NOTE : possible memory leak
        cache.close()


DEFAULT_LINK_CHECKER = LinkChecker()
