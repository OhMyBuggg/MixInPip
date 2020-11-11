
from src.package import Package
from src.package_source import PackageSource

from pip._internal.resolution.resolvelib.provider import PipProvider
from pip._internal.resolution.resolvelib.candidates import EditableCandidate

from semver.semver.version import Version

from mixology.mixology.partial_solution import PartialSolution
from mixology.mixology.version_solver import VersionSolver

class my_EditableCandidate(EditableCandidate):
    def __init__(self,name,version):
        super(EditableCandidate,self).__init__(None,None,None,None,name,version)
        
class my_pkg_source(PackageSource):

	def init_pkg(self,package):
		self.package=package

def test_build_mapping():
    #package_source init*******
    pkg_source = my_pkg_source(PipProvider,None)
    pkg1_name = 'numpy'
    pkg1_version_1 = Version(1,1,0)
    pkg1_version_2 = Version(1,5,1)
    
    pkg2_name = 'skilearn'
    pkg2_version_1 = Version(1,2,0)
    pkg2_version_2 = Version(2,0,1)
    
    pkg3_name = 'pandas'
    pkg3_version_1 = Version(1,4,0)
    pkg3_version_2 = Version(1,7,2)
    
    test_package = {
        Package(pkg1_name): {pkg1_version_1: my_EditableCandidate(pkg1_name, '1.1.0') ,pkg1_version_2:my_EditableCandidate(pkg2_name, '1.5.1')},
        Package(pkg2_name): {pkg2_version_1:my_EditableCandidate(pkg2_name, '1.2.0'),pkg2_version_2:my_EditableCandidate(pkg2_name, '2.0.1')},
        Package(pkg3_name): {pkg3_version_1:my_EditableCandidate(pkg3_name, '1.4.0'),pkg3_version_2:my_EditableCandidate(pkg3_name, '1.7.2')}                  
    }
    pkg_source.init_pkg(test_package)
    # package_source init************

    pkg_list = []
    pkg_list.append( Package(pkg1_name) )
    pkg_list.append( Package(pkg2_name) )
    pkg_list.append( Package(pkg3_name) )

    pkg1_required_ver = Version(1,1,0)
    pkg2_required_ver = Version(1,2,0)
    pkg3_required_ver = Version(1,4,0)

    ver_list = []
    ver_list.append( pkg1_required_ver)
    ver_list.append( pkg2_required_ver )
    ver_list.append( pkg3_required_ver )

    solver = VersionSolver(pkg_source)

    for i in range(len(pkg_list)):
        solver._solution._decisions[ pkg_list[i] ] = ver_list[i]

    result_mapping = solver._build_mapping()
    print(result_mapping)

    expected_mapping = {
        pkg1_name: my_EditableCandidate(pkg1_name, '1.1.0'),
        pkg2_name: my_EditableCandidate(pkg2_name, '1.2.0'),
        pkg3_name: my_EditableCandidate(pkg3_name, '1.4.0')
    } 

    assert expected_mapping == result_mapping

