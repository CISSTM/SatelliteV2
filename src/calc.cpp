#include <Python.h>
#include <math.h>


float getDistanceLight (long res_time, float altitude) {
    long time = 0.2; //I still need a value here
    float lightstpeed = 299792458;

    float distance = (float) (time - res_time) / lightstpeed;

    float distance_ground = sqrt( (distance * distance) - (altitude * altitude) );

    return distance_ground;

}

float getDistanceRSSI(float signal_loss, float freq, float signal_decay, float distance_0) {
    float pi = 3.14159;
    float lightspeed = 299792458;
    float golflength =  lightspeed / freq;
    float distance = distance_0 * powf(10, (signal_loss/(10*signal_decay))) * powf((golflength/(4*pi*distance_0)), (2/signal_decay));

    return distance;
}

static PyObject* get_distance_light(PyObject* self, PyObject* args) {
    long res_time;
    float altitude;

    if (!PyArg_ParseTuple(args, "lf", &res_time, &altitude)) {
      return NULL;
    }

    return Py_BuildValue("f", getDistanceLight(res_time, altitude));
}

static PyObject* get_distance_rssi(PyObject* self, PyObject* args) { 
    float signal_loss, freq, signal_decay, distance_0;

    if (!PyArg_ParseTuple(args, "ffff", &signal_loss, &freq, &signal_decay, &distance_0)) {
      return NULL;
    }

    float distance = getDistanceRSSI(signal_loss, freq, signal_decay, distance_0);
    return Py_BuildValue("f", distance);

}

static PyObject* get_altitude(PyObject* self, PyObject* args){
    float temp_now, pressure_now, pressure_0;
    float alt;
    float errors[3] = { 1111, 2222, 9999 };
    if (!PyArg_ParseTuple(args, "fff", &temp_now, &pressure_now, &pressure_0)) {
      return NULL;
    }

    if (pressure_0 < 500){
        pressure_0 = 1013.25;
    }

    if (pressure_now < 500){
        pressure_now = 1013.25;
    }

    for (int i = 1; i < 3; i++){
        if (pressure_now == errors[i]){
            pressure_now = 1013.25;
        }
        if (temp_now == errors[i]){
            temp_now = 5;
        }
    }

    alt = ((powf(pressure_0/pressure_now, 0.19) - 1) * (temp_now + 273.15)) / 0.0065;

    if (alt < 0) {
        alt = -alt + 9000;
    }
    return Py_BuildValue("f", alt);
};

static PyMethodDef myMethods[] = {
    {"get_altitude", get_altitude, METH_VARARGS, "Calculates altitude"},
    {"get_distance_rssi", get_distance_rssi, METH_VARARGS, "Calculates distance"},
    {"get_distance_light", get_distance_light, METH_VARARGS, "Calulates distance"},
    { NULL, NULL, 0, NULL}
};

static struct PyModuleDef calc = {
    PyModuleDef_HEAD_INIT,
    "calc",
    "The module to calculate for Cisstm",
    -1,
    myMethods
};

PyMODINIT_FUNC PyInit_calc(void)
{
    return PyModule_Create(&calc);
}