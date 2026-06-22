"use client";

import React, { useState } from "react";
import { Settings, Cpu, HardDrive, Key } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function SettingsPage() {
  const [apiKey, setApiKey] = useState("••••••••••••••••••••");
  const [embeddingModel, setEmbeddingModel] = useState("models/embedding-001");
  const [llmModel, setLlmModel] = useState("gemini-1.5-pro");

  const handleSave = () => {
    alert("Settings saved successfully!");
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-zinc-800 pb-4">
        <h2 className="text-xl font-bold text-zinc-150">Configuration Settings</h2>
        <p className="text-xs text-zinc-400">Configure provider keys, database backends, and deployment preferences.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="border-zinc-850">
          <CardHeader>
            <CardTitle className="text-sm flex items-center gap-2">
              <Key className="h-4 w-4 text-yellow-500" />
              API Settings
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-xs font-semibold text-zinc-400 mb-1.5 block">Google Gemini API Key</label>
              <Input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
              />
            </div>
            <Button onClick={handleSave} size="sm">
              Save Credentials
            </Button>
          </CardContent>
        </Card>

        <Card className="border-zinc-850">
          <CardHeader>
            <CardTitle className="text-sm flex items-center gap-2">
              <Cpu className="h-4 w-4 text-blue-500" />
              Model Configuration
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-xs font-semibold text-zinc-400 mb-1.5 block">Embedding Model</label>
              <select
                value={embeddingModel}
                onChange={(e) => setEmbeddingModel(e.target.value)}
                className="w-full bg-zinc-900 border border-zinc-700 rounded-md px-3 py-2 text-sm text-zinc-200"
              >
                <option value="models/embedding-001">models/embedding-001 (Google Gemini)</option>
                <option value="all-MiniLM-L6-v2">all-MiniLM-L6-v2 (Local Sentence Transformers)</option>
              </select>
            </div>
            <div>
              <label className="text-xs font-semibold text-zinc-400 mb-1.5 block">Chat Model</label>
              <select
                value={llmModel}
                onChange={(e) => setLlmModel(e.target.value)}
                className="w-full bg-zinc-900 border border-zinc-700 rounded-md px-3 py-2 text-sm text-zinc-200"
              >
                <option value="gemini-1.5-pro">gemini-1.5-pro (Recommended)</option>
                <option value="gemini-1.5-flash">gemini-1.5-flash (Faster)</option>
              </select>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
