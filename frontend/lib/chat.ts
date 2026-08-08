import { Message } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChatRequestOptions {
  model: string;
  messages: Message[];
  ps_session_id?: string;
  onChunk: (chunk: string) => void;
  onDone: () => void;
  onError: (error: string) => void;
  signal?: AbortSignal;
}

/**
 * Sends a chat request to the PromptShield backend and parses the SSE stream.
 */
export async function streamChatResponse(options: ChatRequestOptions) {
  const { model, messages, ps_session_id, onChunk, onDone, onError, signal } = options;

  try {
    const response = await fetch(`${API_BASE_URL}/v1/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model,
        messages,
        stream: true,
        ps_session_id,
      }),
      signal,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData?.error?.message || `Failed to fetch: ${response.status}`);
    }

    if (!response.body) {
      throw new Error("No response body returned.");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;
    let buffer = "";

    while (!done) {
      const { value, done: readerDone } = await reader.read();
      done = readerDone;

      if (value) {
        buffer += decoder.decode(value, { stream: true });
        
        // Process SSE lines
        const lines = buffer.split("\n");
        buffer = lines.pop() || ""; // Keep the incomplete line in the buffer
        
        for (const line of lines) {
          if (line.trim() === "") continue;
          if (line.startsWith("data: ")) {
            const data = line.slice(6).trim();
            if (data === "[DONE]") {
              onDone();
              return;
            }
            try {
              const parsed = JSON.parse(data);
              const delta = parsed.choices?.[0]?.delta?.content;
              if (delta) {
                onChunk(delta);
              }
            } catch (err) {
              console.warn("Failed to parse SSE chunk:", data, err);
            }
          }
        }
      }
    }
    onDone();
  } catch (error: any) {
    if (error.name === "AbortError") {
      console.log("Chat request aborted");
      onDone();
    } else {
      onError(error.message || "An unknown error occurred.");
    }
  }
}
