import pyautogui as pya
from automations.software_base import SoftwareBase
import pywinctl as pwctl # Some pyautogui functions are unavailabel on linux systems
from time import sleep

class Machine:
    def __init__(self, screenshots_directory: str) -> None:
        self.screenshots_directory = screenshots_directory
    
    def open_software(self, software: SoftwareBase):
        """Opens the given software and verifies it is open"""
        pya.press("win")
        pya.locateOnScreen(f"{self.screenshots_directory}/window_selector_search_bar.png", 5)
        pya.write(software.software_name)

        try:
            pya.locateOnScreen(f"{software.scr_directories['base']}/window_selector_selected.png", 5)
        except pya.ImageNotFoundException:
            pya.locateOnScreen(f"{software.scr_directories['base']}/window_selector_selected_already_open.png", 5)

        pya.press("enter")

        try:
            pya.locateOnScreen(f"{software.scr_directories['base']}/open_empty.png", 5)
        except pya.ImageNotFoundException:
            print("Did not find full screen application. Making it into one!")
            pya.hotkey("win", "up")
            pya.locateOnScreen(f"{software.scr_directories['base']}/open_empty.png", 10, confidence=0.9)

    def close_software(self, software: SoftwareBase):
        software.close_application()

        # Make sure the application is closed by checking for title name
        # Needs to sleep for a moment before checking. Sometimes "Xlib.error.BadWindow:" occurs if immediately checked
        sleep(1)
        titles = pwctl.getAllTitles()
        if any([title == software.software_name for title in titles]):
            raise RuntimeError(f"{software.software_name} is still runnning")


