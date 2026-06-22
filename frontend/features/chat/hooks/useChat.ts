"use client";

import { useState } from "react";
import { ChatMessage } from "../types";
import { sendChatMessage } from "../services/api";

export function useChat(repositoryId: number) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionId, setSessionId] = useState<number | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (content: string) => {
    if (!content.trim()) return;
    
    // Optimistic UI updates
    const userMsg: ChatMessage = { role: "USER", content };
    setMessages((prev) => [...prev, userMsg]);
    
    try {
      setIsLoading(true);
      setError(null);
      
      const res = await sendChatMessage({
        repository_id: repositoryId,
        session_id: sessionId,
        message: content,
      });

      setSessionId(res.session_id);
      
      const assistantMsg: ChatMessage = {
        role: "ASSISTANT",
        content: res.response,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setError(err.message || "Failed to chat with codebase");
    } finally {
      setIsLoading(false);
    }
  };

  return {
    messages,
    isLoading,
    error,
    sendMessage,
  };
}
