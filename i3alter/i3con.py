"""
Module for interacting with i3
"""
from i3ipc.aio import Connection
from i3ipc import Event


class I3Con:
    """
    Class for interacting with i3

    Properties:
      __workspaces (list):
        a list of workspaces ordered by last focused

      __workspaces_original (list):
        a copy of workspaces before switching starts

      __swtiching (bool):
        define whether or not we're in switching state
        when it's true, switching order is read from
        workspaces_preserved, not workspaces

      __i3 (i3ipc.aio.Connecton):
        i3 connection
    """

    def __init__(self):
        self.__workspaces = []
        self.__workspaces_preserved = []
        self.__switching = False
        self.__i3 = None

    def __on_workspace_focus(self, i3, e):
        """
        handle workspace focus event
        bring the workspace to the front of the self.__workspaces
        """
        ws = e.current.name
        if ws in self.__workspaces:
            self.__workspaces.remove(ws)
        self.__workspaces = [ws, *self.__workspaces]

    def __on_workspace_empty(self, i3, e):
        """
        handle workspace empty event
        delete workspace from self.__workspaces
        """
        ws = e.current.name
        if ws in self.__workspaces:
            self.__workspaces.remove(ws)

    async def switch_workspace(self, switch_count: int):
        """
        handle switching
        on first switch, set __switching and preserve the original state of workspaces
        find next workspace based on switch_count (read from preserved workspaces)
        """
        if len(self.__workspaces) == 1:
            return

        if abs(switch_count) == 1 and not self.__switching:
            self.__switching = True
            self.__workspaces_preserved = self.__workspaces.copy()

        next_index = switch_count % len(self.__workspaces_preserved)
        next_ws = self.__workspaces_preserved[next_index]
        await self.__i3.command(f"workspace {next_ws}")

    async def finish_switching(self, switch_count):
        """
        handle finish switching
        unset self.__switching, read .__workspaces from .__workspaces_preserved
        push new focused ws to the front of self.__workspaces
        """
        if not switch_count:
            return

        self.__switching = False
        self.__workspaces = self.__workspaces_preserved.copy()
        next_ws_idx = switch_count % len(self.__workspaces)
        next_ws = self.__workspaces.pop(next_ws_idx)
        self.__workspaces = [next_ws, *self.__workspaces]

    async def run(self):
        """
        run i3 connection and listen on focus/empty events
        """
        self.__i3 = await Connection().connect()

        ws_obj = await self.__i3.get_workspaces()
        self.__workspaces = [o.name for o in ws_obj]

        self.__i3.on(Event.WORKSPACE_FOCUS, self.__on_workspace_focus)
        self.__i3.on(Event.WORKSPACE_EMPTY, self.__on_workspace_empty)
        await self.__i3.main()
