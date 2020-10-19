from src.package_source import PackageSource
from pip._internal.resolution.resolvelib.provider import PipProvider
from semver.semver.version import Version

def test_init():
    p = PackageSource(PipProvider, None)
    v = Version.parse("0.0.0")

    assert p.root_version == v

# def test_init_with_root_requirement():

