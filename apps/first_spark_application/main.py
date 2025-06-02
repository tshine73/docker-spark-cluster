import os
import time

import matplotlib.pyplot as plt
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, round, col, lit

WORKER_DIR = os.getenv("SPARK_WORKER_DIR", "")
DATA_INPUT_PATH = os.path.join(WORKER_DIR, "data/input")
DATA_OUTPUT_PATH = os.path.join(WORKER_DIR, "data/output")


def init():
    spark = SparkSession.builder.getOrCreate()
    return spark


def main():
    start = time.time_ns()

    spark = init()
    ratings_file = os.path.join(DATA_INPUT_PATH, "ratings.csv")
    movies_file = os.path.join(DATA_INPUT_PATH, "movies.csv")

    rating_df = spark.read.option("header", True).csv(ratings_file)
    movie_df = spark.read.option("header", True).csv(movies_file)

    average_rating = rating_df.groupBy("movieId").agg(round(avg("rating"), 1).alias("average_rating"))
    average_rating.show()

    joined_df = average_rating.join(movie_df, on="movieId") \
        .orderBy(col("average_rating").desc(), col("title").asc())
    joined_df.show()

    total = average_rating.count()
    movie_rating_count = average_rating.groupBy("average_rating").agg(count("*").alias("count_movies")) \
        .withColumn("percentage", round((col("count_movies") / lit(total)) * 100, 2)) \
        .orderBy("average_rating", ascending=False)
    movie_rating_count.show()

    generate_chart(movie_rating_count.toPandas())

    csv_output_path = os.path.join(DATA_OUTPUT_PATH, "movie_rating_count")
    movie_rating_count.repartition(10).write.mode("overwrite").csv(csv_output_path)

    end = time.time_ns()
    print(f"Execution time: {(end - start) / 1000000000} seconds")


def generate_chart(df):
    df.plot.line(x='average_rating', y='percentage', xticks=np.arange(0.5, 5, step=0.5))
    plt.show()
    plot_output_path = os.path.join(DATA_OUTPUT_PATH, "movie_rating_count_plot.png")
    plt.savefig(plot_output_path)


if __name__ == '__main__':
    main()
