<!-- markdownlint-disable no-duplicate-heading -->

# Changelog

[简体中文](./CHANGELOG.zh-CN.md) |
**English**

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Python Packaging Version Specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/).

The logs in "Unreleased" are scattered across various language files and will be merged when a new version is released.

## [Unreleased]

## [5.0.4] - 2026-05-07

### Added

- Added changelog.

### Fixed

- Fixed spacing between all components.
- Fixed parameter error in the app icon.

### Changed

- Changed example contacts to ancient Chinese poets.
- Reorganized project documentation.

## [5.0.3] - 2026-04-28

### Added

- Windows GUI version now displays CLI output in a message box, e.g. `.\vcf-generator-lite.exe --version`.

### Fixed

- Fixed the overflow issue on the right side of the list in the Invalid Contacts dialog.

### Removed

- Removed the resize control on Linux.

## [5.0.2] - 2026-04-16

### Changed

- Optimized Invalid Contacts dialog loading: window now displays first, then inserts data asynchronously for faster response.

### Fixed

- Excessive vertical margin of the Invalid Contacts dialog title.
- Unexpected shortcut key display in the Stop Generation menu item.
- Application freeze caused by exceptions when closing files.
- File selection confusion when falling back to another language.
- Occasional crashes and errors when using the software in English.

### Removed

- Removed warning log generation when encountering invalid contacts.

## [5.0.1] - 2026-04-15

### Added

- Introduced a theme patcher that allows users to customize theme patches and prevents patches from being applied to external themes.

### Fixed

- Fixed an issue where fonts might not be found when using a custom theme.
- Fixed an issue where the background color of child windows did not follow the theme.
- Added high DPI support for some components in the save dialog on Linux.
- Fixed an issue where warning icons were too large on Linux.

### Changed

- Refactored parts of the project code.

## [5.0.0] - 2026-04-06

### Added

- The build number on Windows now accommodates pre-release, post-release, and development code identifiers.
- Added support for stopping file generation.
- Added environment information to the About window.
- Open-sourced the icon design files and refined the icon appearance.

### Fixed

- Fixed the missing shebang line when packaging with zipapp.
- Linux version no longer forces centering on the screen, resolving centering misalignment across multiple monitors.
- Fixed the issue where locating an error number did not automatically scroll to it.
- Fixed an incorrect link reference.

### Changed

- Performed a full refactoring of the project code.
- Improved the wording of interface text.
- Improved the project's file structure.

## [4.4.1] - 2026-03-11

### Added

- Added support for Python Wheel distribution.
- Added support for displaying darwin-style shortcuts.
- Editor now always highlights selected text for easier error location.

### Fixed

- Refactored VCF generator implementation to fix thread pool leak issue.
- Fixed path separator incorrectly using `/` on Windows.
- Fixed tree view row height calculation issue under high DPI scaling.
- Fixed issue where symbol bar could be accidentally selected on Linux.

### Changed

- Removed themed background Frame for minor performance improvement.
- Code cleanup for better maintainability.

## [4.4.0] - 2026-02-15

### Added

- Added line numbers to the main window editor, supporting line selection by clicking on line numbers and continuous multi-line selection by dragging.
- Double-click any table item in the error row display window to quickly jump to the corresponding position in the original text.
- Added redo keyboard shortcut for X11 window systems.
- After successful file generation, automatically display performance time consumption and total line count statistics.

### Changed

- Reduced the text length of the Reason field in the error row display window and implemented Chinese localization.
- Upgraded to Python 3.14t, the free-threaded version, significantly reducing main thread blocking.
- Migrated to the `uv` toolchain for improved dependency management and build efficiency.
- Supplemented and improved multiple unit tests to increase code robustness.

## [4.3.0] - 2025-12-31

### Added

- Added preliminary support for the English interface; user-customized translations are not yet supported.
- When contact errors occur, the Invalid Contacts dialog explicitly shows the error cause.
- Users are notified when opening a link fails.
- Added a divider between the title and content in Invalid Contacts dialog for better readability.
- Warning icons in Invalid Contacts dialog are now colored for clearer identification.
- Colored log output is enabled during development for easier debugging.
- Increased test coverage for improved stability.

### Fixed

- Fixed icon scaling issues in the About dialog by removing it.
- Fixed all known text box issues in the About dialog by removing it.

### Changed

- The About window is replaced with a simpler About info box.
- Removed compilation dependencies for Zip apps, enabling support for multiple Python interpreter versions.
- Explicit theme settings are removed; themes are refactored as patches to prepare for future custom theme support.
- The shortcut for the Generate button is changed from `Ctrl+S` to `Ctrl+G`.
- The Generate button now displays a busy state during file generation for better feedback.
- Classes and functions for the menu-building DSL are deleted.
- Streamlined the code logic for enabling DPI awareness.
- Renamed `os_notices.md` to `os-notices.md`.
- Updated certain dependencies to their latest versions.
- Optimized the application build process for efficiency.

### Removed

- Removed tkhtmlview component.

## [4.2.1] - 2025-05-30

### Fixed

