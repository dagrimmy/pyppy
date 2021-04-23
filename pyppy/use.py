# """
# TODO
# """
# from typing import Type
#
# from pyppy.container import get
#
#
# class _Attr:
#     """
#     TODO
#     """
#
#     def __init__(self, container_name, attr_name):
#         self._attr_name = attr_name
#         self._container_name = container_name
#
#     def __get__(self, obj, obj_type=None):
#         return getattr(get[self._container_name], self._attr_name)  # pylint: disable=E1102
#
#     def __set__(self, _, value):
#         setattr(get[self._container_name], self._attr_name, value)  # pylint: disable=E1102
#
#
# class _UseFactory:
#
#     """Kind of a fill_args factory"""
#
#     def __getattr__(self, container_name):
#         def _use(*used_config_attributes: str):
#             def _attr_adder(decorated_class: Type):
#                 for attr in used_config_attributes:
#                     setattr(
#                         decorated_class,
#                         attr,
#                         _Attr(container_name, attr)
#                     )
#                 return decorated_class
#
#             return _attr_adder
#         return _use
#
#
# use = _UseFactory()
# use.__doc__ = """TODO"""
