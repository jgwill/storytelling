from typing import List

from pydantic import BaseModel, Field


class ChapterCount(BaseModel):
    """
    Schema for determining the total number of chapters in the story.
    """

    total_chapters: int = Field(
        ...,
        alias="TotalChapters",
        description="The total number of chapters in the story.",
    )


class CompletionCheck(BaseModel):
    """
    Schema for checking if an outline or chapter is complete.
    """

    is_complete: bool = Field(
        ...,
        alias="IsComplete",
        description="Boolean flag indicating if the content meets quality standards.",
    )


class SummaryCheck(BaseModel):
    """
    Schema for verifying that a generated chapter follows the outline.
    """

    did_follow_outline: bool = Field(
        ...,
        alias="DidFollowOutline",
        description="Boolean flag indicating if the chapter followed the outline.",
    )
    suggestions: str = Field(
        ..., alias="Suggestions", description="Suggestions for improvement."
    )


class StoryInfo(BaseModel):
    """
    Schema for the final metadata of the generated story.
    """

    title: str = Field(..., alias="Title", description="The title of the story.")
    summary: str = Field(..., alias="Summary", description="A summary of the story.")
    tags: str = Field(
        ..., alias="Tags", description="Comma-separated tags for the story."
    )
    overall_rating: int = Field(
        ..., alias="OverallRating", description="An overall rating for the story."
    )


class SceneList(BaseModel):
    """
    Schema for a list of scene outlines for a chapter.
    Pydantic doesn't directly support a root list, so we wrap it in a model.
    The prompt expects a direct JSON array of strings. The parser will handle this.
    """

    scenes: List[str] = Field(
        ..., description="A list of detailed outlines for each scene in a chapter."
    )
