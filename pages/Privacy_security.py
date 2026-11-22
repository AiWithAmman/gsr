import datetime
import tkinter as tk
from tkinter import messagebox

from Components import Theme as T
from Components.Buttons import Button
from Components.Cards import (Expander, SettingRow, card_grid, option_label, paragraph,
                              privacy_resources, radio_group, section_header, stack, toggle_row)

SECURITY= [
    ("privacy/windows-security", "Windows Security",
     "Antivirus, browser, firewall, and network protection for your device", "shield"),
    ("privacy/find-my-device", "Find my device", None, "find_device"),
    ("privacy/device-encryption", "Device encryption",
     "Help protect your data with encryption", "encryption"),
    ("privacy/developers", "For developers",
     "These settings are intended for development use only", "developer"),
]

WINDOWS_PERMISSIONS= [
    ("privacy/general", "General",
     "Advertising ID, local content, app launches, settings suggestion, productivity tools", "lock"),
    ("privacy/speech", "Speech",
     "Online speech recognition for dictation and other voice-based interactions", "speech"),
    ("privacy/inking", "Inking & typing personalization",
     "Personal dictionary, words in your dictionary", "keyboard"),
    ("privacy/diagnostics", "Diagnostics & feedback",
     "Diagnostic data, inking and typing data, tailored experiences, feedback frequency", "diagnostic"),
    ("privacy/activity", "Activity history",
     "Options for getting more from your activity history across devices and accounts", "history"),
    ("privacy/search-permissions", "Search permissions",
     "SafeSearch, cloud content search, search history", "search"),
    ("privacy/searching-windows", "Searching Windows",
     "Search indexing for faster results, Find my files, folders excluded from search", "searching"),
]

COMMON_APPS= ["Feedback Hub", "Mail and Calendar", "Photos", "Settings"]
MEDIA_APPS= ["Media Player", "Paint", "Photos", "Snipping Tool"]

APP_PERMISSIONS= [
    ("location", "Location", "location", "location", ["Camera", "Maps", "Weather", "Photos"], True),
    ("camera", "Camera", "camera", "camera", ["Camera", "Feedback Hub", "Photos"], True),
    ("microphone", "Microphone", "microphone", "microphone", ["Camera", "Feedback Hub", "Sound Recorder"], True),
    ("voice-activation", "Voice activation", "voice activation", "voice", ["Voice assistant"], False),
    ("notifications", "Notifications", "notifications", "notifications", COMMON_APPS, False),
    ("account-info", "Account info", "account info", "account_info", COMMON_APPS, False),
    ("contacts", "Contacts", "contacts", "contacts", ["Mail and Calendar", "People", "Phone Link"], False),
    ("calendar", "Calendar", "calendar", "calendar", ["Mail and Calendar", "People"], False),
    ("phone-calls", "Phone calls", "phone calls", "phone", ["Phone Link"], False),
    ("call-history", "Call history", "call history", "history", ["Phone Link", "People"], False),
    ("email", "Email", "email", "email", ["Mail and Calendar"], False),
    ("tasks", "Tasks", "tasks", "tasks", ["Mail and Calendar", "To Do"], False),
    ("messaging", "Messaging", "messages", "messaging", ["Phone Link"], False),
    ("radios", "Radios", "radios", "radios", ["Settings", "Phone Link"], False),
    ("other-devices", "Other devices", "other devices", "devices", ["Settings", "Phone Link"], False),
    ("app-diagnostics", "App diagnostics", "diagnostic info about other apps", "diagnostic", ["Feedback Hub", "Settings"], False),
    ("automatic-file-downloads", "Automatic file downloads", "automatic file downloads", "download", [], False),
    ("documents", "Documents", "documents library", "document", ["Mail and Calendar", "Notepad"], True),
    ("downloads-folder", "Downloads folder", "downloads folder", "download", COMMON_APPS, True),
    ("music-library", "Music library", "music library", "music", ["Media Player"], True),
    ("pictures", "Pictures", "pictures library", "pictures", MEDIA_APPS, True),
    ("videos", "Videos", "videos library", "videos", ["Media Player", "Photos", "Clipchamp"], True),
    ("file-system", "File system", "file system", "file_system", ["Photos", "Terminal"], False),
    ("screenshot-borders", "Screenshot borders", "screenshot borders", "screenshot", ["Snipping Tool"], True),
    ("screenshots-and-apps", "Screenshots and apps", "screenshots", "screenshot", ["Snipping Tool"], True),
]


