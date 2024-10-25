import streamlit as st
import json
import os
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import itertools
import re


def load_json_files(folder_path):
    """Load all JSON files from the specified folder."""
    json_files = []
    for file in Path(folder_path).glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                json_files.append(data)
            except json.JSONDecodeError:
                st.warning(f"Error reading file: {file}")
    return json_files


def process_item(item):
    """Process an item that could be either a string or a dictionary."""
    if isinstance(item, str):
        return item
    elif isinstance(item, dict) and "nome" in item:
        return item["nome"]
    return None


def normalize_language_name(name):
    """Normalize programming language names, especially for C variants."""
    # Remove extra spaces and convert to lowercase
    name = name.strip().lower()

    # Special cases for C variants
    if name in ["c#", "c-sharp", "csharp"]:
        return "C#"
    elif name in ["c++", "cpp"]:
        return "C++"
    elif name == "c":
        return "C"

    # Capitalize first letter for other languages
    return name.capitalize()


def combine_category_data(json_files, categories, is_language=False):
    """Combine all items from specified categories across all files."""
    all_items = []
    for file in json_files:
        items = []
        # If categories is a list, combine all those categories
        if isinstance(categories, list):
            for category in categories:
                items.extend(file[category])
        else:
            items = file[categories]

        processed_items = []
        for item in items:
            processed_item = process_item(item)
            if processed_item:
                # Apply special normalization for programming languages
                if is_language:
                    processed_item = normalize_language_name(processed_item)
                processed_items.append(processed_item)
        all_items.extend(processed_items)
    return all_items


def create_wordcloud(texts, preserve_special_chars=False):
    """Create a word cloud from a list of texts."""
    if not texts:
        return None

    # Join texts with special handling for programming languages
    if preserve_special_chars:
        # Create a frequency dictionary instead of joining texts
        word_freq = {}
        for word in texts:
            word_freq[word] = word_freq.get(word, 0) + 1
    else:
        text = " ".join(texts)
        word_freq = None

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        font_path="arial.ttf",  # Change this to a font that supports Portuguese characters
        collocations=False,
        regexp=(
            r"\S+" if preserve_special_chars else None
        ),  # Preserve special characters when needed
    )

    if preserve_special_chars:
        wordcloud.generate_from_frequencies(word_freq)
    else:
        wordcloud.generate(text)

    return wordcloud


def main():
    st.title("Tech Stack Word Cloud Visualizer")

    # File uploader
    folder_path = st.text_input("Enter the folder path containing JSON files:")

    if folder_path and os.path.exists(folder_path):
        # Load all JSON files
        json_files = load_json_files(folder_path)

        if not json_files:
            st.error("No valid JSON files found in the specified folder.")
            return

        # Define category groups
        category_groups = {
            "Técnicas": (
                "tecnicas",
                False,
                False,
            ),  # (categories, is_language, preserve_special_chars)
            "Ferramentas e Plataformas": (["ferramentas", "plataformas"], False, False),
            "Linguagens": (
                "linguagens",
                True,
                True,
            ),  # Preserve special chars for languages
            "Frameworks": ("frameworks", False, False),
        }

        # Create word clouds for each category group
        for group_name, (
            categories,
            is_language,
            preserve_special_chars,
        ) in category_groups.items():
            st.header(group_name)

            # Combine data from all files for this category group
            category_data = combine_category_data(json_files, categories, is_language)

            if category_data:
                wordcloud = create_wordcloud(category_data, preserve_special_chars)

                if wordcloud:
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)
                    plt.close()

            else:
                st.write(f"No data found for {group_name}")

        # Display some statistics
        st.header("Statistics")
        st.write(f"Total files processed: {len(json_files)}")
        for group_name, (categories, is_language, _) in category_groups.items():
            items = combine_category_data(json_files, categories, is_language)
            st.write(f"Unique {group_name}: {len(set(items))}")

    elif folder_path:
        st.error("Invalid folder path. Please enter a valid path.")


if __name__ == "__main__":
    main()
