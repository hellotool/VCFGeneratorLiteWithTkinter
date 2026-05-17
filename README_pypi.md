# VCF Generator Lite ![with Tkinter](https://img.shields.io/badge/with-Tkinter-00319C)

VCF Generator Lite is a simple and efficient tool that converts contact lists into a single vCard (`.vcf`) file. Generated files can be batch-imported into mobile phone contacts or used for various other purposes. Built with Python and Tkinter for a native desktop experience.

## Features

- **Smart Parsing**: Batch contacts in `Name Phone Note` format (note optional), automatically handles tabs and spaces.
- **Batch Generation**: Combines all contacts into a single `.vcf` file.
- **Number Validation**: Automatically skips invalid numbers and quickly locates error rows.
- **Editing Assistance**: Displays line numbers in text area, supports one-click quote removal.

## Usage

1. Copy the name and phone number in the format of `Name Phone Note` on each line into the text field below. The note can be omitted.
   ```text
   Qu Yuan		13333333333	Poet of the Warring States period
   Cao Cao		13444444444
   Tao Y.M.	13555555555
   Xie Lingyun	13666666666
   ```
2. Click **Generate**, select a path to save the file.
3. You can use the generated vCard file wherever you need it.

> [!NOTE]
>
> - You can use both tabs and spaces to separate the fields.
> - The program will automatically remove extra spaces from the text field.
>
> Example: `Han Meimei   13333333333   A   well-known girl` will be recognized as
>
> | Name       | Phone       | Note              |
> | ---------- | ----------- | ----------------- |
> | Han Meimei | 13333333333 | A well-known girl |

## License

This project is licensed under the Apache 2.0 license. For details, please refer to the [LICENSE file](https://github.com/hellotool/VCFGeneratorLiteWithTkinter/blob/master/LICENSE).
