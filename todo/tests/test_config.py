from .. import config

def test_config():
    for var in ("HOST", "PORT", "USER", "PASSWORD", "DBNAME", "TESTDB"):
        assert hasattr(config, var)
        assert getattr(config, var)
