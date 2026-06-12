from functools import cache

import pytest

from vcf_generator_lite.core.phone_detector_loader import load_country_phone_detectors


@cache
def _get_detectors():
    """Cached wrapper to ensure load_country_phone_detectors is called only once."""
    return load_country_phone_detectors()


def _test_rules_match(rules, phone):
    """Assert the phone number matches at least one rule."""
    assert any(rule.test(phone) for rule in rules)


def _test_rules_not_match(rules, phone):
    """Assert the phone number matches none of the rules."""
    assert not any(rule.test(phone) for rule in rules)


class TestChinaMainlandPhoneDetector:
    """China mainland phone detector tests."""

    @pytest.fixture
    def detector(self):
        return _get_detectors()["builtin.china.mainland"]

    def test_locale_territories(self, detector):
        assert "CN" in detector.locale_territories

    @pytest.mark.parametrize(
        "phone",
        [
            # Mobile: 11 digits without +86
            "13812345678",
            "14712345678",
            "15812345678",
            "16812345678",
            "17812345678",
            "18812345678",
            "19812345678",
            # Mobile: 14 digits with +86
            "+8613812345678",
            "+8614712345678",
            "+8615812345678",
            "+8616812345678",
            "+8617812345678",
            "+8618812345678",
            "+8619812345678",
            # Landline: 3-digit area code + 8-digit number = 11
            "01012345678",
            "02112345678",
            "02512345678",
            # Landline: 4-digit area code + 7-digit number = 11
            "07551234567",
            "05711234567",
            # Landline: 3-digit area code + 7-digit number = 10 (range lower bound)
            "0101234567",
            # Landline: 4-digit area code + 8-digit number = 12
            "075512345678",
            # Landline: with +86
            "+8601012345678",
            "+8602112345678",
            "+8607551234567",
        ],
    )
    def test_valid(self, detector, phone):
        """Test valid phone numbers."""
        _test_rules_match(detector.rules, phone)

    @pytest.mark.parametrize(
        "phone",
        [
            # 2nd digit not in [3456789]
            "12812345678",
            # Length mismatch
            "1381234567",  # 10 digits, too short
            "138123456789",  # 12 digits, not 11 or 14
            "+861381234567",  # 13 digits with +86, not 14
            "+86138123456789",  # 15 digits with +86, not 14
            # Landline does not start with 0
            "1012345678",
            # Landline length outside range(10, 16)
            "010123456",  # 9 digits
            "0101234567890123",  # 16 digits
            "+8601012345",  # trailing part only 5 digits (< 7)
            "+860101234567890123",  # 20 digits
            # Empty
            "",
        ],
    )
    def test_invalid(self, detector, phone):
        """Test invalid phone numbers."""
        _test_rules_not_match(detector.rules, phone)


class TestChinaHongKongPhoneDetector:
    """Hong Kong phone detector tests."""

    @pytest.fixture
    def detector(self):
        return _get_detectors()["builtin.china.hongkong"]

    def test_locale_territories(self, detector):
        assert "HK" in detector.locale_territories

    @pytest.mark.parametrize(
        "phone",
        [
            # Mobile: 8 digits, starts with 5-9
            "51234567",
            "61234567",
            "71234567",
            "81234567",
            "91234567",
            # Mobile: 12 digits with +852
            "+85251234567",
            "+85261234567",
            "+85271234567",
            "+85281234567",
            "+85291234567",
            # Fixed line: 8 digits, starts with 2-3
            "21234567",
            "31234567",
            # Fixed line: 12 digits with +852
            "+85221234567",
            "+85231234567",
        ],
    )
    def test_valid(self, detector, phone):
        """Test valid phone numbers."""
        _test_rules_match(detector.rules, phone)

    @pytest.mark.parametrize(
        "phone",
        [
            # Starts with 4, not in any valid range
            "41234567",
            # Wrong length
            "5123456",  # 7 digits
            "512345678",  # 9 digits
            "+8525123456",  # 11 digits with +852, not 12
            "+852512345678",  # 13 digits with +852, not 12
        ],
    )
    def test_invalid(self, detector, phone):
        """Test invalid phone numbers."""
        _test_rules_not_match(detector.rules, phone)


