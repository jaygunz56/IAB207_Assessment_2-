from sentence_transformers import util

MODEL_NAME = 'all-MiniLM-L6-v2'

model = None


def get_model():
    # the model takes a few seconds to load so only do it once, the first time it's needed
    global model
    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(MODEL_NAME)
    return model


def event_text(event):
    return f'{event.title}. {event.category.name}. {event.description}'


def rank_events(search, events):
    # returns (event, score) pairs with the best match first, scores go from -1 to 1
    if not events:
        return []

    model = get_model()
    search_embedding = model.encode(search, convert_to_tensor=True)
    event_embeddings = model.encode([event_text(e) for e in events], convert_to_tensor=True)
    scores = util.cos_sim(search_embedding, event_embeddings)[0]

    results = []
    for event, score in zip(events, scores):
        results.append((event, float(score)))

    results.sort(key=lambda result: result[1], reverse=True)
    return results
