import util


def test_get_data_files():
    files = util.get_data_files(base_dir="tests/pipeline/test_data")
    assert len(files) == 4


def test_load_data():
    data = util.load_data(None)
    files = util.get_data_files(base_dir="tests/pipeline/test_data/")
    for file in files:
        data = util.load_data(file)
        assert data is not None


def test_load_data_str():
    util.load_data_str(None)
    jstr = '{"hello":"world"}'
    data = util.load_data_str(jstr)
    assert isinstance(data, dict)


def test_save_data():
    util.save_data("/path_does_not_exist", None)
    data = util.load_data_str('{"hello":"world"}')
    util.save_data("/tmp/test_save_data", data)
