from fastapi import FastAPI, HTTPException
import httpx
from typing import List, Dict

app = FastAPI(title="Gist Lookup API", version="1.0")

GITHUB_API = "https://api.github.com"


@app.get("/{username}", response_model=List[Dict])
async def get_public_gists(username: str):
    """
    Returns list of public Gists for the given GitHub username.
    Example: /octocat
    """
    url = f"{GITHUB_API}/users/{username}/gists"

    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                url,
                headers={"Accept": "application/vnd.github.v3+json"},
                timeout=8.0
            )
            r.raise_for_status()
            gists = r.json()

            # Keep only useful fields – clean & small payload
            return [
                {
                    "id": g["id"],
                    "description": g["description"] or "(no description)",
                    "html_url": g["html_url"],
                    "file_count": len(g["files"]),
                    "created_at": g["created_at"],
                }
                for g in gists
            ]

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(404, detail=f"GitHub user '{username}' not found")
            if e.response.status_code == 403:
                raise HTTPException(429, detail="GitHub API rate limit – wait a bit")
            raise HTTPException(502, detail="GitHub API error")

        except Exception:
            raise HTTPException(500, detail="Something went wrong")