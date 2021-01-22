from utils.config import Config
import math


def sanitize_path(path: str):
    return path.strip(' ').strip('/')


def generate_url(key: str):
    return f'{Config.APP.HOSTNAME}/media/{sanitize_path(key)}'


def generate_s3_url(key: str):
    return f'{Config.APP.HOSTNAME}/s3/{sanitize_path(key)}'


def destructure_url(url: str) -> list[str]:
    parts = sanitize_path(url).replace(f'{Config.APP.HOSTNAME}/media/', '').split('/')
    if len(parts) < 2:
        raise Exception('Invalid url')
    bucket = parts[0]
    path = parts[1:len(parts)-1]
    file_name = parts[len(parts) - 1]
    return [bucket, '/'.join(path), file_name]


def valid_size(width, height):
    return [width, height] in Config.MEDIA.SIZES_ALLOWED


# Returns closest permissible size to input width and height. Ensures output is not equal to input values.
def closest_valid_size(width: int, height: int) -> (int, int):
    width_to_set, height_to_set, diff = -1, -1, -1
    for [allowed_width, allowed_height] in Config.MEDIA.SIZES_ALLOWED:
        cur_diff = math.pow(width - allowed_width, 2) + math.pow(height - allowed_height, 2)
        if (diff == -1 or cur_diff < diff) and (width != allowed_width and height != allowed_height):
            width_to_set, height_to_set = allowed_width, allowed_height
            diff = cur_diff
    return width_to_set, height_to_set


def get_from_dict(obj: dict, fields: list[str]) -> list:
    return [obj.get(field) for field in fields]


def validate(obj, _type, key):
    if type(obj) == _type:
        return obj
    raise Exception(f'{key} must be f{_type}')
