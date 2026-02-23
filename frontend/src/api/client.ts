import type { ChatMessage, PortfolioData } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

export async function getPortfolioData(): Promise<PortfolioData> {
  const response = await fetch(`${API_BASE_URL}/portfolio`);
  if (!response.ok) {
    throw new Error("Failed to fetch portfolio data.");
  }
  return response.json();
}

export async function sendChatMessage(
  message: string,
  history: ChatMessage[]
): Promise<{ answer: string }> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history })
  });
  if (!response.ok) {
    throw new Error("Chat request failed.");
  }
  return response.json();
}

