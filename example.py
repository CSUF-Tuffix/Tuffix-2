#!/usr/bin/env python3.9

from aptsources import sourceslist
import apt_pkg

apt_pkg.config.set("Dir::Etc::sourcelist", "/etc/apt"
                   "sources.list")


def func():
    sources = sourceslist.SourcesList(True, "/etc/apt")

    sources.add("deb", "http://de.archive.ubuntu.com/ubuntu/",
                "focal",
                ["main"]) \
        sources.save()


func()
