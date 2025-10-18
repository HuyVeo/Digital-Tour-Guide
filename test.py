import chromadb
import csv
docs = []
metadatas = []
ids = []
with open("dataset.csv", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    for i, line in enumerate(reader):
        if len(line) < 4:
            continue
        docs.append(line[1])
        metadatas.append({
            "item_id": line[0],
            "Đặc Điểm": line[2],
            "Thời kỳ": line[3],
            "Công dụng / Ý nghĩa": line[4],
        })
        ids.append(str(i))

print(docs)

# lưu trữ
chroma_client = chromadb.PersistentClient(path="./chroma_db2")

try:
    collection = chroma_client.get_collection("docs")
    print("lưu lại docs và sử dụng lại")
except:
    collection = chroma_client.create_collection(name="docs")
    print("Tạo mới collection 'docs'")

collection.add(
        ids=ids,
        documents=docs,
        metadatas=metadatas,
)
# Tìm kiếm
results = collection.query(
    query_texts=["Khuôn đúc rìu đá "],
    n_results=4,
    include=["documents", "metadatas", "distances"]
)
print("\nKết quả :")
for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]):
    print(f"- {doc}")
    print(f"  ID: {meta.get('item_id')}, Đặc Điểm: {meta.get('Đặc Điểm')}, Tk: {meta.get('Thời kỳ')}, Cong dung: {meta.get('Công dụng / Ý nghĩa')},Distance: {dist:.4f}")
# print(results)
