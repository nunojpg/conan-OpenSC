[![Download](https://api.bintray.com/packages/nunojpg/conan-repo/OpenSC%3Anunojpg/images/download.svg)](https://bintray.com/nunojpg/conan-repo/OpenSC%3Anunojpg/_latestVersion)
[![Build Status](https://travis-ci.org/nunojpg/conan-OpenSC.svg?branch=master)](https://travis-ci.org/nunojpg/conan-OpenSC)
[![Build status](https://ci.appveyor.com/api/projects/status/n4avbrlh3kc0x7b2/branch/master?svg=true)](https://ci.appveyor.com/project/nunojpg/conan-opensc/branch/master)

# conan-OpenSC

## Reuse the packages

### Basic setup

    $ conan install OpenSC/next@nunojpg/ci
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    OpenSC/next@nunojpg/ci

    [options]
    #OpenSC:shared=true # default is false
    #OpenSC:zlib=true # default is false
    #OpenSC:openssl=true # default is false
    #OpenSC:readline=true # default is false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.