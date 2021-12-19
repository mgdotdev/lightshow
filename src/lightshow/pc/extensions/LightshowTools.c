#include <Python.h>
#include <math.h>

int _truncate(int item) {
    if (item > 255) {
        item = 255;
    } else if (item < 0) {
        item = 0;
    }
    return item;
}

int _decay(int color, double weight, double distance) {
    int result = color * exp(weight * distance);
    return result;
}

static PyObject* _euclidean_distance(PyObject *self, PyObject *args) {
    double point_x, point_y, spark_x, spark_y;
    if (!PyArg_ParseTuple(
        args, "dddd", &point_x, &point_y, &spark_x, &spark_y)
    ) {
        return NULL;
    }
    double dx = point_x - spark_x;
    double dy = point_y - spark_y;
    double sum_of_squares = dx*dx + dy*dy;
    double distance = sqrt(sum_of_squares);

    return Py_BuildValue("d", distance);
}


static PyObject* _color_merge(PyObject *self, PyObject *args) {
    PyObject* target;
    PyObject* item;
    if (!PyArg_ParseTuple(args, "OO", &target, &item)) {
        return NULL;
    }

    int t_r, t_g, t_b;
    if (!PyArg_ParseTuple(target, "iii", &t_r, &t_g, &t_b)) {
        return NULL;
    }

    int i_r, i_g, i_b;
    if (!PyArg_ParseTuple(item, "iii", &i_r, &i_g, &i_b)) {
        return NULL;
    }

    int r = _truncate(t_r + i_r);
    int g = _truncate(t_g + i_g);
    int b = _truncate(t_b + i_b);

    return Py_BuildValue("iii", r, g, b);
}


static PyObject* _color_from_distance(PyObject *self, PyObject *args) {
    PyObject* color;
    double distance, weight;
    if (!PyArg_ParseTuple(args, "Odd", &color, &distance, &weight)) {
        return NULL;
    }

    int c_r, c_g, c_b;
    if (!PyArg_ParseTuple(color, "iii", &c_r, &c_g, &c_b)) {
        return NULL;
    }

    int r = _decay(c_r, weight, distance);
    int g = _decay(c_g, weight, distance);
    int b = _decay(c_b, weight, distance);

    return Py_BuildValue("iii", r, g, b);
}

static PyMethodDef LightshowToolsMethods[] = {
    {"_euclidean_distance", (PyCFunction)_euclidean_distance, METH_VARARGS, ""},
    {"_color_merge", (PyCFunction)_color_merge, METH_VARARGS, ""},
    {"_color_from_distance", (PyCFunction)_color_from_distance, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef LightshowTools = {
    PyModuleDef_HEAD_INIT,
    "LightshowTools",
    NULL,
    -1,
    LightshowToolsMethods
};


PyMODINIT_FUNC PyInit_LightshowTools(void) {
    return PyModule_Create(&LightshowTools);
}