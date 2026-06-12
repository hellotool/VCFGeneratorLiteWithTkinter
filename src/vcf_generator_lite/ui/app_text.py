from gettext import pgettext

from vcf_generator_lite.__version__ import __version__


def app_name() -> str:
    return pgettext("app.name", "VCF Generator Lite")


def app_description() -> str:
    return pgettext("app.description", "Generate VCF files from contacts")


def repository_url() -> str:
    return pgettext("app.url_repository", "https://github.com/hellotool/VCFGeneratorLiteWithTkinter")


def documentation_url() -> str:
    return pgettext("app.url_documentation", "{repository}/tree/{version}/docs").format(
        repository=repository_url(),
        version=f"v{__version__}",
    )


def third_party_notices_url() -> str:
    return pgettext("app.url_third_party_notices", "{repository}/blob/{version}/NOTICES.md").format(
        repository=repository_url(),
        version=f"v{__version__}",
    )


def error_for(exception: BaseException) -> str:
    from vcf_generator_lite.models.contact import MissingNumberError

    if isinstance(exception, MissingNumberError):
        return pgettext("error_missing_number", "Missing number or number is incorrect")
    return str(exception)
