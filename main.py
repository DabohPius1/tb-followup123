from datetime import date, datetime, timedelta
import json
import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


def add_days(start, days):
    return start + timedelta(days=days)


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=20, spacing=15)

        root.add_widget(Label(
            text="TB PATIENT FOLLOW-UP",
            font_size=26,
            bold=True,
            size_hint_y=None,
            height=60
        ))
        root.add_widget(Label(
            text="Calculate and save follow-up dates",
            font_size=17,
            size_hint_y=None,
            height=40
        ))

        new_btn = Button(text="NEW PATIENT", font_size=19, size_hint_y=None, height=60)
        new_btn.bind(on_press=lambda *_: setattr(self.manager, "current", "new"))
        root.add_widget(new_btn)

        saved_btn = Button(text="SAVED PATIENTS", font_size=19, size_hint_y=None, height=60)
        saved_btn.bind(on_press=lambda *_: setattr(self.manager, "current", "patients"))
        root.add_widget(saved_btn)

        root.add_widget(Label(
            text="Follow-up schedule:\nMonth 2 = +56 days\nMonth 5 = +140 days\nMonth 6 = +168 days",
            font_size=17
        ))
        self.add_widget(root)


class NewPatientScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=20, spacing=12)

        root.add_widget(Label(text="NEW TB PATIENT", font_size=24, bold=True,
                              size_hint_y=None, height=55))

        self.name_input = TextInput(hint_text="Patient name", multiline=False,
                                    font_size=18, size_hint_y=None, height=55)
        self.id_input = TextInput(hint_text="Patient ID", multiline=False,
                                  font_size=18, size_hint_y=None, height=55)
        self.date_input = TextInput(
            hint_text="Treatment start date: DD-MM-YYYY",
            multiline=False, font_size=18, size_hint_y=None, height=55
        )

        root.add_widget(self.name_input)
        root.add_widget(self.id_input)
        root.add_widget(self.date_input)

        calc = Button(text="CALCULATE & SAVE", font_size=18,
                      size_hint_y=None, height=60)
        calc.bind(on_press=self.calculate_save)
        root.add_widget(calc)

        back = Button(text="BACK", size_hint_y=None, height=50)
        back.bind(on_press=lambda *_: setattr(self.manager, "current", "home"))
        root.add_widget(back)

        self.result = Label(text="", font_size=17)
        root.add_widget(self.result)

        self.add_widget(root)

    def calculate_save(self, *_):
        name = self.name_input.text.strip()
        patient_id = self.id_input.text.strip()
        date_text = self.date_input.text.strip()

        if not name or not patient_id or not date_text:
            self.result.text = "Please enter patient name, ID and start date."
            return

        try:
            start = datetime.strptime(
                date_text.replace("/", "-").replace(".", "-"), "%d-%m-%Y"
            ).date()
        except Exception:
            self.result.text = "Invalid date. Use DD-MM-YYYY."
            return

        record = {
            "name": name,
            "patient_id": patient_id,
            "start_date": start.strftime("%d-%m-%Y"),
            "month_2": add_days(start, 56).strftime("%d-%m-%Y"),
            "month_5": add_days(start, 140).strftime("%d-%m-%Y"),
            "month_6": add_days(start, 168).strftime("%d-%m-%Y"),
        }

        app = App.get_running_app()
        app.records.append(record)
        app.save_records()

        self.result.text = (
            f"Saved successfully!\n\n"
            f"Patient: {name}\n"
            f"ID: {patient_id}\n\n"
            f"Start: {record['start_date']}\n"
            f"Month 2: {record['month_2']}\n"
            f"Month 5: {record['month_5']}\n"
            f"Month 6: {record['month_6']}"
        )

        self.name_input.text = ""
        self.id_input.text = ""
        self.date_input.text = ""


class PatientsScreen(Screen):
    def on_pre_enter(self):
        self.refresh()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=15, spacing=10)
        root.add_widget(Label(text="SAVED PATIENTS", font_size=24, bold=True,
                              size_hint_y=None, height=55))

        self.scroll = ScrollView()
        self.list_box = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        self.scroll.add_widget(self.list_box)
        root.add_widget(self.scroll)

        back = Button(text="BACK", size_hint_y=None, height=50)
        back.bind(on_press=lambda *_: setattr(self.manager, "current", "home"))
        root.add_widget(back)
        self.add_widget(root)

    def refresh(self):
        self.list_box.clear_widgets()
        records = App.get_running_app().records

        if not records:
            self.list_box.add_widget(Label(
                text="No saved patients.",
                size_hint_y=None, height=50
            ))
            return

        for i, r in enumerate(records):
            text = (
                f"{r['name']} | ID: {r['patient_id']}\n"
                f"Start: {r['start_date']}   "
                f"M2: {r['month_2']}   M5: {r['month_5']}   M6: {r['month_6']}"
            )
            btn = Button(text=text, halign="left", valign="middle",
                         size_hint_y=None, height=120)
            btn.bind(width=lambda b, w: setattr(b, "text_size", (w - 20, None)))
            btn.bind(on_press=lambda _, index=i: self.confirm_delete(index))
            self.list_box.add_widget(btn)

    def confirm_delete(self, index):
        def delete(*_):
            app = App.get_running_app()
            del app.records[index]
            app.save_records()
            popup.dismiss()
            self.refresh()

        box = BoxLayout(orientation="vertical", padding=15, spacing=10)
        box.add_widget(Label(text="Delete this patient record?"))
        yes = Button(text="DELETE", size_hint_y=None, height=50)
        no = Button(text="CANCEL", size_hint_y=None, height=50)
        box.add_widget(yes)
        box.add_widget(no)
        popup = Popup(title="Confirm deletion", content=box,
                      size_hint=(0.85, 0.4))
        yes.bind(on_press=delete)
        no.bind(on_press=popup.dismiss)
        popup.open()


class TBFollowupApp(App):
    def build(self):
        self.records = []
        self.load_records()

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(NewPatientScreen(name="new"))
        sm.add_widget(PatientsScreen(name="patients"))
        return sm

    def data_file(self):
        return os.path.join(self.user_data_dir, "patients.json")

    def load_records(self):
        try:
            with open(self.data_file(), "r", encoding="utf-8") as f:
                self.records = json.load(f)
        except Exception:
            self.records = []

    def save_records(self):
        os.makedirs(self.user_data_dir, exist_ok=True)
        with open(self.data_file(), "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)


if __name__ == "__main__":
    TBFollowupApp().run()
