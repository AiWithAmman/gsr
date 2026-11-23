# Windows Settings Clone (Privacy & Security)

This is our remake of the **Privacy & security** part of Windows 11 Settings, made with Python and tkinter.

## Why we made this

We started with a simple question: do people actually know what their Windows privacy settings do? Most don't, and a lot of them don't know how much data Windows collects about them either. When we looked into it, we found that people couldn't even find half of these settings, because they're buried a few pages deep with vague descriptions.

So the project ended up with three goals:

1. Show people what their privacy settings are and what Windows collects
2. Make the settings easier to get to, so you don't have to dig through menus
3. Explain each setting better than the real app does

We only rebuilt Privacy & security. The app opens on a basic Home page like real Settings does, and the other sections in the sidebar (System, Apps and so on) are just placeholders so it still looks like Windows.

## What's in it

- A **Privacy Dashboard** at the top with cards for the important stuff: recent changes, activity, camera, mic, location and diagnostic data
- A **privacy history** page that shows what you changed and lets you undo it
- A small **popup** every time a privacy setting changes
- All the pages from the real Privacy & security section:
  - Security: Windows Security, Find my device, Device encryption, For developers
  - Windows permissions: General, Speech, Inking & typing, Diagnostics & feedback, Activity history, Search
  - App permissions: Location, Camera, Microphone, Notifications, Contacts, Calendar, Documents, Pictures and the rest (25 pages)
- Per-app toggles. If you turn off the main switch, the app switches under it grey out like they do in Windows.
- A search box in the sidebar for finding privacy pages
- A back button and breadcrumbs at the top. `Alt + ←` goes back too.
- Your switches get saved, so they're still there next time you open it

## Download

If you just want to try it, grab `PrivacySettings.exe` from the [Releases](../../releases) page and double-click it. You don't need Python.

Windows might show a "Windows protected your PC" warning since the file isn't signed. Click **More info → Run anyway**.

## Running from the code

You need Python 3.8 or newer. tkinter comes with the normal Windows installer, and there's nothing else to install.

```bash
git clone <repo-url>
cd gsr
python Main.py
```

If `python` doesn't work, try `py Main.py`.

It runs on Mac and Linux too, but it looks best on Windows 11 because it uses the Segoe UI font and Windows icons.

## Building the .exe yourself

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name PrivacySettings Main.py
```

The exe shows up in the `dist` folder.

## How the files are laid out

```
gsr/
├── Main.py                  # main window, switching pages, back button, search
├── Components/
│   ├── Theme.py             # colors, fonts, icons
│   ├── Buttons.py           # toggle switch, buttons, links
│   ├── Cards.py             # the setting rows, cards, dropdown sections, scrolling
│   ├── Sidebar.py           # left side menu
│   └── State.py             # saves the settings to a json file
└── pages/
    ├── Home.py              # home page
    ├── Privacy_security.py  # privacy page, dashboard, history and the subpages
    └── Diagnostic.py        # diagnostics & feedback page
```

## Adding a page

Every page file has a `build(parent, app)` function that puts the widgets on the page, plus a `routes()` function that gives the page an id and a title:

```python
from Components.Cards import section_header, toggle_row

def build(parent, app):
    section_header(parent, "Example")
    toggle_row(parent, app.store, "example.enabled", "Enable example",
               "This gets saved automatically", icon="settings")

def routes():
    return {"privacy/example": ("Example", build)}
```

Then add `self.routes.update(YourFile.routes())` in `Main.py`. The id decides the breadcrumb, so `privacy/example` shows up as **Privacy & security › Example**.

## Resetting everything

Close the app and delete `settings_state.json`.

## Heads up

- Nothing in here changes your real Windows settings. It's a prototype, so buttons like "Open Windows Security" just show a message.
- Only Home and Privacy & security work. The rest of the sidebar is placeholders.
- We're not connected to Microsoft in any way. Windows is a trademark of Microsoft.

## License

[MIT](LICENSE)
