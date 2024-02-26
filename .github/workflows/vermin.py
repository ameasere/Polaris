from os import popen,getenv


def get(ver, i):
    try:
        return ver[i]
    except IndexError:
        return 0

def greater_or_equal(ver1: str, ver2: str) -> bool:
    # compare from major to right, either higher, or longer one wins
    ver1 = [int(x) for x in ver1.split('.')]
    ver2 = [int(x) for x in ver2.split('.')]
    if ver1[0] != ver2[0]:
        return ver1[0]>ver2[0]
    if get(ver1, 1) != get(ver2, 1):
        return get(ver1, 1)>get(ver2, 1)
    return True

stream = popen('vermin --no-parse-comments -f parsable --no-config . | tail -n 1')
vermins = stream.read().split(':')[:-1]
versions = getenv('TEST_PYTHON_VERSIONS', '2.7 3.0 3.1 3.2 3.3 3.4 3.5 3.6 3.7 3.8 3.9 3.10').split()

out = set()

exceptions = []

for vermin in vermins:
    if not vermin: continue
    if vermin.startswith('!') or vermin.startswith('~'):
        exceptions.append(vermin[1:])
        continue
    for version in versions:
        if greater_or_equal(version, vermin):
            out.add(version)

for exception in exceptions:
    for x in out:
        if x.startswith(exception): out.remove(x)

str_ = sorted(list(out)).__repr__().replace(' ', '').replace("'", '"')
print('{"version":'+str_+'}')
