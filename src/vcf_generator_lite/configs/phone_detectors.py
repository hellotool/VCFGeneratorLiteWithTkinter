import re

from vcf_generator_lite.models.lazy import LazyPgettext
from vcf_generator_lite.models.phone_detector import PhoneDetector, PhoneRule

PHONE_DETECTORS: list[PhoneDetector] = [
    PhoneDetector(
        id="builtin.china.mainland",
        locale_territories={"CN"},
        name=LazyPgettext("phone_detector.china.mainland", "Chinese mainland"),
        rules=[
            PhoneRule(length={11, 14}, regex=re.compile(r"^(?:\+86)?1[3456789]\d{9}$")),
            PhoneRule(length=range(10, 16), regex=re.compile(r"^(?:\+86)?0\d{2,3}\d{7,8}$")),
        ],
    ),
    PhoneDetector(
        id="builtin.china.hongkong",
        locale_territories={"HK"},
        name=LazyPgettext("phone_detector.china.hongkong", "Hong Kong, China"),
        rules=[
            PhoneRule(length={8, 12}, regex=re.compile(r"^(?:\+852)?[5-9]\d{7}$")),
            PhoneRule(length={8, 12}, regex=re.compile(r"^(?:\+852)?[23]\d{7}$")),
        ],
    ),
    PhoneDetector(
        id="builtin.china.macau",
        locale_territories={"MO"},
        name=LazyPgettext("phone_detector.china.macau", "Macau, China"),
        rules=[
            PhoneRule(length={8, 12}, regex=re.compile(r"^(?:\+853)?6\d{7}$")),
            PhoneRule(length={8, 12}, regex=re.compile(r"^(?:\+853)?28\d{6}$")),
        ],
    ),
    PhoneDetector(
        id="builtin.china.taiwan",
        locale_territories={"TW"},
        name=LazyPgettext("phone_detector.china.taiwan", "Taiwan, China"),
        rules=[
            PhoneRule(length={10, 13}, regex=re.compile(r"^(?:\+886|0)9\d{8}$")),
            PhoneRule(length={8, 12}, regex=re.compile(r"^(?:\+886)?[2-8]\d{7}$")),
        ],
    ),
]
