"""Setup file for GEM."""

from setuptools import setup

setup(
    name="gem",
    version="1.0",
    description="Common classes for GEM Platform",
    author="Advaita Krishna das",
    packages=["gem", "gem.core", "gem.db", "gem.utils", "gem.postman"],
)
