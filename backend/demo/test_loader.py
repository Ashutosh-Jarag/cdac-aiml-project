from services.ai.document.loader import document_loader

docs = document_loader.load("demo/sample.txt")

print("=" * 50)

print(f"Documents : {len(docs)}")

print("=" * 50)

print(docs[0].page_content)

print("=" * 50)

print(docs[0].metadata)