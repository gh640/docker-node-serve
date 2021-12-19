# docker-node-serve

A tiny script to use [`serve`](https://github.com/vercel/serve) with Docker.

## Prerequisites

- Docker
- Python 3

## Usage

```sh
python scripts.py build
```

```sh
python scripts.py run [directory_to_serve]
```

`directory_to_serve` should be a directory. Can be absolute or relative.

Example:

```sh
python scripts.py run ./public
```

## Reference

- [GitHub - vercel/serve: Static file serving and directory listing](https://github.com/vercel/serve)
