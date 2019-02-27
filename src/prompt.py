"""Interactive user prompts as an interface.
"""
# Wishlist:
# regex matching
import textwrap

def _yes(*args):
    return True

def _echo(s):
    return s

def isCallable(f):
    return hasattr(f, '__call__')

class BasePrompt():
    """A prompt with no builtin commands.
    
    Attributes:
        aliases (dict): alias (str): command (Command)
        commands (dict): name (str): command (Command)
        pstr (str): The prompt string (i.e. '$ ')
    """

    def __init__(self, pstr="> "):
        """Initialize a runnable prompt
        
        Args:
            pstr (str) Override the prompt string (i.e. '$ ')
        """
        self.pstr = pstr
        self.commands = {}
        self.aliases = {}
        self.registerCommandsFromNamespace(self, "cmd_")
        # self.registerCommand("help", self.cmd_help, ["?"], "Print help")
        # self.registerCommand("exit", self.cmd_exit, [
        #                      "quit"], "Exit the prompt")

    def registerCommand(self, name, callback, aliases=[], helpstr=None):
        """Register a command.
        This just wraps the creation of a Command object and registers it.
        
        Args:
            name (string): The name of the function, and the command the users types.
            callback (func):
                The callback function that running this command triggers. 
                Should have signature func(*args)
            aliases (list, optional): List of alias strings
            helpstr (None, optional): 
                Multiline string of help information.
                The first line is automatically used as the short help string.
        """
        self.registerCommandObj(Command(name, callback, aliases, helpstr))

    def registerCommandObj(self, command):
        """Add a command object directly.
        
        Args:
            command (Command)
        """
        name = command.name
        self.commands[name] = command
        for a in command.aliases:
            self.aliases[a] = self.commands[name]

    def registerCommandsFromNamespace(self, namespace, prefix="cmd_"):
        """Searches a namespace for callables with a name
        that matches the pattern "cmd_xxxx" and registers them
        with the name "xxxx" and the function's docstring.
        
        Args:
            namespace
            prefix (str, optional): A substitution for the "cmd_" prefix
        """
        self.registerCommandsFromFuncs(
            [namespace.__getattribute__(name) for name in dir(namespace)],
            matches=(lambda func: func.__name__[0:len(prefix)] == prefix),
            mutilate=(lambda name: name[len(prefix):])
        )

    def registerCommandsFromFuncs(self, funcs, matches=_yes, mutilate=_echo):
        """Registers each callable in funcs that matches the function `matches`.
        Names them based on multilate.
        See registerCommandsFromNamespace.
        
        Args:
            funcs (list): List containing callables. Can contain non-callables.
            matches (func): Should return True when function is good.
            mutilate (func): How to alter the function's name.
        """
        for f in funcs:
            if isCallable(f) and matches(f):
                self.registerCommandFromFunc(f, mutilate)

    def registerCommandFromFunc(self, func, mutilate=_echo):
        """Summary
        
        Args:
            func (TYPE): Description
            mutilate (TYPE, optional): Description
        """
        self.registerCommand(
            mutilate(func.__name__),
            func,
            helpstr=textwrap.dedent(func.__doc__) if func.__doc__ else func.__name__
        )

    def run(self):
        """Summary
        """
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
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self.run()


class Prompt(BasePrompt):
    """docstring for Prompt
    """

    def __init__(self, pstr="> "):
        """Summary
        
        Args:
            pstr (str, optional): Description
        """
        super().__init__(pstr)
        self.registerCommandsFromNamespace(self, "cmd_")

    def cmd_exit(self, *args):
        """Exit the prompt.
        Same as Ctrl+C.
        
        Args:
            *args: Description
        
        Raises:
            KeyboardInterrupt: Description
        """
        raise KeyboardInterrupt

    def cmd_help(self, *args):
        """Get information about commands (try "help help")
        
        Usage:
            Run with no arguments to get a list
            of all availible commands.
        
            Run with arguments to get detailed
            help about commands.
        
        Args:
            *args: Description
        """

        if len(args) == 0:

            alen = max(len(k) for k in self.commands) + 2
            blen = max(len(k) for k in self.aliases) + 2

            def printRow(*row):
                """Summary
                
                Args:
                    *row: Description
                """
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
                printRow(*c.helprow)
        else:
            for query in args:
                ck = self.commands.get(query)
                if ck:
                    print(ck.helpdoc)
                else:
                    print("No such command: '{}'".format(query))


class Command(object):
    """Summary
    
    Args:
        name (string): The name of the function, and the command the users types.
        callback (func):
            The callback function that running this command triggers. 
            Should have signature func(*args)
        aliases (list, optional): List of alias strings
        helpstr (None, optional): 
            Multiline string of help information.
            The first line is automatically used as the short help string.
    """

    def __init__(self, name, callback, aliases=[], helpstr=None):
        self.name = name
        self.callback = callback
        self.aliases = aliases
        if helpstr is None:
            helpstr = "Run command {name}".format(**locals())
        self.helpstr = [line for line in helpstr.split("\n") if line != ""][0]
        self.helpdoc = "== " + self.name + " ==\n" + helpstr

    def run(self, *args):
        """Summary
        
        Args:
            *args: Description
        
        Returns:
            TYPE: Description
        """
        return self.__call__(*args)

    @property
    def helprow(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return (
            self.name,
            ",".join(a for a in self.aliases),
            self.helpstr
        )

    def __call__(self, *args):
        """Summary
        
        Args:
            *args: Description
        """
        try:
            self.callback(*args)
        except Exception as e:
            import traceback
            traceback.print_exc()


class Interactable():

    """Summary
    
    Attributes:
        prefix (TYPE): Description
    """
    
    def __init__(self, prefix="cmd_", start=True):
        """Summary
        
        Args:
            prefix (str, optional): Description
            start (bool, optional): Description
        """
        # super(Interactable, self).__init__()
        self.prefix = prefix
        if start:
            self.prompt()

    def prompt(self):
        """Summary
        """
        p = Prompt()
        p.registerCommandsFromNamespace(self, self.prefix)
        p()


def test():
    """Summary
    """
    def echo(*args):
        """
        A docstring with newlines and
        weird indentation and specs
        
        Args:
            *args: Description
        
        No Longer Returned:
            None
        """
        print(*args)

    p = Prompt()
    p.registerCommand("alongcommandname", echo, [], "Repeat input")
    p.registerCommand("echo", echo, ['print'], "Repeat input")
    p.registerCommandsFromFuncs([echo])

    p()


if __name__ == "__main__":
    test()
