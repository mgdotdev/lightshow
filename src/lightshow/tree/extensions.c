#include <Python.h>
#include <math.h>

long int _truncate(long item) {
    if (item > 255) {
        item = 255;
    } else if (item < 0) {
        item = 0;
    }
    return item;
}

int _decay(int color, double weight, double distance) {
    if (distance < 0.0) {
        return 0;
    }
    else if (distance == 0.0) {
        return color;
    }
    int result = color * exp(weight * distance);
    return result;
}

static PyObject* _color_from_collection(PyObject* self, PyObject* args) {
    long index;
    PyObject* pixel;
    PyObject* sparks;

    PyArg_ParseTuple(args, "lOO", &index, &pixel, &sparks);

    int g, r, b;
    g = PyLong_AsLong(PyList_GetItem(pixel, 0));
    r = PyLong_AsLong(PyList_GetItem(pixel, 1));
    b = PyLong_AsLong(PyList_GetItem(pixel, 2));

    PyObject* iter = PyObject_GetIter(sparks);
    PyObject* next;
    while ((next = PyIter_Next(iter))) {
        PyObject* color = PyObject_GetAttrString(next, "color");
        PyObject* _x = PyObject_GetAttrString(next, "x");
        PyObject* _weight = PyObject_GetAttrString(next, "weight");
        double x = PyFloat_AsDouble(_x);
        double weight = PyFloat_AsDouble(_weight);
        double distance = x - index;

        int sr, sg, sb;
        sg = PyLong_AsLong(PyTuple_GetItem(color, 0));
        sr = PyLong_AsLong(PyTuple_GetItem(color, 1));
        sb = PyLong_AsLong(PyTuple_GetItem(color, 2));

        sg = _decay(sg, weight, distance);
        sr = _decay(sr, weight, distance);
        sb = _decay(sb, weight, distance);

        g = _truncate(g + sg);
        r = _truncate(r + sr);
        b = _truncate(b + sb);

        Py_DECREF(color);
        Py_DECREF(_x);
        Py_DECREF(_weight);
        Py_DECREF(next);
    }
    Py_DECREF(iter);
    return Py_BuildValue("lll", g, r, b);
}

static PyMethodDef MethodTable[] = {
    {"_color_from_collection", (PyCFunction) _color_from_collection, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Extensions = {
    PyModuleDef_HEAD_INIT,
    "extensions",
    NULL,
    -1,
    MethodTable,
};

PyMODINIT_FUNC PyInit_extensions() {
    return PyModule_Create(&Extensions);
}
