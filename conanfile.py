#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibuuidConan(ConanFile):
    name = "libuuid"
    version = "1.0.3"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url = "https://sourceforge.net/projects/libuuid/"
    description = "Portable uuid C library"
    license = "BSD-3 (https://sourceforge.net/p/libuuid/code/ci/master/tree/COPYING)"
    exports = ["LICENSE.md"]

    source_subfolder = "source_subfolder"
    install_subfolder = "install_subfolder"

    def source(self):
        source_url = "https://downloads.sourceforge.net/project/"
        tools.get("{0}/{1}/{2}-{3}.tar.gz".format(source_url, self.name, self.name, self.version))
        os.rename(self.name + "-" + self.version, self.source_subfolder)

    def configure(self):
        del self.settings.compiler.libcxx

    def build(self):
        with tools.chdir(self.source_subfolder):
            prefix = os.path.abspath(self.package_folder)
            if self.settings.os == 'Windows':
                prefix = tools.unix_path(prefix)
            configure_args = ['--prefix=%s' % prefix]
            if self.options.shared:
                configure_args.extend(["--enable-shared", "--disable-static"])
            else:
                configure_args.extend(["--disable-shared", "--enable-static"])

            env_build = AutoToolsBuildEnvironment(self)
            if self.settings.arch == "x86" or self.settings.arch == "x86_64":
                env_build.flags.append('-mstackrealign')
            env_build.fpic = True
            env_build.configure(args=configure_args)
            env_build.make()
            env_build.make(args=["install"])

    def package(self):
        self.copy("COPYING", dst="licenses", src=self.source_subfolder, keep_path=False)
        # other files are installed by make install call

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
