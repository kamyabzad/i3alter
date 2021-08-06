#!/usr/bin/env python3
import asyncio
from keypress import KeyCapture

from i3ipc.aio import Connection
from i3ipc import Event


class I3Alter:
    def __init__(self):
        self.workspaces = []
        self.alt_workspaces = []
        self.alting = False
        self.i3 = None

    def on_workspace_focus(self, i3, e):
        ws = e.current.name
        if ws in self.workspaces:
            self.workspaces.remove(ws)
        self.workspaces = [ws, *self.workspaces]

    def on_workspace_empty(self, i3, e):
        ws = e.current.name
        if ws in self.workspaces:
            self.workspaces.remove(ws)

    async def switch_workspace(self, actions: int):
        if len(self.workspaces) == 1:
            return

        if abs(actions) == 1 and not self.alting:
            self.alting = True
            self.alt_workspaces = self.workspaces.copy()

        next_index = actions % len(self.alt_workspaces)
        next_ws = self.alt_workspaces[next_index]
        await self.i3.command(f"workspace {next_ws}")

    async def finish_switching(self, actions):
        if not actions:
            return

        self.alting = False
        self.workspaces = self.alt_workspaces.copy()
        next_ws_idx = actions % len(self.workspaces)
        next_ws = self.workspaces.pop(next_ws_idx)
        self.workspaces = [next_ws, *self.workspaces]


    async def main(self):
        self.i3 = await Connection().connect()

        ws_obj = await self.i3.get_workspaces()
        self.workspaces = [o.name for o in ws_obj]

        self.i3.on(Event.WORKSPACE_FOCUS, self.on_workspace_focus)
        self.i3.on(Event.WORKSPACE_EMPTY, self.on_workspace_empty)
        await self.i3.main()


async def main():
    i3alter = I3Alter()

    def switch_sync(offset: int):
        asyncio.run(i3alter.switch_workspace(offset))

    def finish_sync(actions):
        asyncio.run(i3alter.finish_switching(actions))

    keycapture = KeyCapture(switch_sync, finish_sync)
    i3task = asyncio.create_task(i3alter.main())

    keycapture.start_listening()

    await i3task


if __name__ == "__main__":
    i3alter = I3Alter()
    asyncio.run(main())
