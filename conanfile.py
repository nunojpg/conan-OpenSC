from conans import ConanFile, tools
from conans.tools import os_info, SystemPackageTool
import os

class OpenSCConan(ConanFile):
    name = 'OpenSC'
    version = 'next'
    license = 'LGPL license version 2.1'
    description = 'Open source smart card tools and middleware. PKCS#11/MiniDriver/Tokend.'
    url = 'https://github.com/OpenSC/OpenSC'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        'shared': [True, False],
        'zlib': [True, False],
        'openssl': [True, False],
        'readline': [True, False]
    }
    default_options = 'shared=False', 'zlib=False', 'openssl=False', 'readline=False'

    def system_requirements(self):
        self.global_system_requirements = True
        if os_info.linux_distro == 'ubuntu':
            installer = SystemPackageTool()
            installer.install('pkg-config libpcsclite-dev')

    def source(self):
        if 'CONAN_RUNNER_ENCODED' in os.environ:    #conan package tools linux docker build
            os.environ['GIT_SSL_NO_VERIFY'] = 'true'
        self.run('git clone --depth 1 https://github.com/OpenSC/OpenSC')

    def configure(self):
        del self.settings.compiler.libcxx

    def build(self):
        zlib = ' --enable-zlib' if self.options.zlib else ' --disable-zlib'
        openssl = ' --enable-openssl' if self.options.openssl else ' --disable-openssl'
        readline = ' --enable-readline' if self.options.readline else ' --disable-readline'
        with tools.chdir('OpenSC'):
            if self.settings.os == 'Windows':
                debug = ' DEBUG_DEF=/DDEBUG' if self.settings.build_type == 'Debug' else ''
                self.run(r'bash -c "exec 0</dev/null && ./bootstrap"')
                self.run(r'bash -c "exec 0</dev/null && ./configure%s%s%s' %
                         (zlib, openssl, readline))
                self.run(r'bash -c "make -C etc opensc.conf"')
                self.run(r'cp win32/winconfig.h config.h')
                self.run(r'nmake /f Makefile.mak BUILD_ON=WIN64 BUILD_FOR=WIN64%s' % debug)
            else:
                install_dir = self.conanfile_directory + '/distribution'
                self.run('./bootstrap')
                self.run('./configure --prefix=%s%s%s%s' %
                         (install_dir, zlib, openssl, readline))
                self.run('make install-strip')
                os.rename(install_dir, install_dir + '_stripped')
                self.run('make install')

    def build_id(self):
        if self.settings.os != 'Windows':
            self.info_build.options.shared = 'Any'
            self.info_build.settings.build_type = 'Any'

    def package(self):
        path = 'distribution' if self.settings.build_type == 'Debug' else 'distribution_stripped'
        self.copy('*.h', dst='include', src='OpenSC/src')
        if self.settings.os == 'Windows':
            self.copy('opensc.lib', dst='lib', src='OpenSC/src/libopensc')
            if self.options.shared:
                self.copy('opensc.dll', dst='bin', src='OpenSC/src/libopensc')
        else:
            if self.options.shared:
                self.copy('libopensc.so*', dst='lib', src=path + '/lib')
                self.copy('libopensc*dylib', dst='lib', src=path + '/lib')
            else:
                self.copy('libopensc.a', dst='lib', src=path + '/lib')

    def package_info(self):
        self.cpp_info.libs = ['opensc']
