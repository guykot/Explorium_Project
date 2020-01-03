from utils.infrastructure_utils import SparkAlgoUtil
import pytest
from utils.infrastructure_utils import load_yaml
configs = load_yaml('/utils/config.yml')


@pytest.fixture(scope='function')
def spark_creation():
    return SparkAlgoUtil()


def test_nodes_df_creation(spark_creation):
    assert spark_creation.nodes_df_creation(path=configs['nodes_file_path']).count() > 0


def test_ways_df_creation(spark_creation):
    assert spark_creation.ways_df_creation(path=configs['ways_file_path'], algorithm_type='relation')\
               .count() > 0


def test_relation_df_creation(spark_creation):
    assert spark_creation.relation_df_creation(path=configs['relation_file_path']).count() > 0
