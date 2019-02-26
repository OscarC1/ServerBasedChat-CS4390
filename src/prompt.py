class Prompt(object):
    """docstring for Prompt"""

    def __init__(self, pstr="> "):
        self.pstr = pstr
        self.commands = {}
        self.aliases = {}
        self.registerCommand("help", self.cmd_help, ["?"], "Print help")
        self.registerCommand("exit", self.cmd_exit, [
                             "quit"], "Exit the prompt")

    def cmd_exit(self, *args):
        raise KeyboardInterrupt

    def cmd_help(self, *args):
        for ck in self.commands:
            c = self.commands.get(ck)
            print(c.name, c.aliases, c.helpstr, sep="\t")

    def registerCommand(self, name, callback, aliases=[], helpstr=None):
        self.registerCommandObj(Command(name, callback, aliases, helpstr))

    def registerCommandObj(self, command):
        name = command.name
        self.commands[name] = command
        for a in command.aliases:
            self.aliases[a] = self.commands[name]

    def run(self):
        try:
            while True:
                inp = input(self.pstr).split(" ")
                name = inp[0]
                match = self.commands.get(name) or self.aliases.get(name)
                if match:
                    match(*inp[1:])
                else:
                    print("ERROR: No such command " + name)
        except KeyboardInterrupt as e:
            print()

    def __call__(self):
        return self.run()


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


def test():
    def echo(*args):
        print(*args)

    p = Prompt()
    p.registerCommand("echo", echo, ['print'], "Repeat input")

    p()


class Interactable():

    def loadAutoprompt(self):
        p = Prompt()
        for name in dir(self):
            if name[0:len(self.prefix)] == self.prefix and hasattr(self.__getattribute__(name), '__call__'):
                p.registerCommand(
                    name[len(self.prefix):],
                    self.__getattribute__(name),
                    helpstr=self.__getattribute__(name).__doc__
                )
        return p

    def prompt(self):
        p = self.loadAutoprompt()
        p()

    def __init__(self, prefix="cmd_", start=True):
        # super(Interactable, self).__init__()
        self.prefix = prefix
        if start:
            self.prompt()


if __name__ == "__main__":
    test()