- Fixed the bug that the notes were garbled.

## [4.2.0] - 2025-05-30

### Added

- Support for notes field.
- Brand new app icon.
- Invalid window warning icon uses Emoji icons.
- Automatically focuses the text box after launch.
- Access key provided for the Remove Quotes feature.

### Fixed

- Fixed centering issue on Windows; some issues still exist on Linux.
- Fixed high font scaling failure issue.

### Changed

- Project refactored.
- Window class name added.
- Open source statement moved to the website.
- Optimized generation progress bar.

## [4.1.3] - 2025-03-13

### Changed

- The installer will automatically uninstall the old version before installing the update, fixing the resource error caused by overwriting installation.
- Optimized the resource invocation logic.

## [4.1.2] - 2025-03-10

### Changed

- No functional changes; only updated documentation and build output filenames.

## [4.1.1] - 2025-03-10

### Changed

- No functional changes; only updated documentation and build output filenames.

## [4.1.0] - 2025-03-04

### Added

- Added a dialog box for the list of invalid phone numbers.

### Fixed

- Fixed the menu font error on Windows 7.

### Changed

- Optimized the UI.
- Use the filename from the last save when saving a file.

## [4.0.0] - 2025-03-01

> [!CAUTION]
> The previous version 3.0.3 had serious bugs. It is recommended to use this version or later directly.

### Added

- Support for configuration files.

### Changed

- Refactored the project code.
- Changed the license to Apache 2.0.

## [3.0.3] - 2025-02-08

> [!CAUTION]
> This version has a serious bug. The generated VCF file cannot be recognized. Please use version v4.0.0 or later directly.

### Added

- The ZipApp version supports Linux.
- The About window supports closing the window using the Enter key and the Escape key.
- The text editor supports the native theme.

### Changed

- Non-Windows systems use the Clam theme.
- Prevent closing the window while a file is being generated.

## [3.0.2] - 2025-01-28

### Changed

- Optimized the code.

## [3.0.1] - 2025-01-19

### Added

- Added zipapp format app.
- Attempting to support Linux.

### Fixed

- Fixed the issue where generated files were not closed properly.

### Changed

- Editor now uses default color settings.

## [3.0.0] - 2025-01-13

### Added

- Added menu access shortcuts and set the conversion operation shortcut to `Ctrl+S`.
- Added a progress bar display during the file generation process.
- Introduced multithreading technology to achieve parallel processing of text generation and file generation, while ensuring that the user interface is not blocked during file generation.
- Added a function to remove quotation marks.
- Added line number identification for unprocessable numbers to facilitate quick location by users.
- Merged the dialog box for completion of generation with the dialog box for unrecognized numbers, reminding users that unrecognized numbers will not be added to the file.
- Text input box now supports displaying tab characters, Tab.
- Use GitHub Actions for the compilation and packaging process.

### Fixed

- Optimized the scaling function for high-resolution screens, HiDPI, ensuring good scaling effects on Windows 7 as well.

### Changed

- Enhanced the user interface design and optimized the copywriting content.
- Upgraded the Python version to 3.13, which will no longer support Windows 7. Windows 7 users can continue to run the application by manually applying a patch.
- Set the window to display centered by default to enhance the user experience.
- Adjusted and updated the open-source license information for some libraries.

## [2.0.2] - 2024-06-21

### Changed

- Updated the app icon.
- Updated PyInstaller version.

## [2.0.1] - 2024-06-17

### Added

- Added an About page.

### Fixed

- Fixed the incorrect file extension in the Save As dialog.

### Changed

- Optimized high-DPI screen adaptation.
- Continued project refactoring.

## [2.0.0] - 2024-03-25

### Added

- Display all invalid rows after generation is complete.
- Added app icon.
- Added installer; removed direct-run and launcher methods.
- Used poetry package management tool.
- Added right-click context menu.
- Save file now supports choosing the path and filename.

### Changed

- Optimized the UI.
- Refactored the project code.
- Added HiDPI screen adaptation.
- Adjusted the usage instructions.

## [1.1] - 2023-06-12

### Added

- Automatically removes leading and trailing whitespace from each line.

## [1.0] - 2023-04-21

### Added

- Initial release.

[Unreleased]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/compare/v5.0.4...HEAD
[5.0.4]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v5.0.4
[5.0.3]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v5.0.3
[5.0.2]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v5.0.2
[5.0.1]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v5.0.1
[5.0.0]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v5.0.0
[4.4.1]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.4.1
[4.4.0]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.4.0
[4.3.0]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.3.0
[4.2.1]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.2.1
[4.2.0]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.2.0
[4.1.3]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.1.3
[4.1.2]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.1.2
[4.1.1]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.1.1
[4.1.0]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.1.0
[4.0.0]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.0.0
[3.0.3]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v3.0.3
[3.0.2]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v3.0.2
[3.0.1]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v3.0.1
[3.0.0]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v3.0.0
[2.0.2]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v2.0.2
[2.0.1]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v2.0.1
[2.0.0]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v2.0.0
[1.1]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v1.1
[1.0]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v1.0
