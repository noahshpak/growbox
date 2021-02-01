import asyncio
from typing import List, Dict
from kasa import Discover, SmartStrip, SmartDeviceException


def safe(f):
    def wrapper(*arg, **kwargs):
        try:
            f(*arg, **kwargs)
            return True
        except SmartDeviceException as e:
            print(f"Error {e}")
            return False

    return wrapper


class PowerstripController:
    """Simplify asyncio control of powerstrip"""

    def __init__(self):
        self._found_devices: List[SmartStrip] = asyncio.run(self.discover_smart_strips())
        self.plug_mapping: Dict[str, SmartStrip] = {c.alias: c for plug in self._found_devices for c in plug.children}

    async def discover_smart_strips(self):
        devices_on_network = await Discover.discover()
        smart_strips = [d for d in devices_on_network.values() if isinstance(d, SmartStrip)]
        print(f"Found {len(smart_strips)} smart strips")
        return smart_strips

    @safe
    def turn_off(self, alias: str):
        return asyncio.run(self.plug_mapping[alias].turn_off())

    @safe
    def turn_on(self, alias: str):
        return asyncio.run(self.plug_mapping[alias].turn_on())


if __name__ == "__main__":
    import time

    c = PowerstripController()
    ALIASES = {"A", "B", "C", "B-1", "B-2", "B-3", "B-4", "B-5", "B-6"}
    for a in ALIASES:
        c.turn_on(a)
    time.sleep(3)
    for a in ALIASES:
        c.turn_off(a)
    time.sleep(3)
    for a in ALIASES:
        c.turn_on(a)
