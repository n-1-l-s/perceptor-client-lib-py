import base64
import os
from io import BufferedReader
from typing import Union, Optional

from perceptor_client_lib.internal_models import ImageContextData


def _get_file_extension(file_path: str) -> str:
    _, ext = os.path.splitext(file_path)
    if len(ext) > 0:
        return ext[1:]
    return ""


ALLOWED_EXTENSIONS = ["png", "jpg"]


def _is_valid_file_type(file_extension: str) -> bool:
    lower_c = file_extension.lower()
    return lower_c in ALLOWED_EXTENSIONS


def _assert_valid_file_type(file_extension: str) -> None:
    if not _is_valid_file_type(file_extension):
        raise Exception(f"invalid file type, allowed are: {ALLOWED_EXTENSIONS}")


def _parse_image_path(image_path: str) -> ImageContextData:
    file_extension = _get_file_extension(image_path)
    if len(file_extension) == 0:
        raise Exception("file type cannot be determined")
    _assert_valid_file_type(file_extension)

    handle = open(image_path, 'rb')
    with handle:
        return _parse_image_buffered_reader(handle, file_extension)


def _parse_image_buffered_reader(handle: BufferedReader, file_type: str) -> ImageContextData:
    content_bytes = handle.read()
    return _parse_image_from_bytes(content_bytes, file_type=file_type)


def _parse_image_from_bytes(content_bytes: bytes, file_type: str) -> ImageContextData:
    img_str = base64.b64encode(content_bytes).decode('utf-8')
    data_uri = f'data:image/{file_type};base64,{img_str}'
    return ImageContextData(data_uri=data_uri)


def convert_image_to_contextdata(image: Union[str, bytes, BufferedReader],
                                 file_type: Optional[str] = None) -> ImageContextData:

    if isinstance(image, str):
        return _parse_image_path(image)

    def check_file_type_specified() -> bool:
        return file_type is not None and isinstance(file_type, str) and len(file_type) > 0

    if isinstance(image, BufferedReader):
        if not check_file_type_specified():
            raise Exception('file type must be specified when using buffered reader')
        _assert_valid_file_type(file_type)
        return _parse_image_buffered_reader(image, file_type)

    if isinstance(image, bytes):
        if not check_file_type_specified():
            raise Exception('file type must be specified when using bytes')
        _assert_valid_file_type(file_type)
        return _parse_image_from_bytes(image, file_type)

    raise Exception('specified image object cannot be parsed')
