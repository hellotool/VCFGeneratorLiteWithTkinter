# Contribution Guidelines

[简体中文](./CONTRIBUTING.zh-CN.md) |
**English**

First and foremost, thank you for considering contributing to **VCF Generator Lite**!

We welcome contributions of any kind, whether it's reporting issues, suggesting improvements, fixing bugs, or adding new features.

> [!TIP]
>
> If you're new to open source contributions, these resources might help you:
>
> - GitHub Community's [Open Source Guide][how-to-contribute-github-opensource-guide].
> - Gitee Community's [Open Source Guide][participating-gitee-opensource-guide].

## Code of Conduct

When participating in this project, please abide by our [Contributor Covenant](./CODE_OF_CONDUCT.md). We are committed to providing a friendly and inclusive community environment for everyone.

## How to Contribute

### Submitting Issues or Suggestions

If you encounter problems or have improvement suggestions while using the application, feel free to submit feedback through any of the following channels:

- [Gitee Issues][issues-gitee]
- [GitHub Issues][issues-github]

### Localizing the Application

Localization work is divided into two parts: adding new **phone formats** to support more number types, and translating **application interface** texts.

#### Adding Phone Formats

To add a new country or region phone format, follow these steps:

1. **Edit Configuration File**: Open `src/vcf_generator_lite/configs/phone_formats.py`.
2. **Add Format Entry**: Add a `CountryPhoneFormat` instance to the end of the `PHONE_FORMATS` list, using the following format:
   ```python
   CountryPhoneFormat(
       id="builtin.country.region",                # Unique identifier, lowercase dot-separated
       locale_territories={"XX"},                   # ISO 3166-1 alpha-2 territory code
       name=LazyPgettext("country", "English Name"),  # Translatable country name
       rules=[
           PhoneRule(
               length=11,                           # or [11, 14], range(10, 16), None
               regex=re.compile(r"^regex_pattern$"),
           ),
       ],
   ),
   ```
   - The `id` should be in the format `builtin.<country>.<region>`, all lowercase.
   - `locale_territories` is a set containing the territory codes where this format applies.
   - `length` field options:
     - `int`: Fixed length.
     - `list[int]`: Multiple allowed lengths (e.g., `[11, 14]` matches numbers with/without international prefix).
     - `range(min, max+1)`: Length range.
     - Omit the field: No length check, only regex matching applies.
   - Use raw strings `r"..."` if the `regex` contains backslashes.
3. **Run Checks**: Ensure your code passes Ruff and Pyright checks before submitting:

   ```bash
   uv run poe check
   ```

#### Translating the User Interface

To contribute translations to the application, follow these steps:

1. **Initialize Language Files**: If the language file does not exist, execute the following command:
   ```bash
   uv run poe l10n-init -l <language[_territory]>
   ```
   - `<language[_territory]>` follows the [POSIX specification][opengroup-pubs-posix-env], e.g., `zh_CN`, `en`, `zh_TW`.
   - `language` is an [ISO 639][iso-639] code, e.g., `zh`, `en`.
   - `territory` is an [ISO 3166][iso-3166] code, e.g., `CN`, `US`.
2. **Edit Translation Files**: Open the generated `.po` file located at:
   ```txt
   src/vcf_generator_lite/resources/locales/<locale identifier>/LC_MESSAGES/vcf-generator-lite.po
   ```
   Fill in the corresponding `msgstr` translation content based on each `msgid`. If `#, fuzzy` is automatically added, **remove this flag** after updating the translation, or the translation will be ignored during compilation.
3. **Compile Language Files**: Once translation is complete, run the following command to generate the `.mo` file:
   ```bash
   uv run poe l10n-compile -l <locale identifier>
   ```

### Participating in Development

1. Ensure there are no related pull requests (PRs) in the [Gitee repository][repository-gitee] or [GitHub repository][repository-github].
2. Fork this repository.
3. Clone the repository locally using [Git][git-homepage].
4. Read the [Development Guide](./docs/dev/index.md) to familiarize yourself with the project's development practices.
5. Create a branch, such as `feature/xxx` or `bugfix/xxx`.
6. Write your code.
7. Run the following commands to ensure the code complies with standards and introduces no errors:
   ```bash
   uv run poe format
   uv run poe check
   uv run poe test
   ```
8. Commit your code.
9. Submit a PR to this repository.

## Standards

### Code Standards

#### Python Code (`.py`)

- Function parameters must have type annotations.
- Maximum line length is 120 characters.
- For all other cases, follow [PEP 8][pep-0008].

#### Markdown Documents (`.md`)

- No maximum line length restriction.
- Refer to `.markdownlint.json` for specific rules.
- For all other cases, follow [Markdownlint][markdownlint-repository-github].

For more details, refer to `.editorconfig`.

### Documentation Standards

Follow the [Chinese Technical Documentation Style Guide][zh-style-guide].

### Git Commit Standards

Follow [Conventional Commits][conventionalcommits-homepage].

[repository-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/
[repository-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/
[issues-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/issues
[issues-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/issues

[markdownlint-repository-github]: https://github.com/DavidAnson/markdownlint
[git-homepage]: https://git-scm.com/
[conventionalcommits-homepage]: https://www.conventionalcommits.org/en/v1.0.0/

[how-to-contribute-github-opensource-guide]: https://opensource.guide/how-to-contribute/
[participating-gitee-opensource-guide]: https://gitee.com/opensource-guide/guide/participating/roles.html
[zh-style-guide]: https://zh-style-guide.readthedocs.io/zh-cn/latest/index.html

[pep-0008]: https://peps.python.org/pep-0008/
[opengroup-pubs-posix-env]: https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html]
[iso-639]: https://www.iso.org/iso-639-language-code
[iso-3166]: https://www.iso.org/iso-3166-country-codes.html
