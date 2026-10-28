# Learning Python

Small programs I wrote myself while learning Python. They're practice, not products: each one tries out one library or idea.

| Folder | What's in it |
|---|---|
| [`automation-scripts/`](automation-scripts/) | 31 short scripts: renaming and organising files, backups, PDF text extraction, image resizing and downloading, Excel automation, web scraping, site monitoring, text-to-speech, desktop notifications, sending email, a weather API call, and a few classes (`class_Car.py`, `circle_Class.py`, `user.py`) |
| [`pyqt-practice/`](pyqt-practice/) | First PyQt5 windows: layouts, buttons, text input, a combo box, and importing one module from another |
| [`document-writer/`](document-writer/) | Building a Word document page with python-docx |

## Changes for publishing

- Email login details and personal file paths were replaced with environment variables or placeholders.
- A few files began with notebook-style `!pip install` lines, which aren't valid Python in a `.py` file. They're now comments that say what to install.
- Fixed one typo in `resize_images.py` (`8` where `*` was meant) so every file compiles.

Scripts that need credentials read them from environment variables, for example `EMAIL_USER`, `EMAIL_PASS` and `EMAIL_TO` for `auto_email.py`.
