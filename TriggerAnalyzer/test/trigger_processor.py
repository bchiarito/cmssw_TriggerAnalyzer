import sys
import os
import fnmatch

triggers = []

if len(sys.argv) >= 2:
  path = sys.argv[1]
else:
  print "must give directory as argument"
  sys.exit()
  #path = "./"

collect = False
num_files = 0
sys.stdout.write('found ')
for root, dirs, filenames in os.walk(path):
  num_files += len(fnmatch.filter(filenames, 'cmsRun-stdout-*.log'))
  if len(fnmatch.filter(filenames, 'cmsRun-stdout-*.log')) > 0:
    sys.stdout.write(str(len(fnmatch.filter(filenames, 'cmsRun-stdout-*.log'))))
    sys.stdout.write(",")
    sys.stdout.flush()
  for filename in fnmatch.filter(filenames, 'cmsRun-stdout-*.log'):
    stdout = open(os.path.join(root, filename))
    #stdout = open(stdout_file)
    for line in stdout:
      if line.split() == []:
	continue
      if line.split()[0] == "TimeReport>":
	collect = False
	continue
      if collect:
	contents = line.split()
	name = contents[1]
	ps = contents[3]
	run = contents[5]
	nevents = contents[7]
	triggers.append((name, ps, run, nevents))
	continue
      if line == "entering endJob()\n":
	collect = True
	continue
sys.stdout.write(" files.\n")
sys.stdout.flush()
print "found", num_files, "total files."
if len(triggers) >= 1:
  print "done collecting, we got", len(triggers), "entries, e.g."
  print triggers[0][0], triggers[0][1], triggers[0][2], triggers[0][3]
  print "..."
else:
  print "done collecting, no entries!"

outfile = open("list_triggers.txt", "w")
for trigger in triggers:
  outfile.write(trigger[0]+" "+trigger[1]+" "+trigger[2]+" "+trigger[3]+"\n")
outfile.close()
print "overwrote triggers to file 'list_triggers.txt'"

query = []
for trigger in triggers:
  # only collect triggers at prescale 1
  if trigger[1] == "1":
    # check if in list
    found_in_list = False
    for entry in query:
      trig_name = trigger[0]
      trig_name = trig_name[:trig_name.rfind('_v')]
      if entry[0] == trig_name:
	# in list, then update entry
	entry[1] = int(entry[1])+int(trigger[3])
	found_in_list = True
    if not found_in_list:
      # add to list
      trig_name = trigger[0]
      trig_name = trig_name[:trig_name.rfind('_v')]
      query.append( [trig_name , int(trigger[3])] )

print "computed", len(query), "trigger names matching query"
for entry in query:
  print entry[0], ",", entry[1], "total events"
