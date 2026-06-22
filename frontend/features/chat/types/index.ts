export interface ChatMessage {
  id?: number;
  role: "USER" | "ASSISTANT" | "SYSTEM";
  content: string;
  created_at?: string;
}

export interface ChatSession {
  id: number;
  repository_id: number;
  messages: ChatMessage[];
}

export interface ChatRequest {
  repository_id: number;
  session_id?: number;
  message: string;
}

export interface ChatResponse {
  session_id: number;
  response: string;
  sources: string[];
}
