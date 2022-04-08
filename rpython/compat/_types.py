import types


# Types that no longer exist in the types module
NoneType = type(None)
ClassType = getattr(types, "ClassType", type)
