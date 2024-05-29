import os

import gradio as gr
from ai_playground.nl_2_sql import ui as nl_2_sql_ui
from ai_playground.search_paper import search as search_paper


def main():
    with gr.Blocks() as demo:
        gr.Markdown("AI Playground")
        
        with gr.Tab("Search Paper"):
            search_paper()

        with gr.Tab("Natural Language to SQL"):
            nl_2_sql_ui()

    demo.launch(server_name="0.0.0.0", share=False, show_api=True)

if __name__ == "__main__":
    main()
