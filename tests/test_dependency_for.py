from pip._internal.resolution.resolvelib.provider import PipProvider
from src.package_source import PackageSource
from src.package import Package
from semver.semver.version import Version
from mixology.mixology.range import Range

class Requirement(object):
    def __init__(self, name, range):
        self.name = name
        self.range = range

class Candidate(object):
    def __init__(self, name, version):
        self.name = name
        self.version = version

class MockProvider(PipProvider):
    def _get_dependencies(self, candidate):
        v = Version.parse("1.0.0")
        r = Range(v, None, True, False) # >=1.0.0
        return [Requirement("pub", r), Requirement("pub2", r)]
    def find_match(self, requirement):
        v = Version.parse("1.1.0")
        v2 = Version.parse("1.2.0")
        return [Candidate(requirement.name, v), Candidate(requirement.name, v2)]

def test_dependencies_for():
    pkg = Package("mixology")
    v = Version.parse("2.1.0")
    vv = Version.parse("1.0.0")
    rr = Range(vv, None, True, False)

    p = PackageSource(MockProvider, None)

    expected = [Requirement("pub", rr), Requirement("pub2", rr)]

    assert expected == p.dependencies_for(pkg, v)

# def test_package_build():
#     p = PackageSource(MockProvider, None)
#     pkg = Package("mixology")
#     v = Version.parse("2.1.0")

#     p.dependencies_for(pkg, v)

#     # rrr what do package saved
#     assert p.package["pub"]["1.0.0"] == 