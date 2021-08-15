#!/usr/bin/env python3
import asyncio

from i3alter.i3con import I3Con
from i3alter.keycapture import KeyCapture


async def main_async():
    i3con = I3Con()
    i3task = asyncio.create_task(i3con.run())

    def on_switch(switch_count: int):
        asyncio.run(i3con.switch_workspace(switch_count))

    def on_finish(switch_count):
        asyncio.run(i3con.finish_switching(switch_count))

    keycapture = KeyCapture(on_switch, on_finish)

    keycapture.start_listening()
    await i3task

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
