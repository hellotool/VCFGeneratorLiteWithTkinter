import logging

from vcf_generator_lite.configs.phone_detectors import PHONE_DETECTORS
from vcf_generator_lite.models.phone_detector import PhoneDetector

_logger = logging.getLogger(__name__)


def load_country_phone_detectors() -> dict[str, PhoneDetector]:
    result: dict[str, PhoneDetector] = {}
    for detector in PHONE_DETECTORS:
        if detector.id in result:
            result[detector.id] += detector
        else:
            result[detector.id] = detector
    _logger.debug("Loaded %d country phone detectors", len(result))
    return result
