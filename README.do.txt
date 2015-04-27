======= Pysketcher =======

Tool for defining sketches of physics problems in terms of Python code.

===== Purpose =====

Pysketcher can typically be used to draw figures like

FIGURE: [doc/src/tut/fig-tut/wheel_on_inclined_plane, width=600 frac=0.6]

Such figures can easily be *interactively* made using a lot of drawing programs.
A Pysketcher figure, however, is defined in terms of computer code. This gives
a great advantage: geometric features can be parameterized in term
of variables, as here:

FIGURE: [doc/src/tut/fig-tut/vehicle0_dim, width=600 frac=0.6]

One can then quickly change parameters, here to
`R=0.5; L=5; H=2` and `R=2; L=7; H=1`, and get new figures that would be
tedious to draw manually in an interactive tool.

FIGURE: [doc/src/tut/fig-tut/vehicle_v23, width=800]

Another major feature of Pysketcher is the ability to let animate the
sketch. Here is an example of a very simple vehicle on a bumpy road,
where the solution of a differential equation (upper blue line) is fed
back to the sketch to make a vertical displacement of the spring and
other objects in the vehicle, "view animation": "http://hplgit.github.io/bumpy/doc/src/mov-bumpy/m2_k1_5_b0_2/index.html".

FIGURE: [http://hplgit.github.io/bumpy/doc/src/mov-bumpy/m2_k1_5_b0_2/tmp_frame_0030.png, width=600]


===== Tutorial =====

For an introduction to Pysketcher, see the tutorial in "HTML": "http://hplgit.github.io/pysketcher/doc/pub/pysketcher.html", "Sphinx": "http://hplgit.github.io/pysketcher/doc/pub/html/index.html", or "PDF": "http://hplgit/github.io/pysketcher/doc/pub/pysketcher.pdf" format (or a simplified version of
the tutorial in Chapter 9 in "A Primer on Scientific Programming with Python": "http://www.amazon.com/Scientific-Programming-Computational-Science-Engineering/dp/3642549586/ref=sr_1_2?s=books&ie=UTF8&qid=1407225588&sr=1-2&keywords=langtangen", by H. P. Langtangen, Springer, 2014).

===== Citation =====

If you use Pysketcher and want to cite it, you can either cite this
web site or the book
that has the original documentation of the tool.

BibTeX format:

!bc
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
!ec

Publish format:

!bc
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
!ec
