# Windows Settings Clone — Privacy & Security

A desktop recreation of the Windows 11 **Settings → Privacy & security** section, built with Python and tkinter.

It recreates the Windows 11 look: a navigation sidebar, setting cards, on/off switches, collapsible sections and breadcrumb navigation. Your toggle choices are saved between runs.

## Features

- **Sidebar navigation** with a profile area, a working "Find a setting" search and all 12 Settings sections
- **Privacy & security page** with all three groups:
  - **Security**: Windows Security, Find my device, Device encryption, For developers
  - **Windows permissions**: General, Speech, Inking & typing personalization, Diagnostics & feedback, Activity history, Search permissions, Searching Windows
  - **App permissions**: 25 pages including Location, Camera, Microphone, Notifications, Contacts, Calendar, Documents, Pictures and more
- **Per-app permission toggles.** Turning off a main switch greys out the switches that depend on it.
- **Diagnostics & feedback page** with expandable sections, the Diagnostic Data Viewer toggle, delete diagnostic data and a feedback frequency dropdown
- **Breadcrumb header and back button** (`Alt + ←` also goes back)
- **Persistent state**: every switch is saved to `settings_state.json`
- **High-DPI aware**, so it stays sharp on scaled displays

## Requirements

- Python 3.8 or newer
- tkinter (included with the standard Python installer on Windows)

There are no third-party packages to install.

The app runs on macOS and Linux too, but it looks closest to Windows 11 on Windows. It uses the built-in Segoe UI and Segoe Fluent Icons fonts, and falls back to plain text symbols when those aren't installed.

## Getting started

```bash
git clone <your-repo-url>
cd gsr
python Main.py
```

If `python` isn't recognized on Windows, use `py Main.py` instead.

## Project structure

```
gsr/
├── Main.py                  # App window, page routing, breadcrumbs, back button, search
├── Components/
│   ├── Theme.py             # Colors, fonts, icon glyphs, DPI scaling
│   ├── Buttons.py           # Toggle switch, push buttons, hyperlinks
│   ├── Cards.py             # Setting cards, expanders, scroll area, layout helpers
│   ├── Sidebar.py           # Left navigation pane
│   └── State.py             # JSON-backed settings store
└── pages/
    ├── Home.py              # Home page and placeholder pages
    ├── Privacy_security.py  # Privacy & security and all its subpages
    └── Diagnostic.py        # Diagnostics & feedback page
```

## Adding a new page

1. Create a module in `pages/` with a `build(parent, app)` function that adds widgets to `parent`.
2. Expose it through a `routes()` function that returns `{"route/id": ("Page title", build)}`.
3. Register it in `Main.py` with `self.routes.update(YourModule.routes())`.

Route IDs set the breadcrumb path. For example, `privacy/camera` shows **Privacy & security › Camera**.

You can build pages from the components in `Components/Cards.py`:

```python
from Components.Cards import section_header, toggle_row

def build(parent, app):
    section_header(parent, "Example")
    toggle_row(parent, app.store, "example.enabled", "Enable example",
               "This value is saved automatically", icon="settings")
```

## Resetting settings

Close the app and delete `settings_state.json` from the project folder.

## Notes

- This is a UI clone for learning purposes. None of the controls change real system settings. Actions like "Open Windows Security" or "Clear history" only show a message.
- Sections other than Home and Privacy & security are placeholders for now.
- This project is not affiliated with or endorsed by Microsoft. Windows is a trademark of Microsoft Corporation.

## License

[MIT](LICENSE)