def _on_off(value):
    if value:
        return "On"
    return "Off"


def build_main(parent, app):
    store= app.store


    section_header(parent, "Privacy Dashboard")

    card_grid(parent, [
        ("Recent Privacy Changes", "View your privacy history and restore previous settings", "history", lambda: app.open("privacy/history")),

        ("Activity & Personalization", "Review activity history and personalization settings", "history", lambda: app.open("privacy/activity")),

        ("Camera", f"Camera access: {_on_off(store.get('perm.camera.access', True))}", "camera", lambda: app.open("privacy/camera")),

        ("Microphone", f"Microphone access: {_on_off(store.get('perm.microphone.access', True))}", "microphone", lambda: app.open("privacy/microphone")),

        ("Location", f"Location access: {_on_off(store.get('perm.location.access', True))}", "location", lambda: app.open("privacy/location")),

        ("Diagnostic Data", "View your diagnostic and feedback settings", "diagnostic", lambda: app.open("privacy/diagnostics")),
    ])

    section_header(parent, "Security")
    for route, title, desc, icon in SECURITY:
        if route == "privacy/find-my-device":
            desc= _on_off(store.get("security.find_my_device", True))
        stack(SettingRow(parent, title, desc, icon, on_click=lambda r=route: app.open(r)))

    section_header(parent, "Windows permissions")
    for route, title, desc, icon in WINDOWS_PERMISSIONS:
        stack(SettingRow(parent, title, desc, icon, on_click=lambda r=route: app.open(r)))

    section_header(parent, "App permissions")
    for slug, title, _noun, icon, _apps, _desktop in APP_PERMISSIONS:
        desc= _on_off(store.get(f"perm.{slug}.access", True))
        stack(SettingRow(parent, title, desc, icon,
                         on_click=lambda s=slug: app.open(f"privacy/{s}")))
    
    stack(SettingRow(
        parent,
        "Privacy activity history",
        "Review and restore previous privacy setting changes",
        "history",
        on_click=lambda: app.open("privacy/history")))


PROTECTION_AREAS= [
    ("Virus & threat protection", "No actions needed.", "shield"),
    ("Account protection", "No actions needed.", "accounts"),
    ("Firewall & network protection", "No actions needed.", "firewall"),
    ("App & browser control", "No actions needed.", "app_window"),
    ("Device security", "View status and manage hardware security features", "system"),
    ("Device performance & health", "Reports on the health of your device.", "health"),
    ("Family options", "Manage how your family uses their devices.", "family"),
]


def build_windows_security(parent, app):
    paragraph(parent, "Windows Security is your home to view and manage the security and health "
                      "of your device.")
    open_btn= Button(parent, "Open Windows Security", accent=True,
                      command=lambda: messagebox.showinfo(
                          "Windows Security", "All protection areas are up to date.\n\n"
                                              "(This is a settings clone, so no app is launched.)"))
    open_btn.pack(anchor="w", pady=(T.px(4), T.px(4)))

    section_header(parent, "Protection areas")
    for title, desc, icon in PROTECTION_AREAS:
        stack(SettingRow(parent, title, desc, icon,
                         on_click=lambda t=title: messagebox.showinfo(t, f"{t}\n\nNo actions needed.")))
    privacy_resources(parent, [("Get help", "https://support.microsoft.com/windows"),
                               ("Give feedback", "https://support.microsoft.com/")])


def build_find_my_device(parent, app):
    toggle_row(parent, app.store, "security.find_my_device", "Find my device",
               "Use your device's location to help you find it if you think you've lost it",
               icon="find_device", default=True)
    paragraph(parent, "When this is on, your device's location is periodically saved so you can "
                      "see it on a map from another device. Location services must be turned on.")
    stack(SettingRow(parent, "Location services", "Manage location access for this device",
                     "location", on_click=lambda: app.open("privacy/location")))
    privacy_resources(parent)


