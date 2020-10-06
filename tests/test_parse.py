from pip._internal.resolution.resolvelib.provider import PipProvider
from src.package_source import PackageSource
from mixology.mixology.range import Range
from mixology.mixology.union import Union

def test_parse_equal():
    specifier = "==1.0.0"
    p = PackageSource(PipProvider, None)
    expected = Range("1.0.0", "1.0.0", True, True)

    assert expected == p.parse_specifier(specifier)

def test_parse_bigger():
    specifier = ">1.0.0"
    p = PackageSource(PipProvider, None)
    expected = Range("1.0.0", None, False, False)

    assert expected == p.parse_specifier(specifier)

def test_parse_smaller():
    specifier = "<1.0.0"
    p = PackageSource(PipProvider, None)
    expected = Range(None, "1.0.0", False, False)

    assert expected == p.parse_specifier(specifier)

def test_parse_bigger_include():
    specifier = ">=1.0.0"
    p = PackageSource(PipProvider, None)
    expected = Range("1.0.0", None, True, False)

    assert expected == p.parse_specifier(specifier)

def test_parse_smaller_include():
    specifier = "<=1.0.0"
    p = PackageSource(PipProvider, None)
    expected = Range(None, "1.0.0", False, True)

    assert expected == p.parse_specifier(specifier)

def test_parse_not_equal():
    specifier = "!=1.0.0"
    p = PackageSource(PipProvider, None)
    expected = [Range(None, "1.0.0", False, False), Range("1.0.0", None, False, False)]

    assert expected == p.parse_specifier(specifier)

def test_parse_padding():
    specifier = "==12.55"
    p = PackageSource(PipProvider, None)
    expected = Range("12.55", "12.55", True, True)

    assert expected == p.parse_specifier(specifier)