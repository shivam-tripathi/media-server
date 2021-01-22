from utils.helpers import destructure_url, valid_size, generate_s3_url, closest_valid_size
from utils.config import Config
from utils.s3 import S3
from datetime import datetime, timedelta


def get_resource_url(url: str, width: int, height: int) -> (str, bool):
    s3 = S3()

    # If size params are not integers, set default size
    if type(width) != int or type(height) != int:
        [width, height] = Config.MEDIA.DEFAULT_SIZE

    if not valid_size(width, height):
        width, height = closest_valid_size(width, height)

    [bucket, path, file_name] = destructure_url(url)

    # Assert if original file exists. If original file is missing, raise exception.
    key = f'{path}/{file_name}'
    _, original_file_header = s3.assert_file_exists(bucket, key, True)

    # width <= 0 or height <= 0 returns original file
    if width <= 0 and height <= 0:
        return generate_s3_url(key), True

    # Valid sizes append to key to create a new key
    s3_key = f'{key}_{width}_{height}'
    file_exists, file_header, error = s3.assert_file_exists(bucket, s3_key)
    # If file is not found, it could be because:
    #   - It has not been processed for this size yet
    #   - It is in the processing queue for conversion to this size
    # We trigger action for conversion to this size (by principle of laziness).
    # Issues like cache-stampede and conversion failures would be handled at the conversion handler level.
    if not file_exists:
        if error.response.get('Error', {}).get('Code') in ['404', 404]:
            # trigger new size conversion and return original
            return generate_s3_url(key), False
        else:
            raise Exception(error)

    return generate_s3_url(s3_key), True
