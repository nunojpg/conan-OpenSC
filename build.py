from conan.packager import ConanMultiPackager
import platform

if __name__ == '__main__':
    builder = ConanMultiPackager(username='nunojpg')
    builder.add_common_builds(shared_option_name='OpenSC:shared', pure_c=True)
    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        if (settings['arch'] != 'x86' and
            (platform.system() == 'Windows' and options['OpenSC:shared'] == True or
             platform.system() == 'Linux' or
             platform.system() == 'Darwin'
             )):
            filtered_builds.append(
                [settings, options, env_vars, build_requires])
    builder.builds = filtered_builds
    builder.run()
