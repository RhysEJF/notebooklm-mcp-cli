"""Pipeline tools — consolidated tool for multi-step notebook workflows."""

from typing import Any

from ...services import pipeline as pipeline_service
from ...services.errors import ServiceError
from ._utils import get_client, logged_tool


@logged_tool()
def pipeline(
    action: str,
    notebook_id: str | None = None,
    pipeline_name: str | None = None,
    input_url: str = "",
) -> dict[str, Any]:
    """Manage and execute multi-step notebook pipelines.

    Actions:
    - run: Execute a pipeline on a notebook
    - list: List all available pipelines (builtin and user-defined)

    Args:
        action: Operation to perform (run, list)
        notebook_id: Target notebook UUID (required for action=run)
        pipeline_name: Pipeline name (required for action=run, e.g. "ingest-and-podcast")
        input_url: URL variable for pipelines that need it (replaces $INPUT_URL)
    """
    try:
        if action == "run":
            if not notebook_id:
                return {"status": "error", "error": "notebook_id is required for action=run"}
            if not pipeline_name:
                return {"status": "error", "error": "pipeline_name is required for action=run"}
            client = get_client()
            variables = {}
            if input_url:
                variables["INPUT_URL"] = input_url
            result = pipeline_service.pipeline_run(client, notebook_id, pipeline_name, variables)
            return {"status": "success", **result}

        elif action == "list":
            pipelines = pipeline_service.pipeline_list()
            return {
                "status": "success",
                "pipelines": pipelines,
                "count": len(pipelines),
            }

        else:
            return {"status": "error", "error": f"Unknown action: {action}. Use: run, list"}

    except ServiceError as e:
        return {"status": "error", "error": e.user_message}
    except Exception as e:
        return {"status": "error", "error": str(e)}
