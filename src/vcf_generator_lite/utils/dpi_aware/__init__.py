from vcf_generator_lite.utils.environment import is_windows

if is_windows:
    from vcf_generator_lite.utils.dpi_aware.windows_impl import enable_dpi_aware
else:
    from vcf_generator_lite.utils.dpi_aware.no_impl import enable_dpi_aware

__all__ = ["enable_dpi_aware"]
