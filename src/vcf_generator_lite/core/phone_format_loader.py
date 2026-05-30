import logging

from vcf_generator_lite.configs.phone_formats import PHONE_FORMATS
from vcf_generator_lite.models.phone_format import PhoneFormat

_logger = logging.getLogger(__name__)


def load_country_phone_formats() -> dict[str, PhoneFormat]:
    result: dict[str, PhoneFormat] = {}
    for fmt in PHONE_FORMATS:
        if fmt.id in result:
            result[fmt.id] += fmt
        else:
            result[fmt.id] = fmt
    _logger.debug("Loaded %d country phone formats", len(result))
    return result
