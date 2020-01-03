from pyspark.sql.functions import explode
from pyspark.sql.functions import col
from utils.infrastructure_utils import SparkAlgoUtil
from utils.infrastructure_utils import load_yaml

configs = load_yaml('utils\config.yml')

# Relations-Base algorithm:
spark_factory = SparkAlgoUtil()
nodes_df = spark_factory.nodes_df_creation(path=configs['nodes_file_path'])
relation_df = spark_factory.relation_df_creation(path=configs['relation_file_path'])
ways_df = spark_factory.ways_df_creation(path=configs['ways_file_path'], algorithm_type='relation')
join_way_relation = ways_df.join(relation_df, 'way_id')\
    .select(col('street_name'), explode(col('nodes')).name('nodes_explode'))\
    .select('street_name', 'nodes_explode.nodeId')
join_way_relation_nodes = join_way_relation.join(nodes_df, 'nodeId')
group_results = join_way_relation_nodes.groupBy('street_name', 'amenity_type').count().sort(col("street_name").desc())
group_results.toPandas().to_csv('relation_algo.csv')

# Ways-Base algorithm:
ways_df = spark_factory.ways_df_creation(path=configs['ways_file_path'], algorithm_type='ways')
nodes_df = spark_factory.nodes_df_creation(path=configs['nodes_file_path'])
join_results = ways_df.join(nodes_df, 'nodeId')
group_results = join_results.groupBy('street_name', 'amenity_type').count().sort(col("street_name").desc())
group_results.toPandas().to_csv('ways_algo.csv')

