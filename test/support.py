from __future__ import print_function
import os, py, sys, subprocess

currpath = py.path.local(__file__).dirpath()


def setup_make(targetname):
    if sys.platform == 'win32':
        popen = subprocess.Popen([sys.executable, "make_dict_win32.py", targetname], cwd=str(currpath),
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        popen = subprocess.Popen(["make", targetname+"Dict.so"], cwd=str(currpath),
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = popen.communicate()
    if popen.returncode:
        raise OSError("'make' failed:\n%s" % (stdout,))

if sys.hexversion >= 0x3000000:
    pylong = int
    pyunicode = str
    maxvalue = sys.maxsize
else:
    pylong = long
    pyunicode = unicode
    maxvalue = sys.maxint

IS_WINDOWS = 0
if 'win32' in sys.platform:
    import platform
    if '64' in platform.architecture()[0]:
        IS_WINDOWS = 64
        maxvalue = 2**31-1
    else:
        IS_WINDOWS = 32

IS_MAC_ARM = 0
IS_MAC_X86 = 0
if 'darwin' in sys.platform:
    import platform
    if 'arm64' in platform.machine():
        IS_MAC_ARM = 64
        os.environ["CPPYY_UNCAUGHT_QUIET"] = "1"
    else:
        IS_MAC_X86 = 1
IS_MAC = IS_MAC_ARM or IS_MAC_X86

IS_LINUX = 0
IS_LINUX_ARM = 0
IS_LINUX_X86 = 0
if 'linux' in sys.platform:
    IS_LINUX = 1
    import platform
    if 'aarch64' in platform.machine():
        IS_LINUX_ARM = 64
        os.environ["CPPYY_UNCAUGHT_QUIET"] = "1"
    else:
        IS_LINUX_X86 = 1

try:
    import __pypy__
    ispypy = True
except ImportError:
    ispypy = False

import cppyy
IS_CLANG_REPL = (cppyy.gbl.Cpp.Evaluate("""#ifndef __CLING__ 
                                           true
                                           #else
                                           false
                                           #endif\n""") == 1)
IS_CLANG_DEBUG = (cppyy.gbl.Cpp.Evaluate("""#ifdef NDEBUG
                                            false
                                            #else
                                            true
                                            #endif\n""") == 1)
IS_CLING = not IS_CLANG_REPL
IS_VALGRIND = True if os.getenv("IS_VALGRIND") else False