def build_device_encryption(parent, app):
    toggle_row(parent, app.store, "security.device_encryption", "Device encryption",
               "Helps protect your data from unauthorized access in case your device is lost or stolen",
               icon="encryption", default=True)
    stack(SettingRow(parent, "Drive encryption",
                     "Manage encryption settings for each drive on this device", "lock",
                     chevron="open",
                     on_click=lambda: messagebox.showinfo("Drive encryption",
                                                          "Drive C: is encrypted.")))
    privacy_resources(parent)


def build_developers(parent, app):
    store= app.store
    row=None

    def dev_mode_changed(value):
        if value and not messagebox.askyesno(
                "Use developer features",
                "Turning on Developer Mode, including sideloading apps and running apps from "
                "unofficial sources, could expose your device and personal data to security risks "
                "or harm your device.\n\nTurn on Developer Mode?"):
            row.set_value(False)
            return
        store.set("dev.developer_mode", value)

    row= SettingRow(parent, "Developer Mode",
                     "Install apps from any source, including loose files", "developer",
                     toggle=store.get("dev.developer_mode", False), on_toggle=dev_mode_changed)
    stack(row)
    toggle_row(parent, store, "dev.device_discovery", "Device discovery",
               "Make your device visible to USB connections and your local network",
               icon="devices", default=False)
    toggle_row(parent, store, "dev.end_task", "End task",
               "Enable end task in taskbar by right-clicking", icon="app_window", default=False)

    section_header(parent, "File Explorer")
    toggle_row(parent, store, "dev.show_extensions", "Show file extensions", icon="folder",
               default=False)
    toggle_row(parent, store, "dev.show_hidden", "Show hidden and system files", icon="folder",
               default=False)
    toggle_row(parent, store, "dev.show_full_path", "Show full path in title bar", icon="folder",
               default=False)


def build_general(parent, app):
    store= app.store
    section_header(parent, "Change privacy options")
    toggle_row(parent, store, "general.ads", "Let apps show me personalized ads by using my advertising ID")
    toggle_row(parent, store, "general.language_list",
               "Let websites show me locally relevant content by accessing my language list")
    toggle_row(parent, store, "general.app_launches",
               "Let Windows improve Start and search results by tracking app launches")
    toggle_row(parent, store, "general.suggested_content", "Show me suggested content in the Settings app")
    toggle_row(parent, store, "general.notifications", "Show me notifications in the Settings app")
    privacy_resources(parent)


def build_speech(parent, app):
    toggle_row(parent, app.store, "speech.online", "Online speech recognition",
               "Use your voice for apps using our online speech recognition technology",
               icon="speech", default=False)
    paragraph(parent, "If you turn this setting off, you can still use apps that rely on "
                      "device-based speech recognition. Online speech data is never collected "
                      "when this is off.")
    privacy_resources(parent)


def build_inking(parent, app):
    store= app.store
    toggle_row(parent, store, "inking.custom_dictionary", "Custom inking and typing dictionary",
               "Uses your typing history and handwriting patterns to create a local user dictionary",
               icon="keyboard")
    exp= stack(Expander(parent, "Personal dictionary",
                         "Words you add to the dictionary are stored on this device", "document"))
    f= exp.frame()
    status= paragraph(f, f"Last cleared: {store.get('inking.last_cleared', 'Never')}", bg=T.CARD, size=9)

    def clear():
        if messagebox.askyesno("Personal dictionary", "Clear your personal dictionary?"):
            stamp= datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            store.set("inking.last_cleared", stamp)
            status.configure(text=f"Last cleared: {stamp}")

    Button(f, "Clear your personal dictionary", command=clear).pack(anchor="w")
    privacy_resources(parent)


