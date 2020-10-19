from inspect import signature


def tmp2(x, y=1, /, *args, z=None):
    pass

sig = signature(tmp2)

for item in sig.parameters.items():
    print(item[0], item[1].kind)

d = {
    "x": 1,
    "y": 2,
    "z": "tmp"
}
