import kagglehub
import pandas as pd
import os

path = kagglehub.dataset_download("bwandowando/rotten-tomatoes-9800-movie-critic-and-user-reviews")

print("Path to dataset files:", path)
