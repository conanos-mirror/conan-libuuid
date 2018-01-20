#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibuuidConan(ConanFile):
    name = "libuuid"
    version = "1.0.3"
    description = "Portable uuid C library"
    url = "https://github.com/bincrafters/conan-libuuid"
    license = "BSD 3-Clause"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    source_subfolder = "source_subfolder"
    install_subfolder = "install_subfolder"

    def source(self):
        source_url = "https://downloads.sourceforge.net/project/"
        tools.get("{0}/{1}/{2}-{3}.tar.gz".format(source_url, self.name, self.name, self.version))
        os.rename(self.name + "-" + self.version, self.source_subfolder)

    def configure(self):
        if self.settings.os == "Windows":
            raise Exception("Windows is not supported")
        del self.settings.compiler.libcxx

    def build(self):
        with tools.chdir(self.source_subfolder):
            prefix = os.path.abspath(self.package_folder)
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
