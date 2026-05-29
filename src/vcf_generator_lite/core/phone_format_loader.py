import logging
from importlib.resources.abc import Traversable

from vcf_generator_lite.configs.phone_formats import PHONE_FORMATS
from vcf_generator_lite.utils.resources import traversable

PHONE_FORMATS_TRAVERSABLE: Traversable = traversable.joinpath("phone_formats")

_logger = logging.getLogger(__name__)


def load_country_phone_formats():
    result = {}
    for fmt in PHONE_FORMATS:
        if fmt.id in result:
            result[fmt.id] += fmt
        else:
            result[fmt.id] = fmt
    return result
