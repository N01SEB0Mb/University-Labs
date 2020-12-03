# coding=utf-8
"""
Package defines classes from task:
 - Base1, abc
 - Base2, abc
 - Alpha, inherits Base1
 - Beta, inherits Base1
 - Gamma, inherits Base2
 - Delta, inherits Base2
"""

from .base import Base1, Base2, Alpha, Beta, Gamma, Delta, S

__author__ = "Tiron Mykhailo"
__version__ = "1.0.0"
__date__ = "01.11.2020"

__all__ = [
    "S",
    "Base1",
    "Base2",
    "Alpha",
    "Beta",
    "Gamma",
    "Delta"
]
