#!/usr/bin/env python
import os.path
import re
import sys
import tempfile
import zipfile
import wheel.bdist_wheel
import distutils.dist
from distutils.archive_util import make_archive

egg_info_re = re.compile(r'''(?P<name>.+?)-(?P<ver>.+?)
    (-(?P<pyver>.+?))?(-(?P<arch>.+?))?.egg''', re.VERBOSE)

if __name__ == "__main__":
    egg_path = sys.argv[1]
    egg_info = egg_info_re.match(os.path.basename(egg_path)).groupdict()
    egg = zipfile.ZipFile(sys.argv[1])
    dir = tempfile.mkdtemp(suffix="_e2w")
    egg.extractall(dir)
    abi = 'noabi'
    dist_info = "%s-%s" % (egg_info['name'], egg_info['ver'])
    wheel_name = '-'.join((
            dist_info,
            egg_info['pyver'].replace('.', ''),
            (egg_info['arch'] or 'noarch').replace('.', '_').replace('-', '_')
            ))
    bw = wheel.bdist_wheel.bdist_wheel(distutils.dist.Distribution())
    bw.root_is_purelib = egg_info['arch'] is None
    dist_info_dir = os.path.join(dir, '%s.dist-info' % dist_info)
    bw.egg2dist(os.path.join(dir, 'EGG-INFO'),
                dist_info_dir)
    bw.write_wheelfile(dist_info_dir)
    bw.write_record(dir, dist_info_dir)
    filename = make_archive(wheel_name, 'zip', root_dir=dir)
    os.rename(filename, filename[:-3] + 'whl')

