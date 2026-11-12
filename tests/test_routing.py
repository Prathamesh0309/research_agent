import pytest

from graph import should_continue
from schemas import ResearchState


def make(**kw):
    return ResearchState(query="x", **kw)


@pytest.mark.parametrize(
    "state, expected",
    [
        # Coverage is poor and there is budget left: go search again.
        (make(has_gaps=True, coverage_score=0.5, iteration=1), "searcher"),
        # Coverage is poor but the iteration cap is hit: stop and write.
        (make(has_gaps=True, coverage_score=0.5, iteration=3), "writer"),
        # No gaps reported: write.
        (make(has_gaps=False, coverage_score=0.9, iteration=1), "writer"),
        # Gaps flagged but score is already at the threshold: write.
        (make(has_gaps=True, coverage_score=0.75, iteration=1), "writer"),
    ],
)
def test_should_continue(state, expected):
    assert should_continue(state) == expected
