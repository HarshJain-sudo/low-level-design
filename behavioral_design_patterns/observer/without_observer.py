class WeatherStation:
    def __init__(self):
        self.temperature = 0
        self.mobile_display = None
        self.desktop_display = None

    def set_displays(self, mobile, desktop):
        self.mobile_display = mobile
        self.desktop_display = desktop

    def set_temperature(self, temp):
        print(f"Weather Station: Temperature updated to {temp}°C")
        self.temperature = temp
        if self.mobile_display:
            self.mobile_display.update(temp)
        if self.desktop_display:
            self.desktop_display.update(temp)


class MobileDisplay:
    @staticmethod
    def update(temperature):
        print(f"Mobile Display: Updated temperature = {temperature}°C")

class DesktopDisplay:
    @staticmethod
    def update(temperature):
        print(f"Desktop Display: Updated temperature = {temperature}°C")


# Client
station = WeatherStation()
station.set_displays(MobileDisplay(), DesktopDisplay())
station.set_temperature(30)

"""
If you add another display (like a WebDisplay), you must modify the WeatherStation class — violates the Open/Closed Principle.
The WeatherStation tightly depends on each display type.
Not scalable.
"""