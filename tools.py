from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain.tools.retriever import create_retriever_tool
import os
load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")

tavily_tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=False,
    include_domains=[
        "pakistanlawsite.com",          # Pakistan's largest legal database
        "ljcp.gov.pk",                  # Law and Justice Commission of Pakistan
        "supremecourt.gov.pk",          # Supreme Court of Pakistan
        "pljlawsite.com",              # Pakistan Law Journal
        "kpja.edu.pk",                 # Khyber Pakhtunkhwa Judicial Academy
        "shc.gov.pk",                  # Sindh High Court
        "lhc.gov.pk",                  # Lahore High Court
        "bhc.gov.pk",                  # Balochistan High Court
        "fia.gov.pk",                  # Federal Investigation Agency
        "punjab.gov.pk",              # Punjab Government Portal
        "molaw.gov.pk",               # Ministry of Law and Justice
        "na.gov.pk",                  # National Assembly of Pakistan
        "senate.gov.pk",              # Senate of Pakistan
        "pcw.gov.pk",                 # Punjab Commission on Women
        "ncsw.gov.pk"                 # National Commission on Status of Women
    ],
    exclude_domains=[
        "globalsearch.com",
        "genericnews.com",
        "indiankanoon.org",
        "barandbench.com"
    ]
)