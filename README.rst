.. -*- mode: rst -*-

cppyy: Python-C++ bindings interface based on Cling/LLVM
========================================================

cppyy provides fully automatic, dynamic Python-C++ bindings by leveraging
the Cling C++ interpreter and LLVM.
It supports both PyPy (natively), CPython, and C++ language standards
through C++17 (and parts of C++20).

Details and performance are described in
`this paper <http://cern.ch/wlav/Cppyy_LavrijsenDutta_PyHPC16.pdf>`_,
originally presented at PyHPC'16, but since updated with improved performance
numbers.

Full documentation: `cppyy.readthedocs.io <http://cppyy.readthedocs.io/>`_.

Notebook-based tutorial: `Cppyy Tutorial <https://github.com/wlav/cppyy/blob/master/doc/tutorial/CppyyTutorial.ipynb>`_.

For Anaconda/miniconda, install cppyy from `conda-forge <https://anaconda.org/conda-forge/cppyy>`_.

----

Change log:
  https://cppyy.readthedocs.io/en/latest/changelog.html

Bug reports/feedback:
  https://github.com/wlav/cppyy/issues

----

Building with Bazel (experimental)
==================================

The supported build is CMake/``setup.py`` (see the documentation above). A
Bazel build is also provided, but it is **experimental and best-effort**: a
non-gating CI job exercises the whole stack against an upstream LLVM 22 release
(via ``compiler-research/ci-workflows``'s ``setup-llvm``), so a failure warns
rather than blocking a PR, and it may lag behind the CMake build.

It consumes a local LLVM/Clang tree selected by the ``LLVM_DIR`` environment
variable (LLVM 20-22; either a *build* tree or a release *install* tree exposing
``bin/llvm-config``, ``lib/``, ``include/`` -- the build adapts to whichever
static-archive or shared ``libLLVM.so`` layout the tree ships)::

    export LLVM_DIR=/path/to/llvm-project/build

The four stack repos resolve through ``local_path_override`` relative to the
cppyy root, so check them out as siblings and run Bazel from within ``cppyy``::

    <parent>/
      cppyy/          # this repo (carries bazel/ itself)
      CppInterOp/
      cppyy-backend/
      CPyCppyy/

Then, from the ``cppyy`` directory::

    bazelisk build //:lib            # pure-Python cppyy package
    bazelisk build //:cppyy_wheel    # build a wheel
    bazelisk test //:tests           # run the pytest suite
