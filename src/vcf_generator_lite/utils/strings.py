from gettext import pgettext


def get_app_name() -> str:
    return pgettext("app.name", "VCF Generator Lite")


def get_app_description() -> str:
    return pgettext("app.description", "Generate VCF files from contacts")
