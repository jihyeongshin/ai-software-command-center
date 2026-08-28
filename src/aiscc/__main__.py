from __future__ import annotations

import argparse

import uvicorn


def main() -> None:
    parser = argparse.ArgumentParser(prog="aiscc")
    subcommands = parser.add_subparsers(dest="command", required=True)
    serve = subcommands.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", default=8000, type=int)
    args = parser.parse_args()

    if args.command == "serve":
        uvicorn.run("aiscc.api.app:app", host=str(args.host), port=int(args.port))


if __name__ == "__main__":
    main()
