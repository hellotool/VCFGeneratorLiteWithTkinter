from gettext import pgettext

from vcf_generator_lite.__version__ import __version__


def app_name() -> str:
    return pgettext("app.name", "VCF Generator Lite")


def app_description() -> str:
    return pgettext("app.description", "Generate VCF files from contacts")


def repository_url() -> str:
    return pgettext("app.url_repository", "https://github.com/hellotool/VCFGeneratorLiteWithTkinter")


def releases_url() -> str:
    return pgettext("app.url_releases", "{repository}/releases").format(
        repository=repository_url(),
    )


def report_url() -> str:
    return pgettext("app.url_report", "{repository}/issues/new/choose").format(
        repository=repository_url(),
    )


def license_url() -> str:
    return pgettext("app.url_license", "{repository}/blob/{reference}/LICENSE").format(
        repository=repository_url(),
        reference=f"v{__version__}",
    )


def documentation_url() -> str:
    return pgettext("app.url_documentation", "{repository}/tree/{reference}/docs").format(
        repository=repository_url(),
        reference=f"v{__version__}",
    )


def third_party_notices_url() -> str:
    return pgettext("app.url_third_party_notices", "{repository}/blob/{reference}/NOTICES.md").format(
        repository=repository_url(),
        reference=f"v{__version__}",
    )


def error_for(exception: BaseException) -> str:
    from vcf_generator_lite.models.contact import MissingNumberError

    if isinstance(exception, MissingNumberError):
        return pgettext("error_missing_number", "Missing number or number is incorrect")
    return str(exception)
