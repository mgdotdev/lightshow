import os.path

from setuptools import setup, find_packages, Extension

here = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

extensions = [
    Extension(
        "lightshow.pc.extensions.LightshowTools",
        [os.path.join("src", "lightshow", "pc", "extensions", "LightshowTools.c")],
    ),
    Extension(
        "lightshow.tree.extensions",
        [os.path.join("src", "lightshow", "tree", "extensions.c")]
    )
]

setup(
    name="lightshow",
    version="0.0.1",
    python_requires=">=3.6",
    include_package_data=True,
    description="code for running LED lights",
    long_description=long_description,
    url="https://github.com/1mikegrn/lightshow",
    author="Michael Green",
    author_email="michael@michaelgreen.dev",
    license="GPL-3.0",
    classifiers=[
        "Development Status :: 3 - Beta",
        "License :: OSI Approved :: GPL-3.0 License",
    ],
    entry_points={"console_scripts": ["lightshow=lightshow.__main__:main"]},
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    tests_require=["pytest"],
    ext_modules=extensions,
)
