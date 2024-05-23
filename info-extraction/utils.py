def remove_ref(text):
    keywords = ["\nreferences", "\nbibliography"]
    for k in keywords:
        index = text.lower().rfind(k)
        text = text[:index]
    return text


def split_paper(
    paper_content: str,
    max_len: int = 30000,
    window_len: int = 20000,
    hop_len: int = 10000
):
    '''
    Split the paper into chunks in case it is too long

    Statistic of content length on 200 papers
    Max: 48017
    Min: 844
    Mean: 9187
    '''
    # Ignore this if using GPT-4
    if len(paper_content) < max_len:
        return [paper_content]

    i = 0
    chunks = []
    while i < len(paper_content):
        if len(paper_content[i:]) < max_len:
            chunks.append(paper_content[i:])
            break

        sub_content = paper_content[i:i+window_len]
        chunks.append(sub_content)
        i += hop_len

    if len(chunks) > 5:
        print("Too many chunks", len(chunks))
        print("Truncated to 5 chunks")
        chunks = chunks[:3] + chunks[-2:]
    return chunks


def calculate_openai_price(output_token_count, input_token_count):
    input_price = input_token_count * 0.50 / 1e6
    output_price = output_token_count * 1.50 / 1e6
    return input_price + output_price  # in USD


def log_token_report(output_token_count, input_token_count):
    result = f"Input Tokens: {input_token_count}"
    result += f" | Output Tokens: {output_token_count}"
    price = calculate_openai_price(output_token_count, input_token_count)
    result += f" | Price: ${price}"
    print(result)
