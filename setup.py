"""Setup for Vimeo XBlock."""

import os
from setuptools import setup


def package_data(pkg, root):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='vimeo-xblock',
    version='0.4',
    description='Vimeo XBlock',
    packages=[
        'vimeo',
    ],
    install_requires=[
        'XBlock', 'requests'
    ],
    entry_points={
        'xblock.v1': [
            'vimeo = vimeo:VimeoBlock',
        ]
    },
    package_data=package_data("vimeo", "static"),
)