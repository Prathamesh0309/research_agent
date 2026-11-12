from agents import searcher
from schemas import ResearchState


class FakeTavily:
    def __init__(self, results_by_query):
        self.results_by_query = results_by_query
        self.queries = []

    def search(self, query, max_results=3):
        self.queries.append(query)
        return {"results": self.results_by_query.get(query, [])}


def hit(url):
    return {"title": f"title {url}", "url": url, "content": "text"}


def test_first_pass_searches_every_sub_question(monkeypatch):
    fake = FakeTavily({"q1": [hit("a")], "q2": [hit("b")]})
    monkeypatch.setattr(searcher, "get_client", lambda: fake)

    state = searcher.run_searcher(ResearchState(query="x", sub_questions=["q1", "q2"]))

    assert fake.queries == ["q1", "q2"]
    assert [r["url"] for r in state.search_results] == ["a", "b"]
    assert state.iteration == 1


def test_revision_pass_keeps_earlier_results_and_searches_the_gap(monkeypatch):
    fake = FakeTavily({"missing detail": [hit("c")]})
    monkeypatch.setattr(searcher, "get_client", lambda: fake)
    state = ResearchState(
        query="x",
        sub_questions=["q1"],
        search_results=[{"question": "q1", **hit("a")}],
        gap_summary="missing detail",
        iteration=1,
    )

    state = searcher.run_searcher(state)

    assert fake.queries == ["missing detail"]  # searches the gap, not q1 again
    assert [r["url"] for r in state.search_results] == ["a", "c"]  # "a" is not lost
    assert state.iteration == 2


def test_duplicate_urls_are_not_added_twice(monkeypatch):
    fake = FakeTavily({"missing detail": [hit("a"), hit("c")]})
    monkeypatch.setattr(searcher, "get_client", lambda: fake)
    state = ResearchState(
        query="x",
        search_results=[{"question": "q1", **hit("a")}],
        gap_summary="missing detail",
        iteration=1,
    )

    state = searcher.run_searcher(state)

    assert [r["url"] for r in state.search_results] == ["a", "c"]
