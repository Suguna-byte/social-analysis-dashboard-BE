from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import requests


class SocialAPIViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def fetch_trending_topics(self, request):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(
                'https://www.reddit.com/r/popular/hot.json',
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            reddit_data = response.json()
            posts = reddit_data.get('data', {}).get('children', [])
            
            trending_topics = []
            for post in posts[:10]:
                post_data = post.get('data', {})
                trending_topics.append({
                    'topic': post_data.get('title', ''),
                    'mentions': post_data.get('ups', 0),
                    'comments': post_data.get('num_comments', 0),
                    'subreddit': post_data.get('subreddit', ''),
                    'url': post_data.get('url', '')
                })
            
            return Response({
                'status': 'success',
                'trending_topics': trending_topics,
                'total_topics': len(trending_topics)
            })
        except requests.exceptions.RequestException as e:
            return Response({
                'status': 'error',
                'message': f'Failed to fetch trending topics: {str(e)}',
                'trending_topics': [],
                'total_topics': 0
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
