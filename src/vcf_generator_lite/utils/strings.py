from vcf_generator_lite.utils.l10n import pgettext


def get_app_name() -> str:
    return pgettext("app.name", "VCF Generator Lite")


def get_app_description():
    return pgettext("app.description", "Generate VCF files from contacts")
