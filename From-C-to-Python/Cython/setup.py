import distutils.core
import os
import Cython.Build
distutils.core.setup(
    ext_modules=Cython.Build.cythonize("multiply.pyx")
)
os.system('export C_INCLUDE_PATH=/System/Volumes/Data/usr/local/Cellar/python@3.9/3.9.12/Frameworks/Python.framework/Headers/')
# python setup.py build_ext --inplace
