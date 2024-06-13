import sys
import pandas as pd
from PAMI.extras.DF2DB.DenseFormatDF import DenseFormatDF
import matplotlib.pyplot as plt

def process_csv(file_path):
    try:
        dataset = pd.read_csv(file_path, index_col=0)

        # Remove 'TimeStamp' column
        dataset.drop('TimeStamp', inplace=True, axis=1)

        # Remove columns with 'Unnamed'
        sensor_with_info = [i for i in dataset if 'Unnamed' in i]
        dataset.drop(columns=sensor_with_info, inplace=True, axis=1)

        # Fill NaN values with 0
        dataset = dataset.fillna(0)

        # Get max value in each column
        max_value_in_each_column = dataset.max()

        # Plot the data and save it to a file
        ax = max_value_in_each_column.plot()
        plt.savefig('graph.png')

        return 'graph.png'
      
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    csv_file_path = sys.argv[1]

    # Process the CSV file
    image_file_path = process_csv(csv_file_path)
    print(image_file_path)
