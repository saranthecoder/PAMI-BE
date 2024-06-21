import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from PAMI.correlatedPattern.basic import CoMine as alg # Import the CoMine algorithm

def process_data(input_file, separator, min_all_conf_count, min_sup_count_list):
    result = pd.DataFrame(columns=['algorithm', 'minSup', 'minAllConf', 'patterns', 'runtime', 'memory'])
    
    for min_sup_count in min_sup_count_list:
        obj = alg.CoMine(input_file, minSup=min_sup_count, minAllConf=min_all_conf_count, sep=separator)
        obj.mine()
        
        # Store the results in the data frame
        result.loc[result.shape[0]] = [
            'CoMine',
            min_sup_count,
            min_all_conf_count,
            len(obj.getPatterns()),
            obj.getRuntime(),
            obj.getMemoryRSS()
        ]
    
    return result

def plot_results(result, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Plotting the patterns vs minSup
    plt.figure()
    result.plot(x='minSup', y='patterns', kind='line')
    plt.title('Patterns vs Minimum Support')
    plt.xlabel('Minimum Support Count')
    plt.ylabel('Number of Patterns')
    plt.savefig(os.path.join(output_dir, 'patterns_vs_minsup.png'))
    
    # Plotting the runtime vs minSup
    plt.figure()
    result.plot(x='minSup', y='runtime', kind='line')
    plt.title('Runtime vs Minimum Support')
    plt.xlabel('Minimum Support Count')
    plt.ylabel('Runtime (s)')
    plt.savefig(os.path.join(output_dir, 'runtime_vs_minsup.png'))
    
    # Plotting the memory usage vs minSup
    plt.figure()
    result.plot(x='minSup', y='memory', kind='line')
    plt.title('Memory Usage vs Minimum Support')
    plt.xlabel('Minimum Support Count')
    plt.ylabel('Memory Usage (RSS)')
    plt.savefig(os.path.join(output_dir, 'memory_vs_minsup.png'))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script2.py <path_to_csv_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    separator = '\t'
    min_all_conf_count = 0.1
    min_sup_count_list = [100, 150, 200, 250, 300]
    
    # Process the data
    result = process_data(input_file, separator, min_all_conf_count, min_sup_count_list)
    
    # Print the result DataFrame
    print(result)
    
    # Define the output directory
    output_dir = os.path.join('src', 'GRAPHS')
    
    # Plot the results and save them in the specified directory
    plot_results(result, output_dir)
