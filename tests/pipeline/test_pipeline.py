import pytest

import pipeline


@pytest.fixture(autouse=True)
def mock_args(monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest", "-i", "/tmp", "-o", "/tmp"])


@pytest.mark.xfail
def test_pipeline_args():
    pipeline.main()
    pipeline.main([""])
    pipeline.main(["-i"])
    pipeline.main(["-i", "src/tests/pipeline/test_data"])


def test_process():
    pipeline.process_sighting(None, "src/tests/pipeline/test_data")


def test_arg_parse():
    arg_parse = pipeline.get_argparse()
    assert arg_parse is not None
