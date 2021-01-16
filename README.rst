============
 PySketcher
============

.. image:: https://github.com/rvodden/pysketcher/workflows/Tests/badge.svg
    :target: https://github.com/rvodden/pysketcher/actions?query=workflow%3ATests+branch%3Amaster

.. image:: https://badgen.net/pypi/v/pysketcher?icon=pypi
       :target: https://pypi.org/project/pysketcher/

.. image:: https://api.codeclimate.com/v1/badges/eae2c2aa97080fbfed7e/maintainability
    :target: https://codeclimate.com/github/rvodden/pysketcher/maintainability

.. image:: https://codecov.io/gh/rvodden/pysketcher/branch/master/graph/badge.svg?token=AHCKOL75VY
    :target: https://codecov.io/gh/rvodden/pysketcher

.. image:: https://readthedocs.org/projects/pysketcher/badge/?version=latest&style=flat
    :target: https://pysketcher.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit

.. image:: https://img.shields.io/badge/hypothesis-tested-brightgreen.svg
    :target: https://hypothesis.readthedocs.io/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://badgen.net/github/dependabot/rvodden/pysketcher?icon=github
    :target: https://github.com/rvodden/pysketcher

**This is alpha software - the interface is likely to change with every release prior to 0.1.0.**

Tool for creating sketches of physical and mathematical problems in terms of Python code.

This library is continues the legacy of Hans Petter Langtangen. Work done since he sadly passed in 2016 includes:

1. The MatlibplotDraw object is no longer global and is no longer tightly coupled to the shape object. There is now a DrawingTool interface which this class implements.

2. Code is organised into multiple files and published on pypi.

3. Shapes are immutable. This means functions such as ``rotate`` return modified copies of the original shape, rather than altering the shape on which they are called.

4. Angles are in radians not degrees.

5. The Composition object is used more consistently. Previously objects such as Beam were direct children of Shape which led to code repetition.

`Please see the documentation for more information <https://pysketcher.readthedocs.io/en/latest/index.html>`_.
