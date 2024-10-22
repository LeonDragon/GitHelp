import requests
from typing import Dict, Any, Optional, List

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

def bulk_search_papers(
    query: str,
    fields: List[str] = ["title", "abstract", "year", "authors", "url", "venue"],
    sort: Optional[str] = None,
    publication_types: Optional[List[str]] = None,
    open_access_pdf: bool = False,
    min_citation_count: Optional[int] = None,
    publication_date_or_year: Optional[str] = None,
    venue: Optional[str] = None,
    fields_of_study: Optional[List[str]] = None,
    limit: int = 1000,
    offset: int = 0,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform a bulk search for papers using the Semantic Scholar API.

    Args:
        query (str): Text query to match against paper titles and abstracts.
        fields (List[str]): List of fields to return for each paper.
        sort (Optional[str]): Sort order for results (e.g., "publicationDate:desc").
        publication_types (Optional[List[str]]): List of publication types to include.
        open_access_pdf (bool): If True, only include papers with public PDFs.
        min_citation_count (Optional[int]): Minimum number of citations for included papers.
        publication_date_or_year (Optional[str]): Date range for publication dates.
        venue (Optional[str]): Comma-separated list of venues to include.
        fields_of_study (Optional[List[str]]): List of fields of study to include.
        limit (int): Maximum number of results to return (up to 1000).
        offset (int): Number of results to skip (for pagination).
        token (Optional[str]): Continuation token for fetching next batch of results.

    Returns:
        Dict[str, Any]: A dictionary containing the search results, total count, and continuation token.

    Raises:
        requests.exceptions.RequestException: If there's an error with the API request.
        ValueError: If the API returns an error message.

    Example:
        results = bulk_search_papers(
            query="machine learning",
            fields=["title", "abstract", "year"],
            sort="citationCount:desc",
            publication_types=["JournalArticle", "Conference"],
            min_citation_count=10,
            publication_date_or_year="2010:",
            fields_of_study=["Computer Science"]
        )
    """
    params = {
        "query": query,
        "fields": ",".join(fields),
        "limit": limit,
        "offset": offset
    }

    if sort:
        params["sort"] = sort
    if publication_types:
        params["publicationTypes"] = ",".join(publication_types)
    if open_access_pdf:
        params["openAccessPdf"] = "true"
    if min_citation_count is not None:
        params["minCitationCount"] = min_citation_count
    if publication_date_or_year:
        params["publicationDateOrYear"] = publication_date_or_year
    if venue:
        params["venue"] = venue
    if fields_of_study:
        params["fieldsOfStudy"] = ",".join(fields_of_study)
    if token:
        params["token"] = token

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise ValueError(f"API returned an error: {data['error']}")

    return data
