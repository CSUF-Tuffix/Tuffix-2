##########################################################################
# changing the system during keyword add/remove
# AUTHOR: Kevin Wortman, Jared Dyreson
##########################################################################

import apt
import pickle


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
                f'[ERROR] Deb package "{name}" not found, is this Ubuntu?')
    try:
        cache.commit()
    except Exception as e:
        raise EnvironmentError(f'[ERROR] Could not install {name}: {e}.')


class PickleFactory():
    def __init__(self):
        pass

    def pickle(self, obj, path: str):
        if(not isinstance(path, str)):
            raise ValueError

        with open(path, 'wb') as fp:
            pickle.dump(fp)

    def depickle(self, path: str):
        with open(path, 'rb') as fp:
            __class = pickle.load(fp)
        return __class


DEFAULT_PICKLER = PickleFactory()
