"""Replay evaluation traces against a running /chat endpoint."""

import argparse
import json
from pathlib import Path

import httpx


def replay_trace(client: httpx.Client, endpoint: str, trace_path: Path) -> dict:
    payload = json.loads(trace_path.read_text(encoding="utf-8"))
    response = client.post(endpoint, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", default="http://127.0.0.1:8000/chat")
    parser.add_argument("--traces", default="data/traces")
    args = parser.parse_args()

    trace_dir = Path(args.traces)
    trace_paths = sorted(trace_dir.glob("*.json"))
    if not trace_paths:
        raise FileNotFoundError(f"No trace JSON files found in {trace_dir}")

    with httpx.Client() as client:
        for trace_path in trace_paths:
            result = replay_trace(client, args.endpoint, trace_path)
            print(
                json.dumps(
                    {
                        "trace": trace_path.name,
                        "has_reply": bool(result.get("reply")),
                        "end_of_conversation": result.get("end_of_conversation"),
                        "recommendation_count": len(result.get("recommendations", [])),
                    },
                    indent=2,
                )
            )


if __name__ == "__main__":
    main()
