from Tuffix.Exceptions import LinkError
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

    def link_up(self, link: LinkPacket):
        """
        Check if a given link is working
        We make the delineation between Github and regular links
        When a Git repo is not found originally, it will give a 301 code, which
        looks like a success but it ends up showing a 404 message.
        That's because 301 is a redirect code
        """

        if not(isinstance(link, LinkPacket)):
            raise ValueError
        if(link.is_git):
            if((match := self._re.match(link.link))):
                link.link = match.group("content")
            else:
                raise ValueError(f'could not properly parse {link.link}')
        try:
            request = requests.head(link.link)
        except requests.exceptions.ConnectionError:
            return (False, 1000)

        code = request.status_code
        status = ((code >= 200) and (code <= 399))
        return (status, request.status_code)

    def check_links(self, manifest: dict) -> None:
        """
        This is an internal method to check link_dictionary containers
        in Keywords and Editors
        """

        if not(isinstance(manifest, dict)):
            raise ValueError

        for name, packet in manifest.items():
            if not(isinstance(packet, LinkPacket)):
                raise ValueError(
                    f'packet does not have type `LinkPacket`, obtained `{type(packet).__name__}`')
            status, code = self.link_up(packet)
            if not(status):
                raise LinkError(
                    f'[INTERNAL ERROR] Could not reach link {link.link}, received code: {code}')


DEFAULT_LINK_CHECKER = LinkChecker()
