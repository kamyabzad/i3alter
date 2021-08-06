#!/usr/bin/env python3
import asyncio

from i3con import I3Con
from keycapture import KeyCapture


async def main():
    i3con = I3Con()
    i3task = asyncio.create_task(i3con.run())

    def on_switch(switch_count: int):
        asyncio.run(i3con.switch_workspace(switch_count))

    def on_finish(switch_count):
        asyncio.run(i3con.finish_switching(switch_count))

    keycapture = KeyCapture(on_switch, on_finish)

    keycapture.start_listening()
    await i3task


if __name__ == "__main__":
    asyncio.run(main())
