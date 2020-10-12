from pip._internal.resolution.resolvelib.provider import PipProvider
from src.package_source import PackageSource
from src.package import Package

from semver.semver.version import Version

from mixology.mixology.constraint import Constraint
from mixology.mixology.range import Range
from mixology.mixology.union import Union

from typing import Union as _Union


from pip._internal.resolution.resolvelib.requirements import (
    ExplicitRequirement,
    SpecifierRequirement,
    RequiresPythonRequirement,
)

from pip._internal.resolution.resolvelib.candidates import EditableCandidate

class my_EditableCandidate(EditableCandidate):
    def __init__(self,name,version):
        super(EditableCandidate,self).__init__(None,None,None,None,name,version)


def test_ExplicitRequirement():

    pkg_src = PackageSource(PipProvider,None)
    pkg_name = "numpy"
    pkg_version = '1.2.0'

    expected_range = Range(Version(1,2,0), Version(1,2,0), True, True)
    expected_constraint = Constraint(Package(pkg_name), Union(expected_range))
    
    test_candidate =  my_EditableCandidate (pkg_name,pkg_version)
    test_requirement = ExplicitRequirement(test_candidate)
    result=pkg_src.convert_requirement(test_requirement)

    assert expected_constraint._package == result._package
    assert expected_constraint._constraint == result._constraint


