import { useMemo, useState } from "react";
import { Bot, SendHorizontal, X } from "lucide-react";
import { sendChatMessage } from "../api/client";
import type { ChatMessage } from "../types";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content: "Hi, I can answer questions about skills, projects, experience, and education."
    }
  ]);

  const canSend = useMemo(() => input.trim().length > 0 && !loading, [input, loading]);

  async function handleSend() {
    if (!canSend) return;
    const nextUserMessage: ChatMessage = { role: "user", content: input.trim() };
    const historyForBackend = [...messages];
    setMessages((prev) => [...prev, nextUserMessage]);
    setInput("");
    setLoading(true);
    try {
      const result = await sendChatMessage(nextUserMessage.content, historyForBackend);
      setMessages((prev) => [...prev, { role: "assistant", content: result.answer }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I could not process that. Please try again." }
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      {open && (
        <div className="fixed right-6 bottom-24 z-50 w-[360px] max-w-[calc(100vw-2rem)] overflow-hidden rounded-2xl border border-ink-200 bg-white shadow-glass dark:border-ink-500 dark:bg-ink-800">
          <div className="flex items-center justify-between border-b border-ink-200 px-4 py-3 dark:border-ink-600">
            <div className="flex items-center gap-2">
              <Bot size={18} className="text-accent-500" />
              <p className="text-sm font-semibold text-ink-800 dark:text-ink-100">AI Resume Assistant</p>
            </div>
            <button type="button" onClick={() => setOpen(false)} className="text-ink-500 hover:text-ink-800 dark:hover:text-white">
              <X size={16} />
            </button>
          </div>

          <div className="h-80 space-y-3 overflow-y-auto p-4">
            {messages.map((m, idx) => (
              <div
                key={`${m.role}-${idx}`}
                className={`max-w-[85%] rounded-xl px-3 py-2 text-sm ${
                  m.role === "user"
                    ? "ml-auto bg-accent-500 text-white"
                    : "bg-ink-100 text-ink-800 dark:bg-ink-700 dark:text-ink-100"
                }`}
              >
                {m.content}
              </div>
            ))}
          </div>

          <div className="border-t border-ink-200 p-3 dark:border-ink-600">
            <div className="flex items-center gap-2">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") void handleSend();
                }}
                placeholder="Ask about projects, skills..."
                className="w-full rounded-xl border border-ink-300 px-3 py-2 text-sm outline-none focus:border-accent-500 dark:border-ink-500 dark:bg-ink-900 dark:text-ink-100"
              />
              <button
                type="button"
                onClick={() => void handleSend()}
                disabled={!canSend}
                className="rounded-xl bg-accent-500 p-2 text-white disabled:cursor-not-allowed disabled:opacity-50"
              >
                <SendHorizontal size={16} />
              </button>
            </div>
          </div>
        </div>
      )}

      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        className="fixed right-6 bottom-6 z-50 inline-flex items-center gap-2 rounded-full bg-ink-900 px-5 py-3 text-sm font-semibold text-white shadow-glass transition hover:bg-ink-700 dark:bg-accent-500 dark:hover:bg-accent-600"
      >
        <Bot size={16} />
        Ask AI
      </button>
    </>
  );
}
