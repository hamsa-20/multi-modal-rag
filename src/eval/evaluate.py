from src.retriever.retriever import Retriever
from src.rag.generator import answer_query
import time

bench = [
    {"id":"q1", "q":"What is the projected GDP growth for 2024-25?"},
    {"id":"q2", "q":"What does the report say about inflation in 2023?"}
]

r = Retriever()
for b in bench:
    t0 = time.time()
    ans = answer_query(b["q"], r)
    dt = time.time() - t0
    print("ID:", b["id"])
    print("Q:", b["q"])
    print("Time(s):", round(dt,2))
    print("A:", ans[:500])
    print("-"*40)
