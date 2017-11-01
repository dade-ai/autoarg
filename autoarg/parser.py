# -*- coding: utf-8 -*-
import argparse
import sys


def _str2bool(v):
    return v.lower() in ('yes', 'true', 't', '1')


def _str2eval(v):
    return eval(v)


class Parser(object):

    def __init__(self, **defaults_options):

        p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)

        p.register('type', 'bool', _str2bool)
        p.register('type', 'list', _str2eval)
        self._parser = p
        self.positional = []

        self.add_option_map(defaults_options)

    @property
    def description(self):
        return self._parser.description

    @description.setter
    def description(self, value):
        self._parser.description = value

    def add_option(self, arg, default, help='', **kwargs):
        h = help or arg.replace('_', ' ')
        atype, default = self._get_type_and_default(default)
        h += ' : default = {}'.format(default)
        self._parser.add_argument('--' + arg, type=atype, default=default, help=h, **kwargs)

    def add_option_map(self, optionmap):
        for opt in optionmap.iteritems():
            self.add_option(*opt)

    def add_positional_args(self, args):
        """
        add positional arguments
        :param args:
        :return:
        """
        # for i, a in enumerate(args):
        #     self._parser.add_argument(a, nargs=i+1)
        for a in args:
            self._parser.add_argument(a)

        self.positional = args

    def parse(self, argv=None, namespace=None, **kwargs):
        """
        parse argv and return args, kwargs
        :param list(str) argv:
        :param namespace:
        :return: args, kwargs
        """
        # parse
        parsed, unparsed = self._parser.parse_known_args(args=argv, namespace=namespace)
        parsed = parsed.__dict__

        # convert parsed value like as function arguments (args)
        args = [parsed[k] for k in self.positional]
        args += unparsed

        # convert parsed value like as function arguments (kwargs)
        # NameSpace object always has an 'options' attribute
        kw = {k for k in parsed if k not in self.positional}
        kwargs.update({k: parsed[k] for k in kw})

        return args, kwargs

    @staticmethod
    def _get_type_and_default(value):
        if value is None:
            return str, value
        elif isinstance(value, bool):
            return 'bool', value
        else:
            return type(value), value

    @classmethod
    def from_entry_point(cls, entry=None, **defaults):
        import inspect

        def get_doc(entry_):
            if inspect.isclass(entry_):
                docstring = entry_.__init__.__doc__
            else:
                docstring = entry_.__doc__
            return docstring

        def get_options_from_entry(entry_):
            a = inspect.getargspec(entry_)  # namedtuple(args, varargs, keywords, defaults)
            if a.defaults is None:
                options = dict()
                nargs = len(a.args)
            else:
                options = dict(zip(reversed(a.args), reversed(a.defaults)))
                nargs = len(a.args) - len(a.defaults)
            args = a.args[:nargs]  # type: list(str)

            return args, options

        # def main() is default entry point
        main = entry or _get_entry_point(main=entry)

        docstring = get_doc(main)
        args, options = get_options_from_entry(main)
        options.update(defaults)

        parser = cls(**options)  # type Parser
        parser.add_positional_args(args)

        # description ?
        parser.description = docstring

        return parser


def _get_entry_point(main=None):
    import sys as _sys
    main = main or _sys.modules['__main__'].main
    return main


def run(main=None, argv=None, **options):

    main = _get_entry_point(main)
    parser = Parser.from_entry_point(main, **options)

    args, kwargs = parser.parse(argv)

    sys.exit(main(*args, **kwargs))

