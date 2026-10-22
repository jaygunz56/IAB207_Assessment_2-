import os

MODEL_NAME = 'all-MiniLM-L6-v2'

# hosts like PythonAnywhere can't download from Hugging Face, so the model can be saved
# into a models folder in the project instead
LOCAL_MODEL = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', MODEL_NAME)

# from testing, unrelated events score around 0.2 to 0.25, so anything under this isn't a real match
MIN_SCORE = 0.3

model = None


def get_model():
    # the model takes a few seconds to load so only do it once, the first time it's needed
    global model
    if model is None:
        from sentence_transformers import SentenceTransformer
        if os.path.isdir(LOCAL_MODEL):
            model = SentenceTransformer(LOCAL_MODEL)
        else:
            model = SentenceTransformer(MODEL_NAME)
    return model


def event_text(event):
    return f'{event.title}. {event.category.name}. {event.description}'


def rank_events(search, events):
    # returns (event, score) pairs with the best match first, scores go from -1 to 1
    if not events:
        return []

    from sentence_transformers import util

    model = get_model()
    search_embedding = model.encode(search, convert_to_tensor=True)
    event_embeddings = model.encode([event_text(e) for e in events], convert_to_tensor=True)
    scores = util.cos_sim(search_embedding, event_embeddings)[0]

    results = []
    for event, score in zip(events, scores):
        results.append((event, float(score)))

    results.sort(key=lambda result: result[1], reverse=True)
    return results
