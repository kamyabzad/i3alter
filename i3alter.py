#!/usr/bin/env python3
import asyncio

from i3con import I3Con
from keycapture import KeyCapture

async def main():
    i3con = I3Con()

    def switch_sync(offset: int):
        asyncio.run(i3con.switch_workspace(offset))

    def finish_sync(actions):
        asyncio.run(i3con.finish_switching(actions))

    keycapture = KeyCapture(switch_sync, finish_sync)
    i3task = asyncio.create_task(i3con.main())

    keycapture.start_listening()

    await i3task


if __name__ == "__main__":
    asyncio.run(main())
