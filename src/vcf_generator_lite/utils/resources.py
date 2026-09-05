import importlib.resources
from functools import partial
from importlib.resources.abc import Traversable

__all__ = ["read_binary", "read_image", "resources_traversable"]

# 使用 .joinpath("resources") 以兼容 Python3.12
# https://github.com/python/importlib_resources/issues/287
resources_traversable: Traversable = importlib.resources.files("vcf_generator_lite").joinpath("resources")


def read_binary(*descendants: str) -> bytes:
    # 为了兼容 Python3.12 及以下版本，不能使用 importlib.resources.read_binary
    return resources_traversable.joinpath(*descendants).read_bytes()


read_image = partial(read_binary, "images")
