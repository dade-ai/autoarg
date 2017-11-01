autoarg
=======

a simple tiny wrapper of argument parser
----------------------------------------

-  There are already pairs of optional keywords and default values and
   types in function signature, and docstring as a description. just use
   it!
-  no more verbose code for command line options :)

write sample.py
---------------

.. code:: python


    # sample.py

    def main(pos1, pos2, kw1=1, kw2=2):
        """
        dostring as a help string
        :param pos1:
        :param pos2:
        :param kw1:
        :param kw2:
        :return:
        """
        pass


    if __name__ == '__main__':
        import autoarg
        autoarg.run(main)

just run
--------

.. code:: sh

    $ python sample.py -h

    $ python sample.py --help
    usage: sample.py [-h] [--kw2 KW2] [--kw1 KW1] pos1 pos2

        dostring as a help string
        :param pos1:
        :param pos2:
        :param kw1:
        :param kw2:
        :return:


    positional arguments:
      pos1
      pos2

    optional arguments:
      -h, --help  show this help message and exit
      --kw2 KW2   kw2 : default = 2
      --kw1 KW1   kw1 : default = 1

if you need complex one, consider python-fire
