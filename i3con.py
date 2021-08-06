from i3ipc.aio import Connection
from i3ipc import Event


class I3Con:
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