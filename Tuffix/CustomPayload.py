import dataclasses

from Tuffix.Constants import KEYWORD_MAX_LENGTH

@dataclasses.dataclass
class CustomPayload:
    name: str
    instructor: str
    packages: list

    def __init__(self, container: dict):
        self.name, self.instructor, self.packages = list(
            container.values())  # will raise ValueError

        if((argc := len(self.name)) > KEYWORD_MAX_LENGTH):
            self.name = self.trim_name()

    def trim_name(self):
        container = ''.join([_ for _ in self.name if(_.isupper())])
        if not(container):
            container = ''.join(
                self.name[:KEYWORD_MAX_LENGTH]).replace(' ', '')

        return container.lower()

