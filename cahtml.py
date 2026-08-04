"""
Convert raw Luna dataset records (schema above) into Qwen2.5-Coder's
ChatML training format.

Each raw record -> one final training string with real ChatML tags.
Output: a .jsonl file where each line is {"text": "<|im_start|>..."}
ready for SFT (e.g. with trl / axolotl).
"""

import json
import sys
from pathlib import Path

PLAN_OPEN, PLAN_CLOSE = "<plan>", "</plan>"
TOOLCALL_OPEN, TOOLCALL_CLOSE = "<tool_call>", "</tool_call>"
TOOLRESPONSE_OPEN, TOOLRESPONSE_CLOSE = "<tool_response>", "</tool_response>"


def render_assistant_content(msg: dict) -> str:
    parts = []

    plan = msg.get("plan")
    if plan:
        parts.append(f"{PLAN_OPEN}\n{plan.strip()}\n{PLAN_CLOSE}")

    for call in msg.get("tool_calls", []) or []:
        call_json = json.dumps(
            {"name": call["name"], "arguments": call["arguments"]},
            ensure_ascii=False,
        )
        parts.append(f"{TOOLCALL_OPEN}\n{call_json}\n{TOOLCALL_CLOSE}")

    content = (msg.get("content") or "").strip()
    if content:
        parts.append(content)

    return "\n".join(parts)


def render_record(record: dict) -> str:
    out = []

    system = record.get("system", "").strip()
    if system:
        out.append(f"<|im_start|>system\n{system}<|im_end|>")

    for msg in record["messages"]:
        role = msg["role"]

        if role == "user":
            out.append(f"<|im_start|>user\n{msg['content'].strip()}<|im_end|>")

        elif role == "assistant":
            body = render_assistant_content(msg)
            out.append(f"<|im_start|>assistant\n{body}<|im_end|>")

        elif role == "tool":
            body = f"{TOOLRESPONSE_OPEN}\n{msg['content'].strip()}\n{TOOLRESPONSE_CLOSE}"
            out.append(f"<|im_start|>user\n{body}<|im_end|>")

        else:
            raise ValueError(f"unknown role: {role}")

    return "\n".join(out)


def convert_file(in_path: str, out_path: str) -> None:
    in_file = Path(in_path)
    out_file = Path(out_path)

    records = [
        json.loads(line)
        for line in in_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    with out_file.open("w", encoding="utf-8") as f:
        for rec in records:
            text = render_record(rec)
            f.write(
                json.dumps({"text": text, "meta": rec.get("meta", {})}, ensure_ascii=False)
                + "\n"
            )

    print(f"Converted {len(records)} records -> {out_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python render_to_chatml.py <raw.jsonl> <out.jsonl>")
        sys.exit(1)
    convert_file(sys.argv[1], sys.argv[2])
