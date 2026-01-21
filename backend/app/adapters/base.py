"""
Base data adapter for PublicPulse
"""
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from app.config import YOUTUBE_API_KEY, MAX_VIDEOS_PER_QUERY, MAX_COMMENTS_PER_VIDEO, MAX_TOTAL_COMMENTS_PER_ITEM


class DataAdapter(ABC):
    """Base class for category-specific data adapters"""

    def __init__(self):
        self.youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    @abstractmethod
    def get_search_queries(self, item_name: str) -> List[str]:
        """
        Return list of YouTube search queries for this category

        Args:
            item_name: Name of the movie/gadget

        Returns:
            List of search query strings
        """
        pass

    @abstractmethod
    def get_recency_days(self) -> int:
        """Return number of days for video recency filter"""
        pass

    def fetch_comments(self, item_name: str) -> List[str]:
        """
        Fetch YouTube comments for an item

        Args:
            item_name: Name of the movie/gadget

        Returns:
            List of normalized comment texts
        """
        queries = self.get_search_queries(item_name)
        all_comments = []

        for query in queries:
            if len(all_comments) >= MAX_TOTAL_COMMENTS_PER_ITEM:
                break

            video_ids = self._search_videos(query)

            for video_id in video_ids:
                if len(all_comments) >= MAX_TOTAL_COMMENTS_PER_ITEM:
                    break

                comments = self._fetch_video_comments(video_id)
                all_comments.extend(comments)

        # Cap at max limit
        return all_comments[:MAX_TOTAL_COMMENTS_PER_ITEM]

    def _search_videos(self, query: str) -> List[str]:
        """Search for videos matching query"""
        recency_days = self.get_recency_days()
        published_after = (datetime.utcnow() - timedelta(days=recency_days)).isoformat("T") + "Z"

        try:
            request = self.youtube.search().list(
                part="id",
                q=query,
                type="video",
                maxResults=MAX_VIDEOS_PER_QUERY,
                publishedAfter=published_after,
                order="relevance",
                relevanceLanguage="en",
            )
            response = request.execute()

            video_ids = []
            for item in response.get("items", []):
                if item["id"]["kind"] == "youtube#video":
                    video_ids.append(item["id"]["videoId"])

            return video_ids

        except Exception as e:
            print(f"Error searching videos for '{query}': {e}")
            return []

    def _fetch_video_comments(self, video_id: str) -> List[str]:
        """Fetch comments from a specific video"""
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=MAX_COMMENTS_PER_VIDEO,
                order="relevance",
                textFormat="plainText",
            )
            response = request.execute()

            comments = []
            for item in response.get("items", []):
                comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                # Normalize: strip whitespace
                comment_text = comment_text.strip()
                if comment_text:
                    comments.append(comment_text)

            return comments

        except Exception as e:
            print(f"Error fetching comments for video {video_id}: {e}")
            return []
