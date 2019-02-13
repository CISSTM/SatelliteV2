#include <Python.h>
#include <stdio.h>
#include <time.h>

int number = 0;

int Cfib(int n){
    if (n < 2)
        return n;
    else
        return Cfib(n-1)+Cfib(n-2);
}

static PyObject* fib(PyObject* self, PyObject* args){
    int n;
    if(!PyArg_ParseTuple(args, "i", &n))
        return NULL;

    return Py_BuildValue("i", Cfib(n));
}

static PyObject* getNumber(PyObject* self, PyObject* args){
    return Py_BuildValue("i", number);
};

static PyMethodDef myMethods[] = {
    {"getNumber", getNumber, METH_NOARGS, "Gets current number from loop"},
    {"fib", fib, 1, "Gives fibonacci thing"},
    { NULL, NULL, 0, NULL}
};

static struct PyModuleDef distance = {
    PyModuleDef_HEAD_INIT,
    "distance",
    "The module to find the distance using the lightspeed and C, great",
    -1,
    myMethods
};

PyMODINIT_FUNC PyInit_distance(void)
{
    return PyModule_Create(&distance);
}