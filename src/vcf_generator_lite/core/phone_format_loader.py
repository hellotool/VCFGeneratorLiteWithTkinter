import logging
from collections.abc import Iterable
from importlib.resources.abc import Traversable

from vcf_generator_lite.configs.phone_formats import PHONE_FORMATS
from vcf_generator_lite.models.phone_format import CountryPhoneFormat
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


def filter_phone_formats_by_locale_territories(
    phone_formats: Iterable[CountryPhoneFormat],
    locale_territories: set[str],
) -> Iterable[CountryPhoneFormat]:
    """根据给定的地区集合过滤号码格式。

    :param phone_formats: 全部号码格式。
    :param locale_territories: 需要保留的地区代码集合。
    :yield: 至少有一个地区匹配的格式。
    """
    for phone_format in phone_formats:
        if any(territory in locale_territories for territory in phone_format.locale_territories):
            yield phone_format
