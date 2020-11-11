from pip._internal.resolution.resolvelib.provider import PipProvider
from src.package_source import PackageSource
from src.package import Package
from mixology.mixology.constraint import Constraint
from semver.semver.version import Version
from mixology.mixology.range import Range
from pip._internal.resolution.resolvelib.requirements import (
    ExplicitRequirement,
    SpecifierRequirement,
    RequiresPythonRequirement,
)
from pip._internal.resolution.resolvelib.candidates import EditableCandidate

class my_EditableCandidate(EditableCandidate):
    def __init__(self,name,version):
        super(EditableCandidate,self).__init__(None,None,None,None,name,version)

class Candidate(object):
    def __init__(self, name, version):
        self.name = name
        self.version = version

class MockProvider(PipProvider):

    def get_dependencies(self, candidate):
        candidate1 = my_EditableCandidate('pub', '1.1.0')
        candidate2 = my_EditableCandidate('pub', '1.2.0')
        requirement1 = ExplicitRequirement(candidate1)
        requirement2 = ExplicitRequirement(candidate2)
        return [requirement1, requirement2]
        
    def find_match(self, requirement):
        return [Candidate(requirement.name, '1.1.0'), Candidate(requirement.name, '1.2.0')]

def test_dependencies_for():
    pkg = Package("mixology")
    v = Version.parse("2.1.0")

    p = PackageSource(MockProvider, None)
    p.package[pkg] = {}
    p.package[pkg][v] = {}

    expected_range1 = Range(Version(1,1,0), Version(1,1,0), True, True)
    expected_constraint = Constraint(Package('pub'), expected_range1)
    expected_range2 = Range(Version(1,2,0), Version(1,2,0), True, True)
    expected_constraint2 = Constraint(Package('pub'), expected_range2)
    expected = [expected_constraint, expected_constraint2]

    assert expected == p.dependencies_for(pkg, v)

# def test_package_build():
#     p = PackageSource(MockProvider, None)
#     pkg = Package("mixology")
#     v = Version.parse("2.1.0")

#     p.dependencies_for(pkg, v)

#     # rrr what do package saved
#     assert p.package["pub"]["1.0.0"] == 