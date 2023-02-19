#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <math.h>

static PyObject* add(PyObject *self, PyObject *args) {
    const int *a, *b;
    if (PyTuple_Size(args) != 2) {
        PyErr_SetString(self, "Must be 2 arguments!");
        return Py_None;
    }

    if (!PyArg_ParseTuple(args, "OO", &a, &b)) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    if (PyLong_Check(a) && PyLong_Check(b))
        return PyLong_FromLong(PyLong_AsLong(a) + PyLong_AsLong(b));

    if ((PyFloat_Check(a) && (PyFloat_Check(b) || PyLong_Check(b))) ||
       ((PyFloat_Check(a) || PyLong_Check(a)) && PyFloat_Check(b)))
        return PyFloat_FromDouble(PyFloat_AsDouble(a) + PyFloat_AsDouble(b));

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* sub(PyObject *self, PyObject *args) {
    const int *a, *b;
    if (PyTuple_Size(args) != 2) {
        PyErr_SetString(self, "Must be 2 arguments!");
        return Py_None;
    }

    if (!PyArg_ParseTuple(args, "OO", &a, &b)) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    if (PyLong_Check(a) && PyLong_Check(b))
        return PyLong_FromLong(PyLong_AsLong(a) - PyLong_AsLong(b));

    if ((PyFloat_Check(a) && (PyFloat_Check(b) || PyLong_Check(b))) ||
       ((PyFloat_Check(a) || PyLong_Check(a)) && PyFloat_Check(b)))
        return PyFloat_FromDouble(PyFloat_AsDouble(a) - PyFloat_AsDouble(b));

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* mul(PyObject *self, PyObject *args) {
    const int *a, *b;
    if (PyTuple_Size(args) != 2) {
        PyErr_SetString(self, "Must be 2 arguments!");
        return Py_None;
    }

    if (!PyArg_ParseTuple(args, "OO", &a, &b)) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    if (PyLong_Check(a) && PyLong_Check(b))
        return PyLong_FromLong(PyLong_AsLong(a) * PyLong_AsLong(b));

    if ((PyFloat_Check(a) && (PyFloat_Check(b) || PyLong_Check(b))) ||
       ((PyFloat_Check(a) || PyLong_Check(a)) && PyFloat_Check(b)))
        return PyFloat_FromDouble(PyFloat_AsDouble(a) * PyFloat_AsDouble(b));

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* divide(PyObject *self, PyObject *args) {
    const int *a, *b;
    if (PyTuple_Size(args) != 2) {
        PyErr_SetString(self, "Must be 2 arguments!");
        return Py_None;
    }

    if (!PyArg_ParseTuple(args, "OO", &a, &b)) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    if (PyFloat_AsDouble(b) == 0.00) {
        PyErr_SetString(PyExc_ZeroDivisionError, "Cannot divide by zero");
        Py_INCREF(Py_None);
        return Py_None;
    }

    if (PyLong_Check(a) && PyLong_Check(b))
        return PyLong_FromLong(PyLong_AsLong(a) / PyLong_AsLong(b));

    if ((PyFloat_Check(a) && (PyFloat_Check(b) || PyLong_Check(b))) ||
       ((PyFloat_Check(a) || PyLong_Check(a)) && PyFloat_Check(b)))
        return PyFloat_FromDouble(PyFloat_AsDouble(a) / PyFloat_AsDouble(b));

    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef CalculatorMethods[] = {{"add", add, METH_VARARGS, ""},
                                          {"sub", sub, METH_VARARGS, ""},
                                          {"mul", mul, METH_VARARGS, ""},
                                          {"div", divide, METH_VARARGS, ""},
                                          {NULL, NULL, 0, NULL}};
                                
static struct PyModuleDef calculator = {PyModuleDef_HEAD_INIT, "calculator",
                                        "Basic C calculator", -1, CalculatorMethods};
        
PyMODINIT_FUNC PyInit_calculator(void) {
    return PyModule_Create(&calculator);
}
