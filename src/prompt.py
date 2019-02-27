# Wishlist:
# regex matching
import textwrap


class BasePrompt():
    """A prompt with no builtin commands."""

    def __init__(self, pstr="> "):
        self.pstr = pstr
        self.commands = {}
        self.aliases = {}
        self.registerCommand("help", self.cmd_help, ["?"], "Print help")
        self.registerCommand("exit", self.cmd_exit, [
                             "quit"], "Exit the prompt")

    def registerCommand(self, name, callback, aliases=[], helpstr=None):
        self.registerCommandObj(Command(name, callback, aliases, helpstr))

    def registerCommandObj(self, command):
        name = command.name
        self.commands[name] = command
        for a in command.aliases:
            self.aliases[a] = self.commands[name]

    def registerCommandsFromNamespace(self, namespace, prefix):
        return self._registerCommandsFromNamespace(
            namespace,
            matches=(lambda name: name[0:len(prefix)] == prefix),
            mutilate=(lambda name: name[len(prefix):])
        )

    def _registerCommandsFromNamespace(self, namespace, matches=lambda a: True, mutilate=lambda a: a):
        for name in namespace:
            if matches(name) and hasattr(namespace.__getattribute__(name), '__call__'):
                func = namespace.__getattribute__(name)
                self.registerCommand(
                    mutilate(name),
                    func,
                    helpstr=textwrap.dedent(func.__doc__) if func.__doc__ else ""
                )

    def run(self):
        import shlex
        try:
            while True:
                inp = shlex.split(input(self.pstr))
                name = inp[0]
                match = self.commands.get(name) or self.aliases.get(name)
                if match:
                    # Run command, if a command matches
                    match(*inp[1:])
                else:
                    print("ERROR: No such command " + name)
        except (KeyboardInterrupt, EOFError) as e:
            # Catch Ctrl-C, Ctrl-D, and exit.
            print("User interrupt.")

    def __call__(self):
        return self.run()


class Prompt(BasePrompt):
    """docstring for Prompt"""

    def __init__(self, pstr="> "):
        super().__init__(pstr)
        self.registerCommandsFromNamespace(self, "cmd_")

    def cmd_exit(self, *args):
        raise KeyboardInterrupt

    def cmd_help(self, *args):

        if len(args) == 0:

            alen = max(len(k) for k in self.commands) + 2
            blen = max(len(k) for k in self.aliases) + 2

            def printRow(*row):
                print("{0:{alen}}{1:{blen}}{2:<48}".format(
                    *row,
                    alen=alen,
                    blen=blen
                ))

            printRow(
                "command",
                "alias",
                "help"
            )
            print(*["-"] * 32, sep="")
            for ck in self.commands:
                c = self.commands.get(ck)
                printRow(
                    c.name,
                    ",".join(a for a in c.aliases),
                    c.helpstr
                    # [line for line in c.helpstr.split("\n") if line != ""][0]
                )
        else:
            for query in args:
                ck = self.commands.get(query)
                if ck:
                    print("== {} ==".format(query))
                    print(ck.helpstr)
                else:
                    print("No such command: '{}'".format(query))


class Command(object):
    """docstring for Command"""

    def __init__(self, name, callback, aliases=[], helpstr=None):
        self.name = name
        self.callback = callback
        self.aliases = aliases
        if helpstr is None:
            helpstr = "Run command {name}".format(**locals())
        self.helpstr = helpstr

    def run(self, *args):
        return self.__call__(*args)

    def __call__(self, *args):
        try:
            self.callback(*args)
        except Exception as e:
            import traceback
            traceback.print_exc()


class Interactable():

    def __init__(self, prefix="cmd_", start=True):
        # super(Interactable, self).__init__()
        self.prefix = prefix
        if start:
            self.prompt()

    def prompt(self):
        p = Prompt()
        p.registerCommandsFromNamespace(self, self.prefix)
        p()


def test():
    def echo(*args):
        """
        A docstring with newlines and
        weird indentation and specs

        Returns:
            None
        """
        print(*args)

    p = Prompt()
    p.registerCommand("alongcommandname", echo, [], "Repeat input")
    p.registerCommand("echo", echo, ['print'], "Repeat input")
    p.registerCommandsFromFuncs([echo], lambda a: True, lambda a: a)

    p()


if __name__ == "__main__":
    test()
