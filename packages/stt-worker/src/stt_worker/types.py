import typing

if typing.TYPE_CHECKING:
    from types_boto3_s3.client import S3Client as S3Client
else:
    S3Client = typing.Any
