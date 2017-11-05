#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
import tempfile


class LibuuidConan(ConanFile):
    name = "libuuid"
    version = "1.0.3"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url = "https://sourceforge.net/projects/libuuid/"
    description = "Portable uuid C library"
    license = "https://sourceforge.net/p/libuuid/code/ci/master/tree/COPYING"
    exports = "LICENSE"
    root = name + "-" + version
    intall_dir = tempfile.mkdtemp(prefix=root)

    def source(self):
        source_url = "https://downloads.sourceforge.net/project/"
        tools.get("{0}/{1}/{2}-{3}.tar.gz".format(source_url, self.name, self.name, self.version))

    def configure(self):
        if self.settings.os != "Linux" and self.settings.os != "FreeBSD":
            raise Exception("Only Linux/FreeBSD supported for libuuid")
        del self.settings.compiler.libcxx

    def build(self):
        with tools.chdir(self.root):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.configure(args=["--prefix=%s" % self.intall_dir])
            env_build.make()
            env_build.make(args=["install"])

    def package(self):
        self.copy(pattern="LICENSE")
        self.copy(pattern="*.h", dst="include", src=os.path.join(self.intall_dir, "include"))
        if self.options.shared:
            self.copy(pattern="*.so*", dst="lib", src=os.path.join(self.intall_dir, "lib"), keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src=os.path.join(self.intall_dir, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
