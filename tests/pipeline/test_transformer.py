import pytest
import transformer


@pytest.mark.xfail
def test_pipeline_args():
    transformer.main([""])
    transformer.main(["-i"])
    transformer.main(["-i", "src/tests/pipeline/test_data"])
    transformer.main(["-o"])
    transformer.main(["-i", "src/tests/pipeline/test_data", "-o"])
