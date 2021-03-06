# Licensed under the GPLv3 - see LICENSE
from ..base.frame import FrameBase
from .header import DADAHeader
from .payload import DADAPayload


__all__ = ['DADAFrame']


class DADAFrame(FrameBase):
    """Representation of a DADA file, consisting of a header and payload.

    Parameters
    ----------
    header : `~baseband.dada.DADAHeader`
        Wrapper around the header lines, providing access to the values.
    payload : `~baseband.dada.DADAPayload`
        Wrapper around the payload, provding mechanisms to decode it.
    valid : bool, optional
        Whether the data are valid.  Default: `True`.
    verify : bool, optional
        Whether to do basic verification of integrity.  Default: `True`.

    Notes
    -----
    DADA files do not support storing whether data are valid or not on disk.
    Hence, this has to be determined independently.  If ``valid=False``, any
    decoded data are set to ``cls.fill_value`` (by default, 0).

    The Frame can also be instantiated using class methods:

      fromfile : read header and map or read payload from a filehandle

      fromdata : encode data as payload

    Of course, one can also do the opposite:

      tofile : method to write header and payload to filehandle

      data : property that yields full decoded payload

    One can decode part of the payload by indexing or slicing the frame.

    A number of properties are defined: `shape`, `dtype` and `size` are
    the shape, type and number of complete samples of the data array, and
    `nbytes` the frame size in bytes.  Furthermore, the frame acts as a
    dictionary, with keys those of the header.  Any attribute that is not
    defined on the frame itself, such as ``.time`` will be looked up on the
    header as well.
    """
    _header_class = DADAHeader
    _payload_class = DADAPayload
