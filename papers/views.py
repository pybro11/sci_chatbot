from django.shortcuts import render
# papers/views.py
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def search_papers(request):
    query = request.GET.get('query', '')
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&fields=title,abstract,citationCount"
    response = requests.get(url)
    
    if response.status_code == 200:
        papers = response.json().get('data')
        sorted_papers = sorted(papers, key=lambda x: -x['citationCount'])
        return Response(sorted_papers)
    return Response({'error': 'Failed to retrieve papers'}, status=500)

# papers/views.py
from .utils import summarize_text

@api_view(['GET'])
def summarize_paper(request):
    abstract = request.GET.get('abstract', '')
    if abstract:
        summary = summarize_text(abstract)
        return Response({'summary': summary})
    return Response({'error': 'No abstract provided'}, status=400)
