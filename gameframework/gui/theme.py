from tkinter import ttk

TREBUCHET_MS = "Trebuchet MS"
TITLE_FONT = (TREBUCHET_MS, 28, "bold")
BASIC_FONT = (TREBUCHET_MS, 14)
BOLD_FONT = (TREBUCHET_MS, 14, "bold")
CARD_FONT = (TREBUCHET_MS, 18, "bold")
LEFT_MOUSE_BUTTON = "<Button-1>"


def configure_styles() -> None:
    """Erzeugt die ttk-Styles. ttk.Button/Radiobutton akzeptieren kein -font direkt."""
    style = ttk.Style()
    style.configure("Basic.TButton", font=BASIC_FONT)
    style.configure("Basic.TRadiobutton", font=BASIC_FONT)
