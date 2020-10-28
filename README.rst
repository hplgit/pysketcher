============
 PySketcher
============
.. image:: https://api.codeclimate.com/v1/badges/eae2c2aa97080fbfed7e/maintainability
    :target: https://codeclimate.com/github/rvodden/pysketcher/maintainability

.. image:: https://api.codeclimate.com/v1/badges/eae2c2aa97080fbfed7e/test_coverage
    :target: https://codeclimate.com/github/rvodden/pysketcher/test_coverage

.. image:: https://circleci.com/gh/rvodden/pysketcher.svg?style=shield
    :target: https://app.circleci.com/pipelines/github/rvodden/pysketcher

.. image:: https://readthedocs.org/projects/pysketcher/badge/?version=latest&style=flat
    :target: https://pysketcher.readthedocs.io/en/latest/
.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit

.. image:: https://img.shields.io/badge/hypothesis-tested-brightgreen.svg
    :target: https://hypothesis.readthedocs.io/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://api.dependabot.com/badges/status?host=github&repo=rvodden/pysketcher
    :target: https://dependabot.com

**This is alpha software - the interface is likely to change with every release prior to 0.1.0.**

Tool for creating sketches of physical and mathematical problems in terms of Python code.

This library is very heavily based on the thinking of Hans Petter Langtangen however
very little if any of his code remains. Significant deviations from his library are:

1. The MatlibplotDraw object is no longer global and is no longer tightly coupled to the shape object. There is now a DrawingTool interface which this class implements.

2. Code is organised into multiple files and published on pypi.

3. Shapes are immutable. This means functions such as ``rotate`` return modified copies of the original shape, rather than altering the shape on which they are called.

4. Angles are in radians not degrees.

5. The Composition object is used more consistently. Previously objects such as Beam where direct children of Shape which led to code repetition.

`Please see the documentation for more information <https://pysketcher.readthedocs.io/en/latest/index.html>`_.
