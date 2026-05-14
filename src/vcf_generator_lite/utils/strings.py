from vcf_generator_lite.utils.i18n.app_l10n import pgettext


def get_app_name() -> str:
    return pgettext("app.name", "VCF Generator Lite")


def get_app_description():
    return pgettext("app.description", "Generate VCF files from contacts")
