from setuptools import setup

setup(
    name="duppy",
    version="1.0",
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "duppy = main:main",  # dupefinder will be the command
        ],
    },
)

