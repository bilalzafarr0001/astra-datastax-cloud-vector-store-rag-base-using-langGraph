# Simple RAG with Astra DB + LangGraph + Groq

1. Put your 3 keys in `.env`
2. Run:

```bash
uv run rag.py
```

`rag.py` is the whole project. It runs 4 steps in a straight line:

```
read_pdf  ->  save_to_astra  ->  search_astra  ->  ask_ai
```

The PDF it reads is `data/company_handbook.pdf`. To use your own PDF, put it in `data/` and change the file name in `rag.py`.
