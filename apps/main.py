from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, round, col, lit

if __name__ == '__main__':
    spark = SparkSession.builder.getOrCreate()

    rating_df = spark.read.option("header", True).csv("data/input/ratings_sample.csv")
    movie_df = spark.read.option("header", True).csv("data/input/movies.csv")

    average_rating = rating_df.groupBy("movieId").agg(round(avg("rating"), 1).alias("average_rating"))
    joined_df = average_rating.join(movie_df, on="movieId")

    print(joined_df.show())
    print(joined_df.printSchema())

    total = average_rating.count()

    # .withColumn("percentage", round(col("count_movies") / lit(total), 4)) \

    move_rating_count = average_rating.groupBy("average_rating").agg(count("*").alias("count_movies")) \
        .withColumn("percentage", col("count_movies") / lit(total)) \
        .orderBy("average_rating", ascending=False)

    print(move_rating_count.show())
    print(move_rating_count.printSchema())

    move_rating_count.repartition(1).write.mode("overwrite").csv("data/output/move_rating_count.csv")
