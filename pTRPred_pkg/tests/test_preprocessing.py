import numpy as np
import pandas as pd
import pytest

from pTRPred import extract_X, na_handle


def test_extract_X_list_and_regex():
    df = pd.DataFrame({"a": ["1", "2"], "b": [3, 4], "temp1": [1, 2], "temp2": [3, 4]})
    X1 = extract_X(df, ["a", "b"])
    assert list(X1.columns) == ["a", "b"]
    assert X1.dtypes["a"].kind in ("i", "f")
    X2 = extract_X(df, "temp|b")
    assert set(X2.columns) == {"temp1", "temp2", "b"}


def test_extract_X_empty_selection():
    df = pd.DataFrame({"a": [1, 2]})
    with pytest.raises(ValueError):
        extract_X(df, "nope|missing")


def test_na_handle_omit_and_impute():
    A = np.array([[1.0, np.nan], [2.0, 3.0], [np.nan, 5.0]])
    B = na_handle(A, method="omit_rows")
    assert B.shape == (1, 2)
    C = na_handle(A, method="impute_mean")
    # col0 mean over {1,2} -> 1.5 imputes row2 col0
    assert np.isclose(C[2, 0], 1.5)
    # col1 has two non-na {3,5} -> mean 4 imputes row0 col1
    assert np.isclose(C[0, 1], 4.0)


def test_na_handle_pairwise():
    A = np.array([[1.0, np.nan]])
    B = na_handle(A, method="pairwise_complete")
    assert np.isnan(B[0, 1])
