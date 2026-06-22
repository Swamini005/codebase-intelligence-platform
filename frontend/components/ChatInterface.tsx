import React, { useState, useRef, useEffect } from "react";
import { Send, Terminal, Cpu, User, Loader2 } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { ScrollArea } from "./ui/scroll-area";

interface Message {
  role: "USER" | "ASSISTANT" | "SYSTEM";
  content: string;
}

interface ChatInterfaceProps {
  messages: Message[];
  isLoading: boolean;
  onSendMessage: (msg: string) => void;
}

export function ChatInterface({ messages, isLoading, onSendMessage }: ChatInterfaceProps) {
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input);
      setInput("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  return (
    <Card className="flex flex-col h-[600px] border-zinc-800 bg-zinc-950/40">
      <CardHeader className="border-b border-zinc-800 py-3 flex flex-row items-center justify-between">
        <CardTitle className="text-sm font-bold flex items-center gap-2">
          <Cpu className="h-4 w-4 text-purple-400" />
          RAG Chat Assistant
        </CardTitle>
        <span className="text-xs text-zinc-500 font-mono">Gemini-1.5-Pro</span>
      </CardHeader>
      
      <ScrollArea className="flex-1 p-4 space-y-4" ref={scrollRef}>
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center p-8 text-zinc-500 space-y-2 mt-20">
            <Cpu className="h-10 w-10 text-zinc-700 animate-pulse" />
            <p className="text-sm font-medium">Ask questions about functions, classes, or architecture.</p>
            <p className="text-xs max-w-sm">The platform will retrieve matching code context to ground answers.</p>
          </div>
        )}
        
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex gap-3 max-w-[85%] rounded-lg p-3 ${
              msg.role === "USER"
                ? "bg-zinc-800/80 text-zinc-150 ml-auto border border-zinc-750"
                : "bg-blue-950/20 border border-blue-900/30 text-zinc-150 mr-auto"
            }`}
          >
            <div className="mt-0.5">
              {msg.role === "USER" ? (
                <User className="h-4 w-4 text-blue-400" />
              ) : (
                <Cpu className="h-4 w-4 text-purple-400" />
              )}
            </div>
            <div className="text-sm leading-relaxed whitespace-pre-wrap font-sans">
              {msg.content}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex gap-3 max-w-[80%] bg-blue-950/20 border border-blue-900/30 rounded-lg p-3 text-zinc-400 mr-auto">
            <Cpu className="h-4 w-4 text-purple-400" />
            <div className="flex items-center gap-2 text-sm">
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
              <span>Analyzing code context...</span>
            </div>
          </div>
        )}
      </ScrollArea>

      <div className="p-3 border-t border-zinc-800 flex gap-2">
        <Input
          placeholder="Ask a question about the repository..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        <Button onClick={handleSend} disabled={isLoading || !input.trim()}>
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </Card>
  );
}