def build_privacy_history(parent, app):
    store = app.store

    paragraph(
        parent,
        "Review changes made to your privacy settings. "
        "You can see what changed and restore a previous value."
    )

    section_header(parent, "Recent changes")

    history = store.get_history()

    if not history:
        paragraph(parent, "No privacy setting changes have been recorded yet.")
        return

    for event in reversed(history):
        key = event.get("key", "Unknown setting")
        old_value = event.get("old_value")
        new_value = event.get("new_value")
        timestamp = event.get("timestamp", "")

        setting_name = key.replace(".", " ").replace("_", " ").title()

        if isinstance(old_value, bool):
            old_value = "On" if old_value else "Off"

        if isinstance(new_value, bool):
            new_value = "On" if new_value else "Off"

        section_header(parent, setting_name)

        paragraph(parent, f"{old_value}  ->  {new_value}\n{timestamp}")

        def restore_setting(setting_key = key, previous_value = event.get("old_value")):
            if previous_value is None:
                messagebox.showwarning("Cannot restore", "The previous value was not recorded.")
                return

            confirm = messagebox.askyesno("Restore privacy setting", f"Restore {setting_name} to its previous value?")

            if confirm:
                store.set(setting_key, previous_value)
                app.open("privacy/history")

        tk.Button( parent, text="Restore", command=restore_setting, font=T.font(9), 
            bg=T.CARD, fg=T.TEXT, relief="flat", cursor="hand2").pack(anchor="e", pady=(0, T.px(10)))


def build_activity(parent, app):
    store= app.store
    toggle_row(parent, store, "activity.store", "Store my activity history on this device",
               "Store info about websites I browse and how I use apps and services", icon="history")
    exp= stack(Expander(parent, "Clear activity history",
                         "Clear history for this account", "delete"))
    f= exp.frame()
    status= paragraph(f, f"Last cleared: {store.get('activity.last_cleared', 'Never')}", bg=T.CARD, size=9)

    def clear():
        if messagebox.askyesno("Activity history", "Clear activity history for this account?"):
            stamp= datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            store.set("activity.last_cleared", stamp)
            status.configure(text=f"Last cleared: {stamp}")

    Button(f, "Clear history", command=clear).pack(anchor="w")
    privacy_resources(parent)


SAFESEARCH= [
    ("strict", "Strict", "Filter adult text, images and videos from my web results"),
    ("moderate", "Moderate", "Filter adult images and videos but not text from my web results"),
    ("off", "Off", "Don't filter adult content from my web results"),
]


def build_search_permissions(parent, app):
    store= app.store
    current= store.get("search.safesearch", "moderate")
    exp= stack(Expander(parent, "SafeSearch", option_label(SAFESEARCH, current), "search"))

    def safesearch_changed(value):
        exp.header.set_description(option_label(SAFESEARCH, value))

    radio_group(exp.frame(), store, "search.safesearch", SAFESEARCH, "moderate",
                on_change=safesearch_changed)

    section_header(parent, "Cloud content search")
    toggle_row(parent, store, "search.cloud_microsoft", "Microsoft account",
               "Allow Windows Search to provide results from apps and services that you are signed in to",
               icon="accounts")
    toggle_row(parent, store, "search.cloud_work", "Work or School account",
               "Allow Windows Search to provide results from your work or school account",
               icon="accounts")

    section_header(parent, "History")
    toggle_row(parent, store, "search.history", "Search history on this device",
               "Improve search results by using your search history on this device", icon="history")
    def clear_search_history():
        messagebox.showinfo("Search history", "Device search history cleared.")

    row= stack(SettingRow(parent, "Delete search history on this device", icon="delete"))
    Button(row.right_frame, "Clear device search history", command=clear_search_history).pack(side="right")

    section_header(parent, "More settings")
    toggle_row(parent, store, "search.highlights", "Show search highlights",
               "See content suggestions in the search box and in search home", icon="searching")
    privacy_resources(parent)


FIND_MY_FILES= [
    ("classic", "Classic", "Only index your libraries and desktop"),
    ("enhanced", "Enhanced", "Index your entire PC. This may impact battery life and CPU consumption"),
]


