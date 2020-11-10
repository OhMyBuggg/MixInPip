
from src.package import Package
from src.package_source import PackageSource

from pip._internal.resolution.resolvelib.provider import PipProvider
from pip._internal.resolution.resolvelib.candidates import EditableCandidate
from pip._internal.resolution.resolvelib.requirements import (
    ExplicitRequirement,
    SpecifierRequirement,
    RequiresPythonRequirement,
)
from pip._vendor.resolvelib.structs import DirectedGraph

from semver.semver.version import Version

from mixology.mixology.partial_solution import PartialSolution
from mixology.mixology.version_solver import VersionSolver

class MockCandidate():
    def __init__(self,name):
        self.name = name

class my_EditableCandidate(EditableCandidate):
    def __init__(self,name,version):
        super(EditableCandidate,self).__init__(None,None,None,None,name,version)

class MockRequirement():
    def __init__(self,name,version):
        self.name = name
        self.version = version 

def get_dependency(candidate):
    if candidate.name == 'numpy':
        return []
    elif candidate.name == 'skilearn' :
        return [MockRequirement('SciPy','4.0.0'),MockRequirement ('joblib','3.2.1')]
    elif candidate.name == 'pandas':
        return [MockRequirement('wheel','1.2.0'),MockRequirement ('pub','2.1.0')]
    else :
        return []

class MockProvider(PipProvider):

    def _get_dependencies( candidate):
        return get_dependency(candidate)
        
#*********************************
all_package_list = ['pandas','skilearn','numpy','SciPy','joblib','wheel','pub']
#**************************

def build_expected_graph(graph):

    for pkg in all_package_list:
        graph.add(pkg)

    for pkg in all_package_list:
        tmp_candidate = MockCandidate(pkg)
        related_pkgs = get_dependency(tmp_candidate)
        if related_pkgs :
            for child in related_pkgs:
                graph.connect(pkg,child.name)

def test_build_graph():
    pkg_source = PackageSource(MockProvider,None)

    pkg1_name = 'numpy'
    pkg2_name = 'skilearn'
    pkg3_name = 'pandas'
    
    pkg1_candidate = my_EditableCandidate(pkg1_name, '1.1.0')
    pkg2_candidate = my_EditableCandidate(pkg2_name, '1.2.0')
    pkg3_candidate = my_EditableCandidate(pkg3_name, '1.4.0')

    test_mapping = {}
    test_mapping[Package(pkg1_name)] = pkg1_candidate
    test_mapping[Package(pkg2_name)] = pkg2_candidate
    test_mapping[Package(pkg3_name)] = pkg3_candidate 

    solver = VersionSolver(pkg_source)
    result_graph = solver._build_graph(test_mapping)

    expected_graph = DirectedGraph()
    build_expected_graph(expected_graph)

    assert expected_graph._vertices == result_graph._vertices
    assert expected_graph._backwards == result_graph._backwards
    assert expected_graph._forwards == result_graph._forwards
