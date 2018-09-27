import os
import sys
import fnmatch
import glob
from subprocess import call
import shlex

if len(sys.argv) >= 2:
  path = sys.argv[1]
else:
  print "must give path as argument"
  sys.exit()

for root, dirs, filenames in os.walk(path):
  for dirname in dirs:
    subpath = os.path.join(root, dirname)
    print subpath
    if dirname == "results" or True:
      if len(glob.glob(os.path.join(subpath, '*.log.tar.gz'))) > 0:
        print "untaring in", subpath, "..."
      for filename in glob.glob(os.path.join(subpath, '*.log.tar.gz')):
        #target = filename[filename.rfind('/')+1:]
        target = filename
        command = "tar -zxf "+target+" -C "+subpath
        print command
        call(shlex.split(command))
