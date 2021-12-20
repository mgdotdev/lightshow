notes
=====

install the package on the host device as root using `python -m pip install -e . --no-cahce`.
This is necessary due to the included C extensions that need to be compiled by Python.

Run `./on.sh <*args> <**kwargs>` so to run the program as a nohup process. Pass args to python
as you would running `lightshow <*args> <**kwargs>`

Run `bash off.sh` to kill the python script process, and turn off the lights.
