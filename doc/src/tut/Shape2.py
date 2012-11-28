import commands, os
shapes = os.path.join(os.pardir, os.pardir, os.pardir, 'pysketcher', 'shapes.py')
cmd = 'egrep "^class\s+[A-Za-z_0-9]+\([A-Za-z_0-9]+\):" %s' % shapes
failure, outtext = commands.getstatusoutput(cmd)
f = open('Shape2.dot', 'w')
f.write('digraph G {\n')
for line in outtext.splitlines():
    child, parent = line[6:-2].split('(')
    f.write('  "%s" -> "%s" [dir=none];\n' % (parent, child))
f.write('}\n')
f.close()


