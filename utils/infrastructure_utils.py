from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import col
from pyspark.sql import SQLContext
from pyspark.sql.functions import size
import pyspark
import yaml


def load_yaml(path: str) -> dict:
    """
    Loading Yaml files from a giving path.
    :param path: A path to the Yaml file.
    :return:dict with Yaml's data.
    """
    with open(path, 'r') as f:
        yaml_file = yaml.load(f, Loader=yaml.FullLoader)
    return yaml_file


class SparkAlgoUtil:
    """This class define the configs and methods which required to execute the both Relation/Ways-base algorithm"""
    def __init__(self):
        try:
            self.spark = SparkSession.builder \
                .master('local') \
                .appName('myAppName') \
                .config("spark.sql.warehouse.dir", "file:///C:/temp") \
                .getOrCreate()
        except Exception as err:
            print("OS error: {0}".format(err))
        self.sc = self.spark.sparkContext
        self.sqlContext = SQLContext(self.sc)  # Using SQLContext to read parquet file
        self.sqlContext.setConf("spark.sql.parquet.binaryAsString", "true")  # Convert binary data in columns to Strings

    def nodes_df_creation(self, path: str) -> pyspark.sql.dataframe.DataFrame:
        """
        Generating a Pyspark-DF from a nodes-parquet file with only the nodes which tagged as amenity.
        :param path: Path to the parquet file.
        :return: Pyspark-DF which contains the identification number of all the nodes who are tagged only as amenity.
        """
        try:
            nodes_df = self.spark.read.parquet(path)
        except OSError:
            print('cannot open', path)
        nodes_df = nodes_df.select('id', 'tags').filter(size(col('tags')) > 0)
        nodes_df = nodes_df.select(col('id'), explode(col('tags')).name('exploded_tags'))\
            .filter(col('exploded_tags.key') == 'amenity')
        nodes_df = nodes_df.select("id", 'exploded_tags.value').withColumnRenamed('id', 'nodeId')\
            .withColumnRenamed('value', 'amenity_type')
        return nodes_df

    def relation_df_creation(self, path: str) -> pyspark.sql.dataframe.DataFrame:
        """
        Generating a Pyspark-DF from a relation-parquet file with only "street" relations.
        :param path: path to the parquet file.
        :return: Pyspark-DF which contains the streets name and ways Id.
        """
        try:
            relation_df = self.spark.read.parquet(path)
        except OSError:
            print('cannot open', path)
        relation_df = relation_df.withColumn("members_explode", explode(relation_df.members))\
            .filter(col('members_explode.role') == 'street')
        relation_df = relation_df.withColumn("street_name", explode(relation_df.tags))\
            .filter(col('street_name.key') == 'name').select('members_explode.id', 'street_name.value')\
            .withColumnRenamed('value', 'street_name').withColumnRenamed('id', 'way_id')
        return relation_df

    def ways_df_creation(self, path: str, algorithm_type: str) -> pyspark.sql.dataframe.DataFrame:
        """
        Generating a Pyspark-DF from a relation-parquet file with only "street" relations.
        :param algorithm_type:
        :param path: path to the parquet file.
        :return: Pyspark-DF which contains the streets name and ways Id.
        """
        try:
            ways_df = self.spark.read.parquet(path)
        except OSError:
            print('cannot open', path)
        if algorithm_type == 'relation':
            return ways_df.select('id', 'nodes').withColumnRenamed('id', 'way_id')
        else:  # Type of algorithm is 'way'
            ways_df = ways_df.select('tags', 'nodes').withColumn("tags_explode", explode(ways_df.tags))\
                .filter(col("tags_explode.key") == "name").withColumn("tags_explode_for_residential", explode(ways_df.tags))
            ways_df = ways_df.filter(col("tags_explode_for_residential.value") == "residential")\
                .select(col('tags_explode'), explode(col('nodes')).name('nodes_explode'))
            ways_df = ways_df.select(col('tags_explode.value'), col('nodes_explode.nodeId'))\
                .withColumnRenamed('value', 'street_name')
        return ways_df



