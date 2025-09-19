"""Project-wide shared test fixtures."""

import os

import pytest

IF_DUMMY_SPARK = 'DUMMY_SPARK' in os.environ

@pytest.fixture(scope='session', autouse=True)
def spark_ctx():
    """A simple context fixture for backward compatibility.
    
    After migration to Dask, this fixture returns None since 
    Drudge no longer requires a context parameter.
    """
    
    # For backward compatibility with tests that still expect a context,
    # we return a dummy context object for tests that still use dummy_spark
    if IF_DUMMY_SPARK:
        from dummy_spark import SparkConf, SparkContext
        conf = SparkConf()
        ctx = SparkContext(master='', conf=conf)
        return ctx
    else:
        # For Dask-based drudge, no context is needed
        return None


def skip_in_spark(**kwargs):
    """Skip the test in Apache Spark environment.

    Mostly due to issues with pickling some SymPy objects, some tests have to
    be temporarily skipped in Apache Spark environment.
    """
    return pytest.mark.skipif(not IF_DUMMY_SPARK, **kwargs)
