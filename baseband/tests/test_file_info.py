# Licensed under the GPLv3 - see LICENSE
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import importlib
import pytest
from astropy.time import Time
import astropy.units as u

from .. import file_info
from ..data import (SAMPLE_MARK4 as SAMPLE_M4, SAMPLE_MARK5B as SAMPLE_M5B,
                    SAMPLE_VDIF, SAMPLE_MWA_VDIF as SAMPLE_MWA, SAMPLE_DADA,
                    SAMPLE_GSB_RAWDUMP_HEADER, SAMPLE_GSB_RAWDUMP,
                    SAMPLE_GSB_PHASED_HEADER, SAMPLE_GSB_PHASED)


@pytest.mark.parametrize(
    ('sample', 'format_'),
    ((SAMPLE_M4, 'mark4'),
     (SAMPLE_M5B, 'mark5b'),
     (SAMPLE_VDIF, 'vdif'),
     (SAMPLE_MWA, 'vdif'),
     (SAMPLE_DADA, 'dada'),
     (SAMPLE_GSB_RAWDUMP_HEADER, 'gsb'),
     (SAMPLE_GSB_PHASED_HEADER, 'gsb')))
def test_basic_file_info(sample, format_):
    info = file_info(sample)
    info_dict = info()
    assert info.format == format_
    assert info_dict['format'] == format_
    if format_.startswith('mark') or format_.startswith('gsb'):
        assert info.missing
        assert 'missing' in info_dict
    else:
        assert not info.missing
        assert 'missing' not in info_dict


@pytest.mark.parametrize(
    ('sample', 'missing'),
    ((SAMPLE_M4, {'decade', 'ref_time'}),
     (SAMPLE_M5B, {'kday', 'ref_time', 'nchan'})))
def test_open_missing_args(sample, missing):
    info = file_info(sample)
    assert info.missing
    assert set(info.missing) == missing


@pytest.mark.parametrize(
    ('sample', 'format_', 'used_extra_args'),
    ((SAMPLE_M4, 'mark4', ('ref_time',)),
     (SAMPLE_M5B, 'mark5b', ('ref_time', 'nchan')),
     (SAMPLE_VDIF, 'vdif', ()),
     (SAMPLE_DADA, 'dada', ())))
def test_file_info(sample, format_, used_extra_args):
    # Pass on extra arguments needed to get Mark4 and Mark5B to pass.
    # For GSB, we also need raw files, so we omit them.
    extra_args = {'ref_time': Time('2014-01-01'),
                  'nchan': 8}
    info = file_info(sample, **extra_args)
    assert info.format == format_
    assert not info.missing
    info_dict = info()
    for attr in info.attr_names:
        assert getattr(info, attr) is not None
        assert attr in info_dict
    assert all(arg in info.kwargs for arg in used_extra_args)
    # Check we can indeed open a file with those extra arguments.
    module = importlib.import_module('.' + info.format, package='baseband')
    with module.open(sample, mode='rs', **info.kwargs) as fh:
        info2 = fh.info
    assert info2() == info_dict


@pytest.mark.parametrize(
    ('sample', 'raw', 'mode'),
    ((SAMPLE_GSB_RAWDUMP_HEADER, SAMPLE_GSB_RAWDUMP, 'rawdump'),
     (SAMPLE_GSB_PHASED_HEADER, SAMPLE_GSB_PHASED, 'phased')))
def test_gsb_with_raw_files(sample, raw, mode):
    info = file_info(sample, raw=raw)
    assert info.format == 'gsb'
    assert not info.missing
    module = importlib.import_module('.' + info.format, package='baseband')
    # Check we can indeed open a file with the extra arguments.
    with module.open(sample, mode='rs', **info.kwargs) as fh:
        info2 = fh.info
    assert info2() == info()
