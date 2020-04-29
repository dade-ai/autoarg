import autoarg

def test_parser1():

    def entry1(pos1, pos2):
        pass

    p = autoarg.Parser.from_entry_point(entry1)

    argv = 'parse 1 2'.split()[1:]
    args, kwargs = p.parse(argv)
    assert args == ('1', '2')


def test_parser2():

    def entry1(pos1, pos2, kw1=1, kw2=3):
        pass

    p = autoarg.Parser.from_entry_point(entry1)

    argv = 'parse 1 2 --kw1 3 --kw2 4'.split()[1:]
    args, kwargs = p.parse(argv)
    assert args == ('1', '2')
    assert kwargs == {'kw1': 3, 'kw2': 4}


def main(pos1, pos2, kw1=1, kw2=2):
    print('args: ', autoarg.parsed.args)
    print('kwargs: ', autoarg.parsed.kwargs)


@autoarg.entry_point
def main_auto(pos1, pos2, kw1=1, kw2=2):
    print(pos1, pos2, kw1, kw2)
    print('args: ', autoarg.parsed.args)
    print('kwargs: ', autoarg.parsed.kwargs)


if __name__ == '__main__':
    main_auto()
    # arg.run(main)
