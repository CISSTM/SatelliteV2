#include <Python.h>
#include <stdio.h>
#include <time.h>

int number = 0;

int test(){
    while (1){
        number++;
    }
}

static PyObject* getNumber(PyObject* self, PyObject* args){
    return Py_BuildValue("i", number);
    test();
};

static PyMethodDef myMethods[] = {
    {"getNumber", getNumber, METH_NOARGS, "Gets current number from loop"},
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