import os
import re
import pandas as pd
import gradio as gr
import psycopg2

from database.base import Database
from langchain.schema.messages import BaseMessage
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import wait_fixed, stop_after_attempt, retry
from .template import sql_template, refiner_template
from search.search_engine import SearchEngine
from schemas import PaperResponse


load_dotenv()


engine = SearchEngine(
    index_dir="./data/index",
    top_k_candidates=10,
)


collection = Database("paper_demo", PaperResponse)

def fetch_result(user_query: str):
    l_result = engine.query(user_query, top_k=10)
    if len(l_result) == 0:
        l_result = engine.query(user_query, top_k=10)

    l_result_report = []
    for result in l_result:
        paper_id = result.metadata['paper_id']
        database_item = collection.get(paper_id)
        
        l_result_report.append({
            'Title': database_item.title,
            'DOI': database_item.doi,
            'URL': database_item.url,
            'Publication Year': database_item.publication_year,
            'Journal': database_item.journal,
            'Conclusion': database_item.conclusions,
            'Demographic': database_item.demographic,
            'Diseases': database_item.diseases            
        })

    return pd.DataFrame(l_result_report)


def export_csv(d):
    d.to_csv("output.csv")
    return gr.File(value="output.csv", visible=True)


def search():
    with gr.Blocks() as demo:
        gr.Markdown(
            """
        # Search Paper Tools
        Start to write the query you want to search for paper
        """
        )

        txtbox_user_query = gr.Textbox(label="User Query", value="Gut microbiome and also diabetes")

        btn_fetch_result = gr.Button("Fetching the result")

        search_result = gr.DataFrame(label="Final Result")
        
        with gr.Column():
            button = gr.Button("Export")
            csv = gr.File(interactive=False, visible=False)

        button.click(export_csv, search_result, csv)
        btn_fetch_result.click(fetch_result, inputs=[txtbox_user_query], outputs=[search_result])