class TestChinaMacauPhoneDetector:
    """Macau phone detector tests."""

    @pytest.fixture
    def detector(self):
        return _get_detectors()["builtin.china.macau"]

    def test_locale_territories(self, detector):
        assert "MO" in detector.locale_territories

    @pytest.mark.parametrize(
        "phone",
        [
            # Mobile: 8 digits, starts with 6
            "61234567",
            "62345678",
            "63456789",
            # Mobile: 12 digits with +853
            "+85361234567",
            "+85362345678",
            "+85363456789",
            # Fixed line: 8 digits, starts with 28
            "28123456",
            "28234567",
            "28345678",
            # Fixed line: 12 digits with +853
            "+85328123456",
            "+85328234567",
            "+85328345678",
        ],
    )
    def test_valid(self, detector, phone):
        """Test valid phone numbers."""
        _test_rules_match(detector.rules, phone)

    @pytest.mark.parametrize(
        "phone",
        [
            # Mobile: starts with 5/7/8/9, not 6
            "51234567",
            "71234567",
            "81234567",
            "91234567",
            # Mobile: wrong length
            "6123456",  # 7 digits
            "612345678",  # 9 digits
            "+8536123456",  # 11 digits with +853
            "+853612345678",  # 13 digits with +853
            # Fixed line: does not start with 28
            "27123456",
            "29123456",
            # Fixed line: wrong length
            "2812345",  # 7 digits
            "281234567",  # 9 digits
            "+8532812345",  # 11 digits with +853
            "+853281234567",  # 13 digits with +853
        ],
    )
    def test_invalid(self, detector, phone):
        """Test invalid phone numbers."""
        _test_rules_not_match(detector.rules, phone)


class TestChinaTaiwanPhoneDetector:
    """Taiwan phone detector tests."""

    @pytest.fixture
    def detector(self):
        return _get_detectors()["builtin.china.taiwan"]

    def test_locale_territories(self, detector):
        assert "TW" in detector.locale_territories

    @pytest.mark.parametrize(
        "phone",
        [
            # Mobile: 10 digits, starts with 09
            "0912345678",
            "0923456789",
            "0934567890",
            # Mobile: 13 digits with +886
            "+886912345678",
            "+886923456789",
            "+886934567890",
            # Fixed line: 8 digits, starts with 2-8
            "21234567",
            "31234567",
            "41234567",
            "51234567",
            "61234567",
            "71234567",
            "81234567",
            # Fixed line: 12 digits with +886
            "+88621234567",
            "+88631234567",
            "+88641234567",
            "+88651234567",
            "+88661234567",
            "+88671234567",
            "+88681234567",
        ],
    )
    def test_valid(self, detector, phone):
        """Test valid phone numbers."""
        _test_rules_match(detector.rules, phone)

    @pytest.mark.parametrize(
        "phone",
        [
            # Mobile: starts with 08/07, not 09
            "0812345678",
            "0712345678",
            # Mobile: wrong length
            "091234567",  # 9 digits
            "09123456789",  # 11 digits
            "+88691234567",  # 12 digits with +886
            "+8869123456789",  # 14 digits with +886
            # Fixed line: starts with 0 or 9, not in [2-8]
            "01234567",
            "91234567",
            # Fixed line: wrong length
            "2123456",  # 7 digits
            "212345678",  # 9 digits
            "+8862123456",  # 11 digits with +886
            "+886212345678",  # 13 digits with +886
        ],
    )
    def test_invalid(self, detector, phone):
        """Test invalid phone numbers."""
        _test_rules_not_match(detector.rules, phone)
