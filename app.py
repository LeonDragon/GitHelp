import streamlit as st
import requests
from semanticscholar import SemanticScholar
import httpx
import pandas as pd
import re
import traceback
from bulk_search_api import bulk_search_papers

st.set_page_config(page_title="Semantic Scholar Paper Search", page_icon="📚", layout="wide")

st.title("Semantic Scholar Paper Search")

# Initialize Semantic Scholar client
sch = SemanticScholar()

# Sidebar for query type selection
query_type = st.sidebar.selectbox(
    "Select Query Type",
    ["Search Papers", "Bulk Search Papers", "Get Paper by ID", "Get Recommended Papers"]
)

# Initialize session state for storing results
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

def handle_api_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (requests.exceptions.RequestException, httpx.HTTPError) as e:
            st.error(f"An error occurred while connecting to the Semantic Scholar API: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    return wrapper

def highlight_match(text, query):
    return re.sub(f'({re.escape(query)})', r'**\1**', text, flags=re.IGNORECASE)

@handle_api_error
def search_papers(query, year, fields_of_study, page=1, limit=10):
    results = sch.search_paper(query, year=year, fields_of_study=fields_of_study, limit=limit, fields=['title', 'abstract', 'year', 'authors', 'url', 'venue'])
    st.session_state.search_results = results
    st.session_state.current_page = page

    st.write(f"Total results: {results.total}")
    
    if not results:
        st.warning("No results found.")
    else:
        start_number = (st.session_state.current_page - 1) * limit + 1
        for i, paper in enumerate(results, start=start_number):
            st.write(f"**Result {i}**")
            st.write(f"**Title:** {highlight_match(paper.title, query)}")
            st.write(f"**Year:** {paper.year}")
            st.write(f"**Journal/Venue:** {paper.venue}")
            st.write(f"**Abstract:** {highlight_match(paper.abstract if paper.abstract else 'N/A', query)}")
            st.write(f"**Authors:** {', '.join([author.name for author in paper.authors])}")
            st.write(f"**Paper Link:** [Semantic Scholar]({paper.url})")
            st.write("---")

@handle_api_error
def perform_bulk_search(query, sort, publication_types, open_access_pdf, min_citation_count, publication_date_or_year, venue, fields_of_study, page=1, limit=1000):
    try:
        offset = (page - 1) * limit
        results = bulk_search_papers(
            query=query,
            sort=sort,
            publication_types=publication_types,
            open_access_pdf=open_access_pdf,
            min_citation_count=min_citation_count,
            publication_date_or_year=publication_date_or_year,
            venue=venue,
            fields_of_study=fields_of_study,
            limit=limit,
            offset=offset
        )

        st.write(f"Total results found: {results['total']}")
        st.write(f"Displaying results {offset + 1} to {min(offset + limit, int(results['total']))}")

        if not results['data']:
            st.warning("No results found on this page.")
        else:
            for i, paper in enumerate(results['data'], start=offset + 1):
                st.write(f"**Result {i}**")
                st.write(f"**Title:** {paper['title']}")
                st.write(f"**Year:** {paper.get('year', 'N/A')}")
                st.write(f"**Journal/Venue:** {paper.get('venue', 'N/A')}")
                st.write(f"**Abstract:** {paper.get('abstract', 'N/A')}")
                st.write(f"**Authors:** {', '.join([author['name'] for author in paper.get('authors', [])])}")
                st.write(f"**Paper Link:** [Semantic Scholar]({paper.get('url', '#')})")
                st.write("---")

        st.session_state.search_results = results
        st.session_state.current_page = page

    except Exception as e:
        st.error(f"An error occurred during the bulk search: {str(e)}")
        st.write("Debug information:")
        st.write(f"Query: {query}")
        st.write(f"Sort: {sort}")
        st.write(f"Publication Types: {publication_types}")
        st.write(f"Open Access PDF: {open_access_pdf}")
        st.write(f"Min Citation Count: {min_citation_count}")
        st.write(f"Publication Date or Year: {publication_date_or_year}")
        st.write(f"Venue: {venue}")
        st.write(f"Fields of Study: {fields_of_study}")
        
        st.write("Detailed error traceback:")
        st.code(traceback.format_exc())

def export_to_excel():
    if st.session_state.search_results:
        data = []
        for paper in st.session_state.search_results:
            data.append({
                'Title': paper.title,
                'Year': paper.year,
                'Journal/Venue': paper.venue,
                'Abstract': paper.abstract,
                'Authors': ', '.join([author.name for author in paper.authors]),
                'URL': paper.url
            })
        df = pd.DataFrame(data)
        return df.to_csv(index=False).encode('utf-8')
    return None

def export_bulk_results_to_csv(results):
    if results:
        data = []
        for paper in results:
            data.append({
                'Title': paper.get('title', ''),
                'Year': paper.get('year', ''),
                'Journal/Venue': paper.get('venue', ''),
                'Abstract': paper.get('abstract', ''),
                'Authors': ', '.join([author.get('name', '') for author in paper.get('authors', [])]),
                'URL': paper.get('url', '')
            })
        df = pd.DataFrame(data)
        return df.to_csv(index=False).encode('utf-8')
    return None

if query_type == "Search Papers":
    st.header("Search Papers")
    search_query = st.text_input("Enter search query", value="Business process compliance")
    year = st.text_input("Enter year or range (e.g., 2000 or 1991-2020)", "")
    fields_of_study = st.multiselect("Select fields of study", ["Computer Science", "Medicine", "Physics", "Mathematics", "Biology", "Chemistry", "Business"], default=["Business", "Computer Science"])
    limit = st.slider("Number of results per page", min_value=1, max_value=100, value=10)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Search"):
            search_papers(search_query, year, fields_of_study, limit=limit)
    
    with col2:
        if st.session_state.search_results:
            csv = export_to_excel()
            st.download_button(
                label="Export to CSV",
                data=csv,
                file_name="search_results.csv",
                mime="text/csv",
            )
    
    # Pagination
    if st.session_state.search_results:
        total_pages = (st.session_state.search_results.total + limit - 1) // limit
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=st.session_state.current_page)
        if st.button("Go to Page"):
            search_papers(search_query, year, fields_of_study, page=page, limit=limit)

