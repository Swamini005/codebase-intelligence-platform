import "./globals.css";
import React from "react";
import Link from "next/link";
import { FolderGit2, Search, Cpu, Settings, LayoutDashboard, Terminal } from "lucide-react";

export const metadata = {
  title: "Codebase Intelligence Platform",
  description: "AI-powered RAG Code Search and Architecture Visualizer",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-zinc-950 text-zinc-100 flex min-h-screen">
        {/* Sidebar */}
        <aside className="w-64 border-r border-zinc-800 bg-zinc-950 flex flex-col justify-between p-4 hidden md:flex">
          <div className="space-y-6">
            <Link href="/dashboard" className="flex items-center gap-2 px-2">
              <Terminal className="h-6 w-6 text-blue-500" />
              <span className="font-bold text-lg tracking-tight gradient-text">CodeIntel AI</span>
            </Link>
            
            <nav className="space-y-1">
              <Link
                href="/dashboard"
                className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md hover:bg-zinc-900 hover:text-zinc-100 transition-colors"
              >
                <LayoutDashboard className="h-4 w-4 text-zinc-400" />
                Dashboard
              </Link>
              <Link
                href="/repositories"
                className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md hover:bg-zinc-900 hover:text-zinc-100 transition-colors"
              >
                <FolderGit2 className="h-4 w-4 text-zinc-400" />
                Repositories
              </Link>
              <Link
                href="/search"
                className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md hover:bg-zinc-900 hover:text-zinc-100 transition-colors"
              >
                <Search className="h-4 w-4 text-zinc-400" />
                Global Search
              </Link>
              <Link
                href="/chat"
                className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md hover:bg-zinc-900 hover:text-zinc-100 transition-colors"
              >
                <Cpu className="h-4 w-4 text-zinc-400" />
                RAG Chat
              </Link>
            </nav>
          </div>
          
          <div className="border-t border-zinc-900 pt-4">
            <Link
              href="/settings"
              className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md hover:bg-zinc-900 hover:text-zinc-100 transition-colors"
            >
              <Settings className="h-4 w-4 text-zinc-400" />
              Settings
            </Link>
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 flex flex-col min-h-screen bg-zinc-950/60">
          {/* Top header navbar */}
          <header className="h-14 border-b border-zinc-800 bg-zinc-950 flex items-center justify-between px-6">
            <div className="text-sm font-medium text-zinc-400">Workspace / Default Project</div>
            <div className="flex items-center gap-3">
              <span className="h-2 w-2 rounded-full bg-green-500 animate-ping" />
              <span className="text-xs text-zinc-400 font-mono">Platform Active</span>
            </div>
          </header>
          
          {/* Page Container */}
          <div className="flex-1 p-6 overflow-y-auto">
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