def build_searching_windows(parent, app):
    store= app.store
    current= store.get("searching.mode", "classic")
    exp= stack(Expander(parent, "Find my files", option_label(FIND_MY_FILES, current), "searching",
                        expanded=True))

    def mode_changed(value):
        exp.header.set_description(option_label(FIND_MY_FILES, value))

    radio_group(exp.frame(), store, "searching.mode", FIND_MY_FILES, "classic", on_change=mode_changed)

    toggle_row(parent, store, "searching.respect_power", "Respect power settings when indexing",
               "Indexing pauses when battery saver is on or when your device is on low power",
               icon="health")
    section_header(parent, "Excluded folders")
    def add_folder():
        messagebox.showinfo("Excluded folders", "Folder picker is not available in this clone.")

    row= stack(SettingRow(parent, "Add an excluded folder", icon="folder"))
    Button(row.right_frame, "Add an excluded folder", command=add_folder).pack(side="right")
    for folder in (r"C:\ProgramData", r"C:\Users\Default\AppData", r"C:\Windows"):
        stack(SettingRow(parent, folder, icon="folder"))

    section_header(parent, "Related settings")
    stack(SettingRow(parent, "Advanced indexing options", icon="settings", chevron="open",
                     on_click=lambda: messagebox.showinfo("Indexing options",
                                                          "Indexing complete. 48,213 items indexed.")))
    privacy_resources(parent)


def make_permission_page(slug, title, noun, icon, apps, desktop):
    def build(parent, app):
        store= app.store
        master_key=f"perm.{slug}.access"
        apps_key=f"perm.{slug}.apps"
        app_rows=[]
        desktop_row=None

        def refresh(_value=None):
            master_on= store.get(master_key, True)
            apps_row.set_enabled(master_on)
            apps_on= master_on and store.get(apps_key, True)
            for r in app_rows:
                r.set_enabled(apps_on)
            if desktop_row:
                desktop_row.set_enabled(master_on)

        if slug == "location":
            master_title="Location services"
        else:
            master_title= title+" access"
        toggle_row(parent, store, master_key, master_title,
                   f"Anyone using this device can choose if their apps have access to {noun} "
                   f"when this is on", icon=icon, on_change=refresh)

        apps_row= toggle_row(parent, store, apps_key, f"Let apps access your {noun}",
                              f"Choose which apps can access your {noun}", icon="apps",
                              on_change=refresh)

        if apps:
            section_header(parent, "Apps")
            for name in apps:
                key=f"perm.{slug}.app.{name.lower().replace(' ', '_')}"
                app_rows.append(toggle_row(parent, store, key, name, icon="app_window"))

        if desktop:
            section_header(parent, "Desktop apps")
            desktop_row= toggle_row(parent, store, f"perm.{slug}.desktop",
                                     f"Let desktop apps access your {noun}",
                                     "Desktop apps that have accessed it recently appear here",
                                     icon="system")

        if slug == "location":
            section_header(parent, "Default location")

            def set_default():
                messagebox.showinfo("Default location", "Default location saved.")

            def clear_location_history():
                messagebox.showinfo("Location history", "Location history cleared.")

            row= stack(SettingRow(parent, "Default location",
                                  "Windows, apps, and services can use this when we can't detect a more "
                                  "exact location on this PC", "location"))
            Button(row.right_frame, "Set default", command=set_default).pack(side="right")
            row= stack(SettingRow(parent, "Location history",
                                  "Clear history of location data stored on this device", "history"))
            Button(row.right_frame, "Clear", command=clear_location_history).pack(side="right")

        refresh()
        privacy_resources(parent)

    return build


def routes():
    r= {
        "privacy": ("Privacy & security", build_main),
        "privacy/windows-security": ("Windows Security", build_windows_security),
        "privacy/find-my-device": ("Find my device", build_find_my_device),
        "privacy/device-encryption": ("Device encryption", build_device_encryption),
        "privacy/developers": ("For developers", build_developers),
        "privacy/general": ("General", build_general),
        "privacy/speech": ("Speech", build_speech),
        "privacy/inking": ("Inking & typing personalization", build_inking),
        "privacy/activity": ("Activity history", build_activity),
        "privacy/search-permissions": ("Search permissions", build_search_permissions),
        "privacy/searching-windows": ("Searching Windows", build_searching_windows),
        "privacy/history": ("Privacy activity history", build_privacy_history),
    }
    for slug, title, noun, icon, apps, desktop in APP_PERMISSIONS:
        r["privacy/"+slug]= (title, make_permission_page(slug, title, noun, icon, apps, desktop))
    return r
