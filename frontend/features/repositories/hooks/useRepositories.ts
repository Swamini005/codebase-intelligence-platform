"use client";

import { useState, useEffect } from "react";
import { Repository } from "../types";
import { fetchRepositories, connectGithubRepo } from "../services/api";

export function useRepositories() {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadRepos = async () => {
    try {
      setIsLoading(true);
      const data = await fetchRepositories();
      setRepositories(data);
    } catch (err: any) {
      setError(err.message || "Failed to load repositories");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadRepos();
  }, []);

  const addRepository = async (githubUrl: string) => {
    try {
      const newRepo = await connectGithubRepo(githubUrl);
      setRepositories((prev) => [newRepo, ...prev]);
      return newRepo;
    } catch (err: any) {
      setError(err.message || "Failed to connect repository");
      throw err;
    }
  };

  return {
    repositories,
    isLoading,
    error,
    refresh: loadRepos,
    addRepository,
  };
}
