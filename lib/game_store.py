import json
import os
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.utils import embedding_functions

DB_PATH = "chromadb"
COLLECTION_NAME = "udaplay"


def make_embedding_function():
    """Embedding function shared by Part 1 (indexing) and Part 2 (querying)."""
    return embedding_functions.OpenAIEmbeddingFunction(
        api_key_env_var="OPENAI_API_KEY",
        api_base=os.getenv("OPENAI_BASE_URL"),
    )


class GameVectorStore:
    """Reusable manager for the UdaPlay game collection in a persistent ChromaDB."""

    def __init__(self, path: str = DB_PATH, name: str = COLLECTION_NAME):
        self.client = chromadb.PersistentClient(path=path)
        self.embedding_fn = make_embedding_function()
        self.name = name
        self.collection = self.client.get_or_create_collection(
            name=name, embedding_function=self.embedding_fn
        )

    @staticmethod
    def load_games(data_dir: str = "games") -> List[Dict[str, Any]]:
        """Read every JSON game file in data_dir; the file name (e.g. 001) becomes the id."""
        games = []
        for file_name in sorted(os.listdir(data_dir)):
            if not file_name.endswith(".json"):
                continue
            with open(os.path.join(data_dir, file_name), "r", encoding="utf-8") as f:
                game = json.load(f)
            game["id"] = os.path.splitext(file_name)[0]
            games.append(game)
        return games

    @staticmethod
    def to_text(game: Dict[str, Any]) -> str:
        """Text that gets embedded for one game."""
        return (
            f"[{game['Platform']}] {game['Name']} ({game['YearOfRelease']}) - "
            f"{game['Genre']} game published by {game['Publisher']}. {game['Description']}"
        )

    def index_games(self, data_dir: str = "games") -> int:
        """Embed and upsert all games. Safe to re-run: existing ids are overwritten."""
        games = self.load_games(data_dir)
        self.collection.upsert(
            ids=[g["id"] for g in games],
            documents=[self.to_text(g) for g in games],
            metadatas=[{k: v for k, v in g.items() if k != "id"} for g in games],
        )
        return len(games)

    def count(self) -> int:
        return self.collection.count()

    def search(self, query: str, n_results: int = 3, where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Semantic search. Returns a list of dicts, best match first, with a distance."""
        res = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        return [
            {"id": i, "document": d, "metadata": m, "distance": dist}
            for i, d, m, dist in zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0])
        ]
