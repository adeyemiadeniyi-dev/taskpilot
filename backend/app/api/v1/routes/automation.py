import httpx
from fastapi import APIRouter, HTTPException
from app.config import settings

router = APIRouter(prefix="/automation", tags=["Automation"])

KESTRA_BASE_URL = settings.kestra_base_url.rstrip("/")
KESTRA_UI_URL = (settings.kestra_ui_url or KESTRA_BASE_URL).rstrip("/")
KESTRA_TENANT = settings.kestra_tenant
KESTRA_NAMESPACE = settings.kestra_namespace
KESTRA_FLOW_ID = settings.kestra_flow_id
KESTRA_USERNAME = settings.kestra_username
KESTRA_PASSWORD = settings.kestra_password
HTTPX_TIMEOUT = 20


@router.post("/daily-review")
async def trigger_daily_review() -> dict:
    """
    Trigger Kestra 'daily-review' flow.

    Returns:
        dict: {
            "message": str,
            "execution_id": str,
            "kestra_url": str
        }
    """
    # Validate credentials
    if not all([KESTRA_USERNAME, KESTRA_PASSWORD]):
        raise HTTPException(status_code=500, detail="Kestra credentials not configured")

    url = f"{KESTRA_BASE_URL}/api/v1/{KESTRA_TENANT}/executions/{KESTRA_NAMESPACE}/{KESTRA_FLOW_ID}"

    multipart_fields = {
        "goal": (None, "Daily review"),
        "source": (None, "backend"),
        "reason": (None, "daily-review"),
    }

    try:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            resp = await client.post(
                url,
                auth=(KESTRA_USERNAME, KESTRA_PASSWORD),
                files=multipart_fields,
            )
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502,
            detail=f"Kestra call failed (status={resp.status_code})",
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Error connecting to Kestra: {e}")
    except ValueError:
        raise HTTPException(status_code=502, detail="Kestra returned a non-JSON response")

    execution_id = data.get("id")
    if not execution_id:
        raise HTTPException(status_code=502, detail="Kestra returned no execution id")

    return {
        "message": "Kestra daily-review flow triggered",
        "execution_id": execution_id,
        "kestra_url": f"{KESTRA_UI_URL}/ui/execution/{KESTRA_NAMESPACE}/{KESTRA_FLOW_ID}/{execution_id}",
    }