elif query_type == "Bulk Search Papers":
    st.header("Bulk Search Papers")
    st.write("Use complex query syntax for advanced searching. Examples:")
    st.code("""
    fish ladder  # matches papers that contain "fish" and "ladder"
    fish -ladder  # matches papers that contain "fish" but not "ladder"
    fish | ladder  # matches papers that contain "fish" or "ladder"
    "fish ladder"  # matches papers that contain the phrase "fish ladder"
    (fish ladder) | outflow  # matches papers that contain "fish" and "ladder" OR "outflow"
    fish~  # matches papers that contain "fish", "fist", "fihs", etc.
    "fish ladder"~3  # matches papers that contain the phrase "fish ladder" or "fish is on a ladder"
    """)
    
    search_query = st.text_area("Enter complex search query", value='"Business process compliance"')
    sort = st.selectbox("Sort by", ["", "paperId:asc", "paperId:desc", "publicationDate:asc", "publicationDate:desc", "citationCount:asc", "citationCount:desc"], index=4)  # Default to publicationDate:desc
    publication_types = st.multiselect("Publication Types", ["Review", "JournalArticle", "CaseReport", "ClinicalTrial", "Conference", "Dataset", "Editorial", "LettersAndComments", "MetaAnalysis", "News", "Study", "Book", "BookSection"], default=["JournalArticle", "Conference"])
    open_access_pdf = st.checkbox("Only include papers with public PDF")
    min_citation_count = st.number_input("Minimum Citation Count", min_value=0, value=5)
    publication_date_or_year = st.text_input("Publication Date or Year Range (e.g., 2010:2020 or 2019-03-05:2020-06-06)", value="2010:")
    venue = st.text_input("Venue (comma-separated list)", "")
    fields_of_study = st.multiselect("Fields of Study", ["Computer Science", "Medicine", "Chemistry", "Biology", "Materials Science", "Physics", "Geology", "Psychology", "Art", "History", "Geography", "Sociology", "Business", "Political Science", "Economics", "Philosophy", "Mathematics", "Engineering", "Environmental Science", "Agricultural and Food Sciences", "Education", "Law", "Linguistics"], default=["Business", "Computer Science"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Bulk Search"):
            perform_bulk_search(
                query=search_query,
                sort=sort if sort else None,
                publication_types=publication_types if publication_types else None,
                open_access_pdf=open_access_pdf,
                min_citation_count=min_citation_count if min_citation_count > 0 else None,
                publication_date_or_year=publication_date_or_year if publication_date_or_year else None,
                venue=venue if venue else None,
                fields_of_study=fields_of_study if fields_of_study else None
            )
    
    with col2:
        if st.session_state.get('search_results'):
            csv = export_bulk_results_to_csv(st.session_state.search_results['data'])
            st.download_button(
                label="Export to CSV",
                data=csv,
                file_name="bulk_search_results.csv",
                mime="text/csv",
            )
    
    # Pagination for bulk search
    if st.session_state.get('search_results'):
        total_results = int(st.session_state.search_results['total'])
        total_pages = (total_results + 999) // 1000
        page = st.number_input("Page", min_value=1, max_value=max(1, total_pages), value=st.session_state.current_page)
        if st.button("Go to Page"):
            perform_bulk_search(
                query=search_query,
                sort=sort if sort else None,
                publication_types=publication_types if publication_types else None,
                open_access_pdf=open_access_pdf,
                min_citation_count=min_citation_count if min_citation_count > 0 else None,
                publication_date_or_year=publication_date_or_year if publication_date_or_year else None,
                venue=venue if venue else None,
                fields_of_study=fields_of_study if fields_of_study else None,
                page=page
            )

elif query_type == "Get Paper by ID":
    st.header("Get Paper by ID")
    paper_id = st.text_input("Enter paper ID (e.g., DOI, arXiv ID, or Corpus ID)", value="10.1007/s10270-021-00892-z")
    
    if st.button("Get Paper"):
        if paper_id:
            get_paper(paper_id)
        else:
            st.warning("Please enter a paper ID.")

elif query_type == "Get Recommended Papers":
    st.header("Get Recommended Papers")
    paper_id = st.text_input("Enter paper ID for recommendations", value="10.1007/s10270-021-00892-z")
    
    if st.button("Get Recommendations"):
        if paper_id:
            get_recommendations(paper_id)
        else:
            st.warning("Please enter a paper ID.")

st.sidebar.markdown("---")
st.sidebar.info("Note: This app requires an active internet connection to access the Semantic Scholar API.")

