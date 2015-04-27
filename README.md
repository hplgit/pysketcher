## Pysketcher

Tool for defining sketches of physics problems in terms of Python code.

### Purpose

Pysketcher can typically be used to draw figures like

<!-- <img src="doc/src/tut/fig-tut/wheel_on_inclined_plane.png" width=600> -->
![](doc/src/tut/fig-tut/wheel_on_inclined_plane.png)

Such figures can easily be *interactively* made using a lot of drawing programs.
A Pysketcher figure, however, is defined in terms of computer code. This gives
a great advantage: geometric features can be parameterized in term
of variables, as here:

<!-- <img src="doc/src/tut/fig-tut/vehicle0_dim.png" width=600> -->
![](doc/src/tut/fig-tut/vehicle0_dim.png)

One can then quickly change parameters, here to
`R=0.5; L=5; H=2` and `R=2; L=7; H=1`, and get new figures that would be
tedious to draw manually in an interactive tool.

<!-- <img src="doc/src/tut/fig-tut/vehicle_v23.png" width=800> -->
![](doc/src/tut/fig-tut/vehicle_v23.png)

Another major feature of Pysketcher is the ability to let animate the
sketch. Here is an example of a very simple vehicle on a bumpy road,
where the solution of a differential equation (upper blue line) is fed
back to the sketch to make a vertical displacement of the spring and
other objects in the vehicle, [view animation](http://hplgit.github.io/bumpy/doc/src/mov-bumpy/m2_k1_5_b0_2/index.html) (the animation was created by
[this Pysketcher script](https://github.com/hplgit/bumpy/blob/master/doc/src/fig-bumpy/bumpy_road_fig.py)).

<!-- <img src="http://hplgit.github.io/bumpy/doc/src/mov-bumpy/m2_k1_5_b0_2/tmp_frame_0030.png" width=600> -->
![](http://hplgit.github.io/bumpy/doc/src/mov-bumpy/m2_k1_5_b0_2/tmp_frame_0030.png)


### Tutorial

For an introduction to Pysketcher, see the tutorial in [HTML](http://hplgit.github.io/pysketcher/doc/pub/pysketcher.html), [Sphinx](http://hplgit.github.io/pysketcher/doc/pub/html/index.html), or [PDF](http://hplgit/github.io/pysketcher/doc/pub/pysketcher.pdf) format (or a simplified version of
the tutorial in Chapter 9 in [A Primer on Scientific Programming with Python](http://www.amazon.com/Scientific-Programming-Computational-Science-Engineering/dp/3642549586/ref=sr_1_2?s=books&ie=UTF8&qid=1407225588&sr=1-2&keywords=langtangen), by H. P. Langtangen, Springer, 2014).

### Examples

See the `examples` directory for some examples.
For example, a pendulum and its body diagram,

<!-- <img src="examples/pendulum2.png" width=800> -->
![](examples/pendulum2.png)

can be created by the program [`examples/pendulum.py`](https://github.com/hplgit/pysketcher/tree/master/examples/pendulum.py).


### Citation

If you use Pysketcher and want to cite it, you can either cite this
web site or the book
that has the original documentation of the tool.

BibTeX format:


```
@book{Langtangen_2014,
  title = {A Primer on Scientific Programming With {P}ython},
  author = {H. P. Langtangen},
  year = {2014},
  publisher = {Springer},
  edition = {Fourth},
}

@misc{Pysketcher,
  title = {{P}ysketcher: {D}rawing tool for making sketches},
  author = {H. P. Langtangen},
  url = {https://github.com/hplgit/pysketcher},
  key = {Pysketcher},
  note = {\url{https://github.com/hplgit/pysketcher}},
}
```

Publish format:


```
* books
** A Primer on Scientific Programming With {P}ython
   key:       Langtangen_2014
   author:    H. P. Langtangen
   year:      2014
   publisher: Springer
   status:    published
   edition:   Fourth
   entrytype: book
* misc
** {P}ysketcher: {D}rawing tool for making sketches
   key:       Pysketcher
   author:    H. P. Langtangen
   url:       https://github.com/hplgit/pysketcher
   status:    published
   sortkey:   Pysketcher
   note:      \url{https://github.com/hplgit/pysketcher}
```

### History

Pysketcher was first constructed as a powerful educational example on
object-oriented programming for the book
*A Primer on Scientific Programming With Python*, but the tool quickly
became so useful for the author that it was further developed and
heavily used for creating figures in other books by the author.

