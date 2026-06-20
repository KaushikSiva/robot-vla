from __future__ import annotations

import json
import os
from typing import Any

from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field

from isaac_ext.pathvla_unitree import __version__
from pathvla.plan_validator import validate_plan_dict
from pathvla.schemas import HealthResponseModel, PlanResponseModel, SceneSnapshotModel, VLARequestModel


class InferResponseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subgoals: list[dict[str, Any]] = Field(min_length=1)


PLAN_JSON_SCHEMA: dict[str, Any] = {
    "name": "pathvla_plan",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "subgoals": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["navigate", "inspect", "pickup", "drop", "return_home"],
                        },
                        "target": {"type": "string"},
                        "constraints": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "avoid": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "safe_distance_m": {"type": "number"},
                            },
                            "required": ["avoid", "safe_distance_m"],
                        },
                    },
                    "required": ["type", "target", "constraints"],
                },
            }
        },
        "required": ["subgoals"],
    },
}


SYSTEM_PROMPT = """You are a robotics task planner.
Return only a valid JSON plan following the provided schema.
Use only object names that appear in the scene.
Do not invent targets, objects, or actions.
Prefer short subgoal sequences grounded in the instruction and scene.
If the instruction implies returning home, use target `home_marker`.
For avoidance, include named objects in constraints.avoid.
Use safe_distance_m between 0.4 and 1.0 depending on clutter.
"""

app = FastAPI(title="PathVLA VLA Server", version=__version__)


def _require_openai_client() -> OpenAI:
    base_url = os.getenv("VLA_LLM_BASE_URL")
    api_key = os.getenv("VLA_LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if base_url:
        # OpenAI-compatible local/server backends such as Gemma served via vLLM can run without auth.
        return OpenAI(base_url=base_url, api_key=api_key or "local-no-auth")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Set VLA_LLM_BASE_URL for a local OpenAI-compatible server or OPENAI_API_KEY for OpenAI cloud.",
        )
    return OpenAI(api_key=api_key)


def _resolve_model_name(payload: VLARequestModel) -> str:
    model_name = (
        payload.model_name
        or os.getenv("VLA_LLM_MODEL")
        or os.getenv("OPENAI_MODEL")
        or os.getenv("VLA_MODEL_NAME")
    )
    if not model_name:
        raise HTTPException(status_code=500, detail="Set VLA_LLM_MODEL or include model_name in the request.")
    return model_name


def _build_user_prompt(payload: VLARequestModel) -> str:
    scene_summary = {
        "scene_name": payload.scene.scene_name,
        "bounds": payload.scene.bounds,
        "robot": payload.scene.robot.model_dump(mode="json"),
        "objects": [obj.model_dump(mode="json") for obj in payload.scene.objects],
    }
    return (
        "Instruction:\n"
        f"{payload.instruction}\n\n"
        "Scene JSON:\n"
        f"{json.dumps(scene_summary, indent=2)}\n"
    )


def _extract_response_text(response) -> str:
    output_text = getattr(response, "output_text", "")
    if output_text:
        return output_text
    try:
        return json.dumps(response.output[0].content[0].json)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Could not extract structured model output: {exc}") from exc


@app.get("/health", response_model=HealthResponseModel)
def health():
    return HealthResponseModel(ok=True, service="pathvla-vla-server", version=__version__)


@app.post("/infer", response_model=PlanResponseModel)
def infer(request: VLARequestModel):
    payload = VLARequestModel(
        instruction=request.instruction,
        scene=SceneSnapshotModel.model_validate(request.scene.model_dump(mode="json")),
        model_name=request.model_name,
    )
    client = _require_openai_client()
    model_name = _resolve_model_name(payload)
    try:
        response = client.responses.create(
            model=model_name,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": _build_user_prompt(payload)},
            ],
            text={"format": {"type": "json_schema", "name": PLAN_JSON_SCHEMA["name"], "strict": True, "schema": PLAN_JSON_SCHEMA["schema"]}},
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"OpenAI request failed: {exc}") from exc

    parsed = validate_plan_dict(json.loads(_extract_response_text(response)))
    return parsed
