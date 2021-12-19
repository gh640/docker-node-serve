"""Scripts to use Docker resources in this repo."""
import argparse
import asyncio
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / 'src'
IMAGE_NAME = 'node-serve'


async def main():
    args = get_args()

    handler = dispatcher(args.command)
    await handler(args)


def dispatcher(command: str):
    handlers = {
        'build': main_build,
        'run': main_run,
    }

    return handlers[command]


async def main_build(args):
    await docker(['build', '-t', IMAGE_NAME, str(SRC_DIR)])


async def main_run(args):
    root_dir = args.root_dir
    await docker(
        [
            'run',
            '--rm',
            '-it',
            '-v',
            f'{str(root_dir)}:/app/root:ro',
            '-p',
            '3000:3000',
            '--init',
            IMAGE_NAME,
        ]
    )


def get_args():
    parser = argparse.ArgumentParser(__doc__)
    subparsers = parser.add_subparsers(title='command', dest='command', required=True)

    subparsers.add_parser('build')

    parser_run = subparsers.add_parser('run')
    parser_run.add_argument('root_dir', type=path_type)

    return parser.parse_args()


def path_type(path_str: str) -> Path:
    path = Path(path_str).resolve()
    if not path.exists():
        raise ValueError()
    if not path.is_dir():
        raise ValueError()

    return path


async def docker(args: list[str]) -> None:
    await run('docker', args)


async def run(program: str, args: list[str]) -> None:
    proc = await asyncio.create_subprocess_exec(program, *args)
    try:
        await proc.communicate()
    except KeyboardInterrupt:
        await proc.kill()

    print(f'{program} {" ".join(args)} exited with {proc.returncode}')


if __name__ == '__main__':
    asyncio.run(main())
