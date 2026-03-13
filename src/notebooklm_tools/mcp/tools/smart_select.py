"""Smart select tools — consolidated tag management and notebook selection."""

from typing import Any

from ...services import smart_select as smart_select_service
from ...services.errors import ServiceError
from ._utils import logged_tool


@logged_tool()
def tag(
    action: str,
    notebook_id: str | None = None,
    tags: str | None = None,
    notebook_title: str = "",
    query: str | None = None,
) -> dict[str, Any]:
    """Manage notebook tags and find relevant notebooks by tag matching.

    Actions:
    - add: Add tags to a notebook for smart selection
    - remove: Remove tags from a notebook
    - list: List all tagged notebooks with their tags
    - select: Find notebooks relevant to a query using tag matching

    Args:
        action: Operation to perform (add, remove, list, select)
        notebook_id: Notebook UUID (required for add, remove)
        tags: Comma-separated tags (required for add, remove; e.g. "ai,research,llm")
        notebook_title: Optional display title (for add)
        query: Search query (required for select; e.g. "ai mcp" or "ai,mcp")
    """
    try:
        if action == "add":
            if not notebook_id:
                return {"status": "error", "error": "notebook_id is required for action=add"}
            if not tags:
                return {"status": "error", "error": "tags parameter is required for action=add"}
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            result = smart_select_service.tag_add(notebook_id, tag_list, notebook_title)
            return {"status": "success", "notebook_id": notebook_id, "tags": result["tags"]}

        elif action == "remove":
            if not notebook_id:
                return {"status": "error", "error": "notebook_id is required for action=remove"}
            if not tags:
                return {"status": "error", "error": "tags parameter is required for action=remove"}
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            result = smart_select_service.tag_remove(notebook_id, tag_list)
            return {"status": "success", "notebook_id": notebook_id, "tags": result["tags"]}

        elif action == "list":
            result = smart_select_service.tag_list()
            return {"status": "success", **result}

        elif action == "select":
            if not query:
                return {"status": "error", "error": "query parameter is required for action=select"}
            result = smart_select_service.smart_select(query)
            return {"status": "success", **result}

        else:
            return {"status": "error", "error": f"Unknown action: {action}. Use: add, remove, list, select"}

    except ServiceError as e:
        return {"status": "error", "error": e.user_message}
    except Exception as e:
        return {"status": "error", "error": str(e)}
