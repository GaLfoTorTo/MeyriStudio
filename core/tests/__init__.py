# Patch de compatibilidade: Django 4.2 + Python 3.14
# BaseContext.__copy__ usa super().__copy__() que não existe no Python 3.14.
# O test client chama copy(context) ao capturar templates renderizados.
from django.template.context import BaseContext


def _patched_base_context_copy(self):
    duplicate = self.__class__.__new__(self.__class__)
    duplicate.__dict__ = self.__dict__.copy()
    duplicate.dicts = self.dicts[:]
    return duplicate


BaseContext.__copy__ = _patched_base_context_copy
