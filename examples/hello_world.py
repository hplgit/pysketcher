"""Minimialistic pysketcher example."""
from pysketcher import *

drawing_tool.set_coordinate_system(
    xmin=0, xmax=5, ymin=0, ymax=3, axis=False)
drawing_tool.set_linecolor('black')

code = Text("print 'Hello, World!'",
            (2.5,1.5), fontsize=24,
            fgcolor='red', bgcolor='gray', fontfamily='monospace')
fig = Composition(dict(text=code))

fig.draw()
drawing_tool.display()
drawing_tool.savefig('tmp1')
input()
