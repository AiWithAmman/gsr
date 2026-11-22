import datetime
from tkinter import messagebox, ttk

from Components import Theme as T
from Components.Buttons import Button
from Components.Cards import (Expander, SettingRow, on_off, paragraph, privacy_resources,
                              section_header, stack)

FEEDBACK_FREQUENCIES= ["Automatically (Recommended)", "Always", "Once a day", "Once a week", "Never"]


def build(parent, app):
    store= app.store

    section_header(parent, "Diagnostics")
    paragraph(parent, "Required diagnostic data is always sent to help keep Windows secure, up to "
                      "date, and performing as expected.")

    diag= stack(Expander(parent, "Diagnostic data",
                          "Help improve Windows and keep it secure, up to date and working as expected",
                          "diagnostic", expanded=True))
    diag.row("Send optional diagnostic data",
             "Diagnostic data is information about your device, Windows, and how "
             "they work. It can include details such as device settings, "
             "performance, app activity, errors, and problems Windows encounters. "
             "When this is turned on, Windows sends additional optional information "
             "to Microsoft, including more details about how you use apps and features, "
             "to help improve Windows and fix problems. When turned off, this extra "
             "optional information is not sent, but required diagnostic data is still "
             "sent to help keep your device secure and working properly. ",
             toggle=store.get("diag.optional", False),
             on_toggle=lambda v: store.set("diag.optional", v))

    ink= stack(Expander(parent, "Improve inking and typing",
                         "Send optional inking and typing diagnostic data", "keyboard"))
    ink.row("Improve inking and typing",
            "Send optional inking and typing diagnostic data to help improve the language "
            "recognition and suggestion capabilities of apps and services",
            toggle=store.get("diag.inking", False), on_toggle=lambda v: store.set("diag.inking", v))

    tailored= stack(Expander(parent, "Tailored experiences",
                              "Let Microsoft use your diagnostic data for personalized tips, ads, "
                              "and recommendations", "feedback"))
    tailored.row("Tailored experiences",
                 "Let Microsoft use your diagnostic data, excluding info about websites you "
                 "browse, to offer personalized tips, ads, and recommendations",
                 toggle=store.get("diag.tailored", False),
                 on_toggle=lambda v: store.set("diag.tailored", v))

    view= stack(Expander(parent, "View diagnostic data", "View your data in the Diagnostic Data Viewer",
                          "view"))
    open_btn=None

    def viewer_changed(value):
        store.set("diag.viewer", value)
        open_btn.set_enabled(value)

    view.row("Turn on the Diagnostic Data Viewer (uses up to 1 GB of hard drive space)",
             toggle=store.get("diag.viewer", False), on_toggle=viewer_changed)
    def show_viewer():
        text= "Optional diagnostic data: "+on_off(store.get("diag.optional"))
        text= text+"\nInking & typing: "+on_off(store.get("diag.inking"))
        text= text+"\nTailored experiences: "+on_off(store.get("diag.tailored"))
        messagebox.showinfo("Diagnostic Data Viewer", text)

    f= view.frame()
    open_btn= Button(f, "Open Diagnostic Data Viewer", command=show_viewer,
                     enabled=store.get("diag.viewer", False))
    open_btn.pack(anchor="w")

    delete= stack(Expander(parent, "Delete diagnostic data",
                            "Clear diagnostic data that Microsoft has collected about this device",
                            "delete"))
    f= delete.frame()
    status= paragraph(f, f"Last delete request: {store.get('diag.last_delete', 'None')}",
                       bg=T.CARD, size=9)

    def do_delete():
        if messagebox.askyesno("Delete diagnostic data",
                               "Delete diagnostic data that has been collected about this device?"):
            stamp= datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            store.set("diag.last_delete", stamp)
            status.configure(text=f"Last delete request: {stamp}")

    Button(f, "Delete", command=do_delete).pack(anchor="w")

    section_header(parent, "Feedback")

    row= stack(SettingRow(parent, "Feedback frequency", "Windows should ask for my feedback", "feedback"))
    box= ttk.Combobox(row.right_frame, values=FEEDBACK_FREQUENCIES, state="readonly", width=26)
    box.set(store.get("diag.feedback_frequency", FEEDBACK_FREQUENCIES[0]))
    box.pack(side="right")

    def frequency_changed(event):
        store.set("diag.feedback_frequency", box.get())
        box.selection_clear()

    box.bind("<<ComboboxSelected>>", frequency_changed)

    privacy_resources(parent)


def routes():
    return {"privacy/diagnostics": ("Diagnostics & feedback", build)}
