from gettext import pgettext


def app_name() -> str:
    return pgettext("app.name", "VCF Generator Lite")


def app_description() -> str:
    return pgettext("app.description", "Generate VCF files from contacts")


def error_for(exception: BaseException) -> str:
    from vcf_generator_lite.models.contact import MissingNumberError

    if isinstance(exception, MissingNumberError):
        return pgettext("error.missing_number", "Missing number or number is incorrect")
    return str(exception)
