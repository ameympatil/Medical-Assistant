import wikipediaapi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def fetch_munich_wiki():
    """
    Fetches the Wikipedia page for Munich using the Wikipedia API.
    Returns the page content as text.
    """
    try:
        # Create a Wikipedia API object with a custom user agent
        wiki = wikipediaapi.Wikipedia(
            language="en", user_agent="MunichInfoBot/1.0 (your@email.com)"
        )

        # Fetch the Munich page
        munich_page = wiki.page("Munich")

        # Check if the page exists
        if not munich_page.exists():
            raise Exception("Failed to fetch Munich Wikipedia page")

        # Save the data in .txt file
        with open("munich_wiki.txt", "w", encoding="utf-8") as file:
            file.write(munich_page.text)

        # Return the full text content
        return munich_page.text
    except Exception as e:
        print(f"Error fetching Munich Wikipedia page: {e}")
        return None


def chunk_text(text):
    """
    Split the text into manageable chunks.
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=256,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        chunks = text_splitter.split_text(text)
        return chunks
    except Exception as e:
        print(f"Error chunking text: {e}")
        return []


def create_faiss_index(chunks):
    """
    Create and populate the FAISS index.
    """
    try:
        # Initialize embeddings using a Hugging Face model
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Create FAISS index
        faiss_index = FAISS.from_texts(chunks, embeddings)

        # Save FAISS Index
        faiss_index.save_local("faiss_index")
        return faiss_index
    except Exception as e:
        print(f"Error creating FAISS index: {e}")
        return None


def load_faiss_index(index):
    """
    Load the FAISS index from a local file.
    """
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        faiss_index = FAISS.load_local(
            index, embeddings, allow_dangerous_deserialization=True
        )
        return faiss_index
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        return None


def similarity_search(faiss_index, query, n_results=4):
    """
    Query the FAISS index and return top matches.
    """
    try:
        similar_data = ""
        results = faiss_index.similarity_search(query, k=n_results)
        for r in results:
            similar_data += "\n" + r.page_content
        return similar_data
    except Exception as e:
        print(f"Error performing similarity search: {e}")
        return ""


if __name__ == "__main__":
    query = "In which country is Munich situated?"
    faiss_index = load_faiss_index("faiss_index")
    if faiss_index:
        context = similarity_search(faiss_index, query)
        print(context)
