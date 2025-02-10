"""Command-Line Arguments Parsing."""

import sys

if __name__ == '__main__':
    import argparse

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description='demo')
    parser.add_argument('arg1', help='positional argument (str type)')
    parser.add_argument('arg2', help='positional argument (int type)', type=int)
    parser.add_argument(
        'arg3', help='argument with value choices', type=str, choices=('a', 'b')
    )
    parser.add_argument('--arg4', help='optional argument')
    parser.add_argument('-a5', '--arg5', help='optional argument (short options)')

    # nargs: multiple values
    parser.add_argument('--arg6', help='multiple values (any)', nargs='*')
    parser.add_argument(
        '--arg7',
        help='multiple values (one or zero)',
        nargs='?',
        const='b',
        default='a',
    )
    parser.add_argument('--arg8', help='multiple values (exact)', nargs=2)
    parser.add_argument('--arg9', help='multiple values (at least one)', nargs='+')

    if sys.version_info < (3, 9):
        parser.add_argument(
            '-q',
            '--quiet',
            help="don't show any message",
            action='store_true',
            default=False,
        )
    else:
        parser.add_argument(
            '-q',
            '--quiet',
            help="don't show any message",
            action=argparse.BooleanOptionalAction,  # New in Python 3.9
            default=False,
        )

    parser.add_argument(
        '--arg10', help='file', type=argparse.FileType('r', encoding='utf-8')
    )

    args = parser.parse_args()

    if args.arg4:
        print(args.arg4)
    if args.arg5:
        print(args.arg5)
    if args.quiet:
        print(args.quiet)
    assert isinstance(args.arg6, list)
    assert isinstance(args.arg7, list)
    assert isinstance(args.arg8, list)
    assert isinstance(args.arg9, list)
    assert len(args.arg7) in (0, 1)  # pyright: ignore
    assert len(args.arg8) == 2  # pyright: ignore
    assert len(args.arg9) > 1  # pyright: ignore
