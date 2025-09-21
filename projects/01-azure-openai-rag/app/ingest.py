import os, glob, uuid
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchFieldDataType,
    SearchableField,
    CorsOptions,
)

try:  # Optional semantic configuration models
    from azure.search.documents.indexes.models import (
        SemanticConfiguration,
        PrioritizedFields,
        SemanticField,
        SemanticSettings,
    )
except ImportError:  # pragma: no cover
    SemanticConfiguration = PrioritizedFields = SemanticField = SemanticSettings = None

try:
    from azure.search.documents.indexes.models import VectorSearch, VectorSearchProfile, HnswAlgorithmConfiguration
except ImportError:  # pragma: no cover - vector support added in newer SDKs
    VectorSearch = VectorSearchProfile = HnswAlgorithmConfiguration = None

INDEX_NAME = os.getenv("SEARCH_INDEX_NAME", "rag-demo-index")
ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"].strip()
API_KEY = os.environ["AZURE_SEARCH_API_KEY"].strip()
DATA_DIR = os.getenv("DATA_DIR", "./data")

def ensure_index():
    sic = SearchIndexClient(endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY))
    try:
        _ = sic.get_index(INDEX_NAME)
        print(f"Index '{INDEX_NAME}' already exists.")
        return
    except Exception:
        pass

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="title", type=SearchFieldDataType.String, sortable=True, filterable=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="url", type=SearchFieldDataType.String, filterable=True, sortable=True, facetable=False),
    ]

    index_kwargs = {
        "name": INDEX_NAME,
        "fields": fields,
        "cors_options": CorsOptions(allowed_origins=["*"])
    }

    attribute_map = getattr(SearchIndex, "_attribute_map", {})

    if all([SemanticSettings, SemanticConfiguration, PrioritizedFields, SemanticField]) and "semantic_settings" in attribute_map:
        index_kwargs["semantic_settings"] = SemanticSettings(configurations=[
            SemanticConfiguration(
                name="default",
                prioritized_fields=PrioritizedFields(
                    title_field=SemanticField(field_name="title"),
                    content_fields=[SemanticField(field_name="content")]
                )
            )
        ])

    if VectorSearch and VectorSearchProfile and HnswAlgorithmConfiguration and "vector_search" in attribute_map:
        index_kwargs["vector_search"] = VectorSearch(
            profiles=[VectorSearchProfile(name="none", algorithm_configuration_name="hnsw")],
            algorithms=[HnswAlgorithmConfiguration(name="hnsw")]
        )

    index = SearchIndex(**index_kwargs)
    sic.create_index(index)
    print(f"Created index '{INDEX_NAME}'.")

def upload_docs():
    sc = SearchClient(endpoint=ENDPOINT, index_name=INDEX_NAME, credential=AzureKeyCredential(API_KEY))
    actions = []
    for path in glob.glob(os.path.join(DATA_DIR, "*.md")):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        title = os.path.basename(path).replace("_", " ").replace(".md","").title()
        url = f"file://{os.path.abspath(path)}"
        actions.append({
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "url": url
        })
    if actions:
        r = sc.upload_documents(actions)
        succeeded = sum(1 for x in r if x.succeeded)
        print(f"Uploaded {succeeded}/{len(actions)} documents.")
    else:
        print("No documents found to upload.")

if __name__ == "__main__":
    ensure_index()
    upload_docs()
