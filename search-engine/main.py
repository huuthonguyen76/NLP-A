from time import time
from search.search_engine import SearchEngine


def print_results(nodes):
    if len(nodes) == 0:
        print("No relevant papers found.")
    for node in nodes:
        print("=" * 20)
        print("Paper ID:", node.node.metadata["paper_id"])
        print("Score:", node.score)
        print(node.node.text)
        print()


if __name__ == "__main__":
    engine = SearchEngine(
        index_dir="./data/index",
        top_k_candidates=10,
    )

    while True:
        query = input("Query: ")
        if query.strip() == "q":
            break
        st = time()
        results = engine.query(query, top_k=10)
        print_results(results)
        print("Elapsed", time() - st)
        print()
