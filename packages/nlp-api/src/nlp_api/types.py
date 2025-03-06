"""
Module for useful type aliases.
"""

import typing

if typing.TYPE_CHECKING:
    import types_aiobotocore_s3
    from types_aiobotocore_s3.type_defs import BlobTypeDef

    S3Client = types_aiobotocore_s3.S3Client
    Blob = BlobTypeDef
else:
    S3Client = typing.Any
    Blob = typing.Any
