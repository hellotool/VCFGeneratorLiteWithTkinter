from vcf_generator_lite.utils.environment import is_windows


def enable_dpi_aware() -> bool:
    if is_windows:
        from vcf_generator_lite.utils.dpi_aware.windows_impl import windows_enable_dpi_aware

        return windows_enable_dpi_aware()

    return False
