from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import zip
from builtins import *
from past.utils import old_div
from pysketcher import *

def equal_dict(d1, d2):
    """Return True if nested dicts d1 and d2 are equal."""
    for k in d1:
        #print('comparing', k)
        if k not in d2:
            return False
        else:
            if isinstance(d1[k], dict):
                if not equal_dict(d1[k], d2[k]):
                    return False
            else:
                # Hack: remove u' for unicode if present
                d1_k = d1[k].replace("u'", "'")
                d2_k = d2[k].replace("u'", "'")
                if d1_k != d2_k:
                    #print('values differ: [%s] vs [%s]' % (d1_k, d2_k))
                    return False
    return True

def test_Axis():
    drawing_tool.set_coordinate_system(
        xmin=0, xmax=15, ymin=-7, ymax=8, axis=True,
        instruction_file='tmp_Axis.py')
    # Draw normal x and y axis with origin at (7.5, 2)
    # in the coordinate system of the sketch: [0,15]x[-7,8]
    x_axis = Axis((7.5,2), 5, 'x', rotation_angle=0)
    y_axis = Axis((7.5,2), 5, 'y', rotation_angle=90)
    system = Composition({'x axis': x_axis, 'y axis': y_axis})
    system.draw()
    drawing_tool.display()

    # Rotate this system 40 degrees counter clockwise
    # and draw it with dashed lines
    system.set_linestyle('dashed')
    system.rotate(40, (7.5,2))
    system.draw()
    drawing_tool.display()

    # Rotate this system another 220 degrees and show
    # with dotted lines
    system.set_linestyle('dotted')
    system.rotate(220, (7.5,2))
    system.draw()
    drawing_tool.display()

    drawing_tool.display('Axis')
    drawing_tool.savefig('tmp_Axis')
    expected = {
        'x axis': {
            'arrow': {
                'head left': {'line': "2 (x,y) coords linestyle='dotted'",},
                'line': {'line': "2 (x,y) coords linestyle='dotted'",},
                'head right': {'line': "2 (x,y) coords linestyle='dotted'",},},
            'label': "Text at (6.57388,-3.25231)",},
        'y axis': {
            'arrow': {
                'head left': {'line': "2 (x,y) coords linestyle='dotted'",},
                'line': {'line': "2 (x,y) coords linestyle='dotted'",},
                'head right': {'line': "2 (x,y) coords linestyle='dotted'",},},
            'label': "Text at (12.7523,1.07388)",},}
    computed = eval(repr(system))
    msg = 'expected=%s, computed=%s' % (expected, computed)
    assert equal_dict(computed, expected), msg


