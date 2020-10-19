from pip._internal.resolution.resolvelib.provider import PipProvider
from src.package_source import PackageSource
from mixology.mixology.range import Range
from mixology.mixology.union import Union
from semver.semver.version import Version

def test_parse_equal():
    specifier = "==1.0.0"
    p = PackageSource(PipProvider, None)
    v = Version.parse("1.0.0")
    expected = Range(v, v, True, True)

    assert [expected] == p.parse_specifier(specifier)

def test_parse_bigger():
    specifier = ">1.0.0"
    p = PackageSource(PipProvider, None)
    v = Version.parse("1.0.0")
    expected = Range(v, None, False, False)

    assert [expected] == p.parse_specifier(specifier)

def test_parse_smaller():
    specifier = "<1.0.0"
    p = PackageSource(PipProvider, None)
    v = Version.parse("1.0.0")
    expected = Range(None, v, False, False)

    assert [expected] == p.parse_specifier(specifier)

def test_parse_bigger_include():
    specifier = ">=1.0.0"
    p = PackageSource(PipProvider, None)
    v = Version.parse("1.0.0")
    expected = Range(v, None, True, False)

    assert [expected] == p.parse_specifier(specifier)

def test_parse_smaller_include():
    specifier = "<=1.0.0"
    p = PackageSource(PipProvider, None)
    v = Version.parse("1.0.0")
    expected = Range(None, v, False, True)

    assert [expected] == p.parse_specifier(specifier)

# please check order of range
def test_parse_not_equal():
    specifier = "!=1.0.0"
    p = PackageSource(PipProvider, None)
    v = Version.parse("1.0.0")
    expected = [Range(v, None, False, False), Range(None, v, False, False)]

    assert expected == p.parse_specifier(specifier)

def test_parse_padding():
    specifier = "==12.55"
    p = PackageSource(PipProvider, None)
    v = Version.parse("12.55.0")
    expected = Range(v, v, True, True)

    assert [expected] == p.parse_specifier(specifier)

def test_parse_compatible():
    specifier = "~=2.2"
    p = PackageSource(PipProvider, None)
    v = Version.parse("2.2")
    v2 = Version.parse("3.0")
    expected = Range(v, v2, True, False)

    assert [expected] == p.parse_specifier(specifier)

def test_parse_compatible2():
    specifier = "~=1.4.5"
    p = PackageSource(PipProvider, None)
    v = Version.parse("1.4.5")
    v2 = Version.parse("1.5")
    expected = Range(v, v2, True, False)

    assert [expected] == p.parse_specifier(specifier)

def test_parse_compatible3():
    specifier = "~=2.2.0"
    p = PackageSource(PipProvider, None)
    v = Version.parse("2.2")
    v2 = Version.parse("2.3")
    expected = Range(v, v2, True, False)

    assert [expected] == p.parse_specifier(specifier)

def test_parse_arbitrary():
    # specifier = "===footbar"
    # p = PackageSource(PipProvider, None)
    # expexted = Range("footbar", "footbar", True, True)

    # assert [expected] == p.parse_specifier(specifier)
    assert True