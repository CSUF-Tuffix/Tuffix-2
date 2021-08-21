update-alternatives  --install /usr/bin/gcc gcc /usr/bin/gcc-11 11 --slave /usr/bin/g++         g++         /usr/bin/g++-11        \
                                                                   --slave /usr/bin/gcc-ar      gcc-ar      /usr/bin/gcc-ar-11     \
                                                                   --slave /usr/bin/gcc-nm      gcc-nm      /usr/bin/gcc-nm-11     \
                                                                   --slave /usr/bin/gcc-ranlib  gcc-ranlib  /usr/bin/gcc-ranlib-11 \
                                                                   --slave /usr/bin/gcov        gcov        /usr/bin/gcov-11       \
                                                                   --slave /usr/bin/gcov-dump   gcov-dump   /usr/bin/gcov-dump-11  \
                                                                   --slave /usr/bin/gcov-tool   gcov-tool   /usr/bin/gcov-tool-11
update-alternatives  --install /usr/bin/gcc gcc /usr/bin/gcc-9   9 --slave /usr/bin/g++         g++         /usr/bin/g++-9         \
                                                                   --slave /usr/bin/gcc-ar      gcc-ar      /usr/bin/gcc-ar-9      \
                                                                   --slave /usr/bin/gcc-nm      gcc-nm      /usr/bin/gcc-nm-9      \
                                                                   --slave /usr/bin/gcc-ranlib  gcc-ranlib  /usr/bin/gcc-ranlib-9  \
                                                                   --slave /usr/bin/gcov        gcov        /usr/bin/gcov-9        \
                                                                   --slave /usr/bin/gcov-dump   gcov-dump   /usr/bin/gcov-dump-9   \
                                                                   --slave /usr/bin/gcov-tool   gcov-tool   /usr/bin/gcov-tool-9

update-alternatives  --install /usr/bin/clang clang /usr/bin/clang-12 12 --slave /usr/bin/clang++            clang++            /usr/bin/clang++-12              \
                                                                         --slave /usr/bin/clang-format       clang-format       /usr/bin/clang-format-12         \
                                                                         --slave /usr/bin/clang-format-diff  clang-format-diff  /usr/bin/clang-format-diff-12    \
                                                                         --slave /usr/bin/clang-tidy         clang-tidy         /usr/bin/clang-tidy-12           \
                                                                         --slave /usr/bin/clang-tidy-diff    clang-tidy-diff    /usr/bin/clang-tidy-diff-12.py
update-alternatives  --install /usr/bin/clang clang /usr/bin/clang-10 10 --slave /usr/bin/clang++            clang++            /usr/bin/clang++-10              \
                                                                         --slave /usr/bin/clang-format       clang-format       /usr/bin/clang-format-10         \
                                                                         --slave /usr/bin/clang-format-diff  clang-format-diff  /usr/bin/clang-format-diff-10    \
                                                                         --slave /usr/bin/clang-tidy         clang-tidy         /usr/bin/clang-tidy-10           \
                                                                         --slave /usr/bin/clang-tidy-diff    clang-tidy-diff    /usr/bin/clang-tidy-diff-10.py
