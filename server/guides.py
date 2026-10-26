"""Thin, read-only routes for the guides included with the app."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import Response

from lib.workbench.guides import GuideBook, GuideUnavailable
from server.workbench import render

ROOT = Path(__file__).resolve().parents[1]
router = APIRouter()


@router.get("/studio/guides")
def guides_home(request: Request, q: str = ""):
    book = GuideBook(ROOT)
    query = q.strip()[:200]
    groups = {}
    for guide in book.available():
        groups.setdefault(guide.group, []).append(guide)
    return render(request, "guides/index.html", active="learn", title="Guides | Prompt Chaining Studio",
                  groups=groups, query=query, hits=book.search(query) if query else [])


@router.get("/studio/guides/{slug}")
def guide_page(request: Request, slug: str):
    book = GuideBook(ROOT)
    try:
        document = book.read(slug)
    except GuideUnavailable:
        return render(request, "guides/not_found.html", active="learn", status=404,
                      title="Find a guide | Prompt Chaining Studio", query="")
    return render(request, "guides/read.html", active="learn", title=f"{document.title} | Guides",
                  document=document, related=book.related(document.guide), query="")


@router.get("/studio/guides/{slug}/download")
def download_guide(request: Request, slug: str):
    try:
        document = GuideBook(ROOT).read(slug)
    except GuideUnavailable:
        return render(request, "guides/not_found.html", active="learn", status=404,
                      title="Find a guide | Prompt Chaining Studio", query="")
    return Response(document.source, media_type="text/markdown",
                    headers={"Content-Disposition": f'attachment; filename="{Path(document.guide.source).name}"'})
