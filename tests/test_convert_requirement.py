import re
import mock

from src.package_source import PackageSource
from src.package import Package

from semver.semver.version import Version

from mixology.mixology.constraint import Constraint
from mixology.mixology.range import Range
from mixology.mixology.union import Union

from typing import Union as _Union

from pip._internal.resolution.resolvelib.provider import PipProvider
from pip._internal.resolution.resolvelib.requirements import (
    ExplicitRequirement,
    SpecifierRequirement,
    RequiresPythonRequirement,
)
from pip._vendor.packaging.specifiers import SpecifierSet
from pip._internal.resolution.resolvelib.candidates import EditableCandidate

class my_EditableCandidate(EditableCandidate):
    def __init__(self,name,version):
        super(EditableCandidate,self).__init__(None,None,None,None,name,version)

class my_req():
    def __init__(self, specifier,name):
        self.specifier = specifier
        self.name = name

class my_ireq():
    def __init__(self,req):
       self.req = req

class my_SpecifierRequirement(SpecifierRequirement):
    def __init__(self, ireq, extras):
        self._ireq = ireq
        self._extras = extras


#*****************************************
#this test function mock the class method 'parse_specifier()'
#*****************************************
def test_ExplicitRequirement(mocker):

    pkg_src = PackageSource(PipProvider,None)
    pkg_name = "numpy"
    pkg_version = '1.2.0'

    expected_range = Range(Version(1,2,0), Version(1,2,0), True, True)
    expected_constraint = Constraint(Package(pkg_name), expected_range)
    
    mocker.patch(
        'src.package_source.PackageSource.parse_specifier',
        return_value = [ expected_range ]
    )

    test_candidate =  my_EditableCandidate (pkg_name,pkg_version)
    test_requirement = ExplicitRequirement(test_candidate)
    result=pkg_src.convert_requirement(test_requirement)

    assert expected_constraint == result

#not finished, just a prototype
def test_RequiresPythonRequirement():
    
    pkg_src = PackageSource(PipProvider,None)
    test_req = RequiresPythonRequirement(None,None)

    test_result = pkg_src.convert_requirement(test_req)
    assert True
    
#*****************************************
#this test function mock the class method 'parse_specifier()'
#*****************************************
def test_SpecifierRequirement_single_specifier(mocker):
    pkg_src = PackageSource(PipProvider,None)
    pkg_name = 'numpy'
    expected_range = Range(Version(1,0,0),None, True, False)
    expected_constraint = Constraint(Package(pkg_name), Union(expected_range))

    mocker.patch(
        'src.package_source.PackageSource.parse_specifier',
        return_value = [ expected_range ]
    )

    test_spififerset = SpecifierSet(">=1.0.0", None)
    test_ireq = my_ireq( my_req(test_spififerset, pkg_name) )
    test_requirement = my_SpecifierRequirement(test_ireq,None)

    result = pkg_src.convert_requirement(test_requirement)

    assert result == expected_constraint

#*****************************************
#this test function mock the class method 'parse_specifier()'
#*****************************************
def test_SpecifierRequirement_multiple_specifiers(mocker):
    pkg_src = PackageSource(PipProvider,None)
    pkg_name = 'numpy'
    expected_range_v1 = Range(Version(1,0,0),None, True, False)
    expected_range_v2 = Range(None,Version(1,5,0), False, False)
    expected_range_v3 = Range(Version(1,2,0),None, False, False)
    expected_range_v4 = Range(None,Version(1,2,0), False, False)

    expected_constraint = Constraint(
        Package(pkg_name), 
        Union(expected_range_v1,expected_range_v2,expected_range_v3,expected_range_v4)
    )

    mocker.patch(
        'src.package_source.PackageSource.parse_specifier',
        side_effect = [ [expected_range_v1],[expected_range_v2],[expected_range_v3,expected_range_v4] ]
    )

    test_spififerset = SpecifierSet(">=1.0.0,<1.5.0,!=1.2.0", None)
    test_ireq = my_ireq( my_req(test_spififerset, pkg_name) )
    test_requirement = my_SpecifierRequirement(test_ireq,None)

    result = pkg_src.convert_requirement(test_requirement)

    assert result == expected_constraint

    



