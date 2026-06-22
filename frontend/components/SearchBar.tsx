import React from "react";
import { Search, Loader2 } from "lucide-react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";

interface SearchBarProps {
  value: string;
  onChange: (val: string) => void;
  onSearch: () => void;
  isLoading?: boolean;
  placeholder?: string;
}

export function SearchBar({ value, onChange, onSearch, isLoading, placeholder }: SearchBarProps) {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      onSearch();
    }
  };

  return (
    <div className="flex gap-2 w-full max-w-2xl">
      <div className="relative flex-1">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-500" />
        <Input
          type="text"
          className="pl-10 bg-zinc-900 border-zinc-800 text-zinc-200"
          placeholder={placeholder || "Search codebase semantically..."}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
        />
      </div>
      <Button onClick={onSearch} disabled={isLoading || !value.trim()}>
        {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Search"}
      </Button>
    </div>
  );
}
