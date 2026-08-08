"""
PromptShield Request Schemas.

Pydantic models for incoming API requests.
Uses extra="allow" to pass through provider-specific parameters transparently.
"""

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single message in a chat completion request."""

    role: str
    content: str | list | None = None
    name: str | None = None
    tool_calls: list | None = None
    tool_call_id: str | None = None

    model_config = {"extra": "allow"}


class ChatCompletionRequest(BaseModel):
    """
    OpenAI-compatible chat completion request.

    Accepts all standard parameters and passes through unknown ones
    to the upstream provider.
    """

    model: str
    messages: list[ChatMessage]
    stream: bool = False

    # Optional standard parameters
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None
    stop: str | list[str] | None = None
    frequency_penalty: float | None = None
    presence_penalty: float | None = None
    n: int | None = None
    seed: int | None = None
    tools: list | None = None
    tool_choice: str | dict | None = None
    response_format: dict | None = None

    # PromptShield-specific (optional)
    ps_session_id: str | None = Field(None, description="Optional session ID for grouping requests")

    model_config = {"extra": "allow"}

    def to_upstream_body(self) -> dict:
        """
        Convert to a dict suitable for the upstream provider.

        Strips PromptShield-specific fields (ps_*).
        """
        data = self.model_dump(exclude_none=True)
        # Remove PromptShield-internal fields
        return {k: v for k, v in data.items() if not k.startswith("ps_")}
