from pathlib import Path, PurePath

from PyInstaller.building.api import COLLECT, EXE, PYZ
from PyInstaller.building.build_main import Analysis
from PyInstaller.utils.win32.versioninfo import (
    FixedFileInfo,
    StringFileInfo,
    StringStruct,
    StringTable,
    VarFileInfo,
    VarStruct,
    VSVersionInfo,
)

from scripts.app_metadata import app_metadata, app_version_variants
from vcf_generator_lite.constants import APP_COPYRIGHT

PATH_PROJECT = Path()
PATH_SOURCE_MODULE = PATH_PROJECT / "src" / "vcf_generator_lite"

DIST_PATH_MODULE = PurePath("vcf_generator_lite")

a = Analysis(
    [PATH_SOURCE_MODULE / "__main__.py"],
    pathex=[],
    binaries=[],
    datas=[(PATH_SOURCE_MODULE / "resources", DIST_PATH_MODULE / "resources")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="vcf-generator-lite",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[PATH_PROJECT / "assets" / "images" / "icon.ico"],
    version=VSVersionInfo(
        # For more details about fixed file info 'ffi' see:
        # http://msdn.microsoft.com/en-us/library/ms646997.aspx
        ffi=FixedFileInfo(
            # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
            # Set not needed items to zero 0. Must always contain 4 elements.
            filevers=app_version_variants.windows_ffi,
            prodvers=app_version_variants.windows_ffi,
            # Contains a bitmask that specifies the valid bits 'flags'r
            mask=0x3F,
            # Contains a bitmask that specifies the Boolean attributes of the file.
            flags=0x0,
            # The operating system for which this file was designed.
            # 0x4 - NT and there is no need to change it.
            OS=0x40004,
            # The general type of file.
            # 0x1 - the file is an application.
            fileType=0x1,
            # The function of the file.
            # 0x0 - the function is not defined for this fileType
            subtype=0x0,
            # Creation date and time stamp.
            date=(0, 0),
        ),
        kids=[
            # TODO @Jesse205: 本地化  # noqa: FIX002, TD003
            StringFileInfo(
                [
                    StringTable(
                        "040904B0",
                        [
                            StringStruct("CompanyName", app_metadata.author),
                            StringStruct("FileVersion", app_version_variants.wheel),
                            StringStruct("InternalName", app_metadata.display_name),
                            StringStruct("LegalCopyright", APP_COPYRIGHT),
                            StringStruct("OriginalFilename", "vcf-generator-lite.exe"),
                            StringStruct("ProductName", app_metadata.display_name),
                            StringStruct("ProductVersion", app_version_variants.wheel),
                        ],
                    ),
                ]
            ),
            # https://learn.microsoft.com/zh-cn/windows/win32/menurc/varfileinfo-block
            VarFileInfo([VarStruct("Translation", [0x0804, 1200, 0x0409, 1200])]),
        ],
    ),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="vcf_generator_lite",
)