def test_Distance_wText():
    drawing_tool.set_coordinate_system(
        xmin=0, xmax=10, ymin=0, ymax=6,
        axis=True, instruction_file='tmp_Distance_wText.py')

    fontsize=14
    t = r'$ 2\pi R^2 $'  # sample text
    examples = Composition({
        'a0': Distance_wText((4,5), (8, 5), t, fontsize),
        'a6': Distance_wText((4,5), (4, 4), t, fontsize),
        'a1': Distance_wText((0,2), (2, 4.5), t, fontsize),
        'a2': Distance_wText((0,2), (2, 0), t, fontsize),
        'a3': Distance_wText((2,4.5), (0, 5.5), t, fontsize),
        'a4': Distance_wText((8,4), (10, 3), t, fontsize,
                             text_spacing=old_div(-1.,60)),
        'a5': Distance_wText((8,2), (10, 1), t, fontsize,
                             text_spacing=old_div(-1.,40), alignment='right'),
        'c1': Text_wArrow('text_spacing=-1./60',
                          (4, 3.5), (9, 3.2),
                          fontsize=10, alignment='left'),
        'c2': Text_wArrow('text_spacing=-1./40, alignment="right"',
                          (4, 0.5), (9, 1.2),
                          fontsize=10, alignment='left'),
        })
    examples.draw()
    drawing_tool.display('Distance_wText and text positioning')
    drawing_tool.savefig('tmp_Distance_wText')

    expected = {
        'a1': {
            'text': "Text at (1.13014,3.14588)",
            'arrow': {
                'arrow': {
                    'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'a0': {
            'text': "Text at (6,5.16667)",
            'arrow': {'arrow': {
                'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'a3': {
            'text': "Text at (1.07454,5.14907)",
            'arrow': {'arrow': {
                'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'a2': {
            'text': "Text at (1.11785,1.11785)",
            'arrow': {'arrow': {
                'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'a5': {
            'text': "Text at (8.8882,1.27639)",
            'arrow': {'arrow': {
                'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'a4': {
            'text': "Text at (8.92546,3.35093)",
            'arrow': {'arrow': {
                'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'a6': {
            'text': "Text at (4.16667,4.5)",
            'arrow': {'arrow': {
                'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'c2': "Text_wArrow at (4,0.5)",
        'c1': "Text_wArrow at (4,3.5)",
        }
    computed = eval(repr(examples))
    msg = 'expected=%s, computed=%s' % (expected, computed)
    assert equal_dict(computed, expected), msg


def test_Rectangle():
    L = 3.0
    W = 4.0

    drawing_tool.set_coordinate_system(
        xmin=0, xmax=2*W, ymin=old_div(-L,2), ymax=2*L,
        axis=True, instruction_file='tmp_Rectangle.py')
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_grid(True)

    xpos = old_div(W,2)
    r = Rectangle(lower_left_corner=(xpos,0), width=W, height=L)
    r.draw()
    r.draw_dimensions()
    drawing_tool.display('Rectangle')
    drawing_tool.savefig('tmp_Rectangle')

    expected = {'rectangle': "5 (x,y) coords",}
    computed = eval(repr(r))
    msg = 'expected=%s, computed=%s' % (expected, computed)
    assert equal_dict(computed, expected), msg

def test_Triangle():
    L = 3.0
    W = 4.0

    drawing_tool.set_coordinate_system(
        xmin=0, xmax=2*W, ymin=old_div(-L,2), ymax=1.2*L,
        axis=True, instruction_file='tmp_Triangle.py')
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_grid(True)

    xpos = 1
    t = Triangle(p1=(old_div(W,2),0), p2=(3*W/2,old_div(W,2)), p3=(4*W/5.,L))
    t.draw()
    t.draw_dimensions()
    drawing_tool.display('Triangle')
    drawing_tool.savefig('tmp_Triangle')

    expected = {'triangle': "4 (x,y) coords",}
    computed = eval(repr(t))
    msg = 'expected=%s, computed=%s' % (expected, computed)
    assert equal_dict(computed, expected), msg


def test_Arc():
    L = 4.0
    W = 4.0

    drawing_tool.set_coordinate_system(
        xmin=old_div(-W,2), xmax=W, ymin=old_div(-L,2), ymax=1.5*L,
        axis=True, instruction_file='tmp_Arc.py')
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_grid(True)

    center = point(0,0)
    radius = old_div(L,2)
    start_angle = 60
    arc_angle = 45
    a = Arc(center, radius, start_angle, arc_angle)
    a.draw()

    R1 = 1.25*radius
    R2 = 1.5*radius
    R = 2*radius
    a.dimensions = {
        'start_angle':
        Arc_wText(
            'start_angle', center, R1, start_angle=0,
            arc_angle=start_angle, text_spacing=old_div(1,10.)),
        'arc_angle':
        Arc_wText(
            'arc_angle', center, R2, start_angle=start_angle,
            arc_angle=arc_angle, text_spacing=old_div(1,20.)),
        'r=0':
        Line(center, center +
             point(R*cos(radians(start_angle)),
                   R*sin(radians(start_angle)))),
        'r=start_angle':
        Line(center, center +
             point(R*cos(radians(start_angle+arc_angle)),
                   R*sin(radians(start_angle+arc_angle)))),
        'r=start+arc_angle':
        Line(center, center +
             point(R, 0)).set_linestyle('dashed'),
        'radius': Distance_wText(center, a(0), 'radius', text_spacing=old_div(1,40.)),
        'center': Text('center', center-point(old_div(radius,10.), old_div(radius,10.))),
        }
    for dimension in a.dimensions:
        if dimension.startswith('r='):
            dim = a.dimensions[dimension]
            dim.set_linestyle('dashed')
            dim.set_linewidth(1)
            dim.set_linecolor('black')

    a.draw_dimensions()
    drawing_tool.display('Arc')
    drawing_tool.savefig('tmp_Arc')

    expected = {'arc': "181 (x,y) coords"}
    computed = eval(repr(a))
    msg = 'expected=%s, computed=%s' % (expected, computed)
    assert equal_dict(computed, expected), msg

    expected = {
        'center': 'text "center" at (-0.2,-0.2)',
        'start_angle': {'text': "Text at (2.68468,1.55)",
                        'arc': {'arc': "181 (x,y) coords",},},
        'r=start+arc_angle': {
            'line': "2 (x,y) coords linecolor='k' linewidth=1 linestyle='dashed'",},
        'r=0': {'line': "2 (x,y) coords linecolor='k' linewidth=1 linestyle='dashed'",},
        'radius': {'text': "Text at (0.629904,0.791025)",
                   'arrow': {'arrow': {
                       'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'r=start_angle': {'line': "2 (x,y) coords linecolor='k' linewidth=1 linestyle='dashed'",},
        'arc_angle': {'text': "Text at (0.430736,3.27177)",
                      'arc': {'arc': "181 (x,y) coords",},}
        }
    computed = eval(repr(a.dimensions))
    msg = 'expected=%s, computed=%s' % (expected, computed)
    assert equal_dict(computed, expected), msg

def test_Spring():
    L = 5.0
    W = 2.0

    drawing_tool.set_coordinate_system(
        xmin=0, xmax=7*W, ymin=old_div(-L,2), ymax=1.5*L,
        axis=True, instruction_file='tmp_Spring.py')
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_grid(True)

    xpos = W
    s1 = Spring((W,0), L, teeth=True)
    s1_title = Text('Default Spring',
                    s1.geometric_features()['end'] + point(0,old_div(L,10)))
    s1.draw()
    s1_title.draw()
    #s1.draw_dimensions()
    xpos += 3*W
    s2 = Spring(start=(xpos,0), length=L, width=old_div(W,2.),
                bar_length=old_div(L,6.), teeth=False)
    s2.draw()
    s2.draw_dimensions()
    drawing_tool.display('Spring')
    drawing_tool.savefig('tmp_Spring')

    # Check s1 and s1.dimensions
    expected = {
        'bar1': {'line': "2 (x,y) coords",},
        'bar2': {'line': "2 (x,y) coords",},
        'spiral': "45 (x,y) coords",}
    computed = eval(repr(s1))
    msg = 'expected=%s, computed=%s' % (expected, computed)
    assert equal_dict(computed, expected), msg

    expected = {
        'bar_length1': {'text': "Text_wArrow at (-1.5,1.75)",
                        'arrow': {'arrow': {
                            'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'bar_length2': {'text': "Text_wArrow at (-1.5,5.5)",
                        'arrow': {'arrow': {
                            'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'width': {'text': "Text at (2,-1.51667)",
                  'arrow': {'arrow': {
                      'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'start': 'annotation "start" at (1.25,-0.75) with arrow to (2,0)',
        'length': {'text': "Text at (3.73333,2.5)",
                   'arrow': {'arrow': {
                       'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'num_windings': 'annotation "num_windings" at (3,5.5) with arrow to (2.6,2.5)'
        }
    computed = eval(repr(s1.dimensions))
    msg = 'expected=%s, computed=%s' % (expected, computed)
    assert equal_dict(computed, expected), msg


def test_Dashpot():
    L = 5.0
    W = 2.0
    xpos = 0

    drawing_tool.set_coordinate_system(
        xmin=xpos, xmax=xpos+5.5*W, ymin=old_div(-L,2), ymax=1.5*L,
        axis=True, instruction_file='tmp_Dashpot.py')
    drawing_tool.set_linecolor('blue')
    drawing_tool.set_grid(True)

    # Default (simple) dashpot
    xpos = 1.5
    d1 = Dashpot(start=(xpos,0), total_length=L)
    d1_title = Text('Dashpot (default)',
                    d1.geometric_features()['end'] + point(0,old_div(L,10)))
    d1.draw()
    d1_title.draw()

    # Dashpot for animation with fixed bar_length, dashpot_length and
    # prescribed piston_pos
    xpos += 2.5*W
    d2 = Dashpot(start=(xpos,0), total_length=1.2*L, width=old_div(W,2),
                 bar_length=W, dashpot_length=old_div(L,2), piston_pos=2*W)
    d2.draw()
    d2.draw_dimensions()

    drawing_tool.display('Dashpot')
    drawing_tool.savefig('tmp_Dashpot')

    expected = {
        'line start': {'line': "2 (x,y) coords",},
        'piston': {
            'line': {'line': "2 (x,y) coords",},
            'rectangle': {
                'rectangle': "5 (x,y) coords fillcolor='' fillpattern='X'",},},
        'pot': "4 (x,y) coords",
        }
    computed = eval(repr(d2))
    msg = 'expected=%s, computed=%s' % (expected, computed)
    assert equal_dict(computed, expected), msg

    expected = {
        'width': {'text': "Text at (6.5,-1.56667)",
                  'arrow': {'arrow': {
                      'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'start': 'annotation "start" at (5.75,-0.75) with arrow to (6.5,0)',
        'bar_length': {'text': "Text_wArrow at (3.5,1.5)",
                       'arrow': {'arrow': {
                           'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'total_length': {'text': "Text_wArrow at (8.75,5)",
                         'arrow': {'arrow': {
                             'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'dashpot_length': {'text': "Text_wArrow at (7,-0.5)",
                           'arrow': {'arrow': {
                               'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},},
        'piston_pos': {'text': "Text_wArrow at (3.5,3.6875)",
                       'arrow': {'arrow': {
                           'line': "2 (x,y) coords linecolor='k' linewidth=1 arrow='<->'",},},}
        }
    computed = eval(repr(d2.dimensions))
    msg = 'expected=%s, computed=%s' % (expected, computed)
    assert equal_dict(computed, expected), msg

def test_Wavy():
    drawing_tool.set_coordinate_system(xmin=0, xmax=1.5,
                                       ymin=-0.5, ymax=5,
                                       axis=True,
                                       instruction_file='tmp_Wavy.py')
    w = Wavy(main_curve=lambda x: 1 + sin(2*x),
             interval=[0,1.5],
             wavelength_of_perturbations=0.3,
             amplitude_of_perturbations=0.1,
             smoothness=0.05)
    w.draw()
    drawing_tool.display('Wavy')
    drawing_tool.savefig('tmp_Wavy')

    expected = {'wavy': "2001 (x,y) coords",}
    computed = eval(repr(w))
    msg = 'expected=%s, computed=%s' % (expected, computed)
    assert equal_dict(computed, expected), msg


def diff_files(files1, files2, mode='HTML'):
    import difflib, time
    n = 3
    for fromfile, tofile in zip(files1, files2):
        fromdate = time.ctime(os.stat(fromfile).st_mtime)
        todate = time.ctime(os.stat(tofile).st_mtime)
        fromlines = open(fromfile, 'U').readlines()
        tolines = open(tofile, 'U').readlines()
        diff_html = difflib.HtmlDiff().\
                    make_file(fromlines,tolines,
                              fromfile,tofile,context=True,numlines=n)
        diff_plain = difflib.unified_diff(fromlines, tolines, fromfile, tofile, fromdate, todate, n=n)
        filename_plain = fromfile + '.diff.txt'
        filename_html = fromfile + '.diff.html'
        if os.path.isfile(filename_plain):
            os.remove(filename_plain)
        if os.path.isfile(filename_html):
            os.remove(filename_html)
        f = open(filename_plain, 'w')
        f.writelines(diff_plain)
        f.close()
        size = os.path.getsize(filename_plain)
        if size > 4:
            print('found differences:', fromfile, tofile)
            f = open(filename_html, 'w')
            f.writelines(diff_html)
            f.close()

def _test_test():
    """Compare files."""
    # Does not work yet.
    os.chdir('test')
    funcs = [name for name in globals() if name.startswith('test_') and callable(globals()[name])]
    funcs.remove('test_test')
    new_files = []
    res_files = []
    for func in funcs:
        mplfile = func.replace('test_', 'tmp_') + '.py'
        #exec(func + '()')
        new_files.append(mplfile)
        resfile = mplfile.replace('tmp_', 'res_')
        res_files.append(resfile)
    diff_files(new_files, res_files)

test_Arc()
