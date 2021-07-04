from Tuffix.Exceptions import UsageError
import re
import requests
import dataclasses


@dataclasses.dataclass
class LinkPacket:
    link: str
    is_git: bool


class LinkChecker:
    def __init__(self):
        self._re = re.compile("(?P<content>.*)\\.git")

    def link_up(self, link: str):
        if not(isinstance(link, str)):
            raise ValueError

        request = requests.head(link)
        status = ((request.status_code >= 200) and (
            request.status_code <= 299) or request.status_code == 302)
        return (status, request.status_code)

    def check_links(self, manifest: dict) -> None:
        if not(isinstance(manifest, dict)):
            raise ValueError

        for name, container in manifest.items():
            link, is_git = dataclasses.astuple(container)
            if(is_git):
                link = self._re.match(link).group("content")

            status, code = self.link_up(link)
            if not(status):
                raise UsageError(
                    f'[INTERNAL ERROR] Could not reach link {link}, received code: {code}')


DEFAULT_LINK_CHECKER = LinkChecker()
