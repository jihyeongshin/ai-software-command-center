from __future__ import annotations

import argparse
import asyncio
import json
import os

import uvicorn


def main() -> None:
    parser = argparse.ArgumentParser(prog="aiscc")
    subcommands = parser.add_subparsers(dest="command", required=True)
    serve = subcommands.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", default=8000, type=int)
    ingress = subcommands.add_parser("serve-public-live")
    ingress.add_argument("--host", default="127.0.0.1")
    ingress.add_argument("--port", default=8001, type=int)
    worker = subcommands.add_parser("public-live-worker")
    worker.add_argument("--check", action="store_true")
    subcommands.add_parser("public-live-luna-canary")
    initializer = subcommands.add_parser("public-live-initializer")
    initializer.add_argument("--check", action="store_true")
    proof = subcommands.add_parser("hosted-l5-proof")
    proof.add_argument("--check", action="store_true")
    proof.add_argument(
        "--fault",
        required=True,
        choices=(
            "before-dispatch",
            "after-dispatch",
            "known-closed-failure",
            "sandbox-termination",
        ),
    )
    args = parser.parse_args()

    if args.command == "serve":
        uvicorn.run("aiscc.api.app:app", host=str(args.host), port=int(args.port))
    elif args.command == "serve-public-live":
        uvicorn.run(
            "aiscc.public_live.ingress:create_app",
            factory=True,
            host=str(args.host),
            port=int(args.port),
            proxy_headers=False,
        )
    elif args.command == "public-live-worker":
        from aiscc.public_live.worker import create_worker

        value = create_worker()
        try:
            value.check()
            if not args.check:
                asyncio.run(value.run(asyncio.Event()))
        finally:
            asyncio.run(value.close())
    elif args.command == "public-live-luna-canary":
        from aiscc.public_live.real_luna_canary import blocked_result, run_real_luna_canary

        try:
            result = run_real_luna_canary()
        except BaseException as error:
            result = blocked_result(error)
        print(json.dumps(dict(result), sort_keys=True, separators=(",", ":")))
    elif args.command == "public-live-initializer":
        from aiscc.public_live.initializer import create_initializer

        value = create_initializer()
        try:
            value.check_configuration()
            if not args.check:
                value.check()
                asyncio.run(value.run(asyncio.Event()))
        finally:
            asyncio.run(value.close())
    elif args.command == "hosted-l5-proof":
        from aiscc.public_live.hosted_proof import (
            FaultPoint,
            HostedProofSettings,
            run_operator_proof,
        )

        HostedProofSettings.from_environment(os.environ)
        if not args.check:
            result = asyncio.run(run_operator_proof(os.environ, FaultPoint(args.fault)))
            observation = result.observation
            print(
                f"run={result.run_id} fault={observation.fault_point.value} "
                f"phase={observation.durable_phase} outcome={observation.outcome} "
                f"receipts={observation.provider_receipts} "
                f"retry={str(observation.retry_allowed).lower()} "
                f"quarantine={str(observation.quarantine_required).lower()}"
            )


if __name__ == "__main__":
    main()
