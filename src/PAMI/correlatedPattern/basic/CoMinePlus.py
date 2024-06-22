import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from PAMI.extras.dbStats import TransactionalDatabase as stats
from PAMI.correlatedPattern.basic import CoMinePlus as alg
from PAMI.extras.graph import plotLineGraphFromDictionary as plt_dict

def analyze_database(input_file, separator):
    # Initialize and run the TransactionalDatabase class
    obj = stats.TransactionalDatabase(input_file, sep=separator)
    obj.run()

    # Print database statistics
    print(f'Database size : {obj.getDatabaseSize()}')
    print(f'Total number of items : {obj.getTotalNumberOfItems()}')
    print(f'Database sparsity : {obj.getSparsity()}')
    print(f'Minimum Transaction Size : {obj.getMinimumTransactionLength()}')
    print(f'Average Transaction Size : {obj.getAverageTransactionLength()}')
    print(f'Maximum Transaction Size : {obj.getMaximumTransactionLength()}')
    print(f'Standard Deviation Transaction Size : {obj.getStandardDeviationTransactionLength()}')
    print(f'Variance in Transaction Sizes : {obj.getVarianceTransactionLength()}')

    # Save item frequencies and transaction lengths
    item_frequencies = obj.getSortedListOfItemFrequencies()
    transaction_length = obj.getTransanctionalLengthDistribution()
    obj.save(item_frequencies, 'itemFrequency.csv')
    obj.save(transaction_length, 'transactionSize.csv')

    return obj

def plot_distributions(obj, output_dir):
    item_frequencies = obj.getFrequenciesInRange()
    transaction_length = obj.getTransanctionalLengthDistribution()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plt_dict.plotLineGraphFromDictionary(item_frequencies, end=100, title="Items' Frequency Graph", xlabel='No of items', ylabel='frequency')
    plt.savefig(os.path.join(output_dir, 'items_frequency_graph.png'))

    plt_dict.plotLineGraphFromDictionary(transaction_length, end=100, title='Transaction Distribution Graph', xlabel='transaction length', ylabel='frequency')
    plt.savefig(os.path.join(output_dir, 'transaction_distribution_graph.png'))

def mine_patterns(input_file, separator, min_sup, min_all_conf_count, output_file):
    # Initialize and run the CoMinePlus algorithm
    obj = alg.CoMinePlus(iFile=input_file, minSup=min_sup, minAllConf=min_all_conf_count, sep=separator)
    obj.mine()

    # Save the patterns
    obj.save(output_file)

    frequent_patterns_df = obj.getPatternsAsDataFrame()
    print('Total No of patterns: ' + str(len(frequent_patterns_df)))
    print('Runtime: ' + str(obj.getRuntime()))
    print('Memory (RSS): ' + str(obj.getMemoryRSS()))
    print('Memory (USS): ' + str(obj.getMemoryUSS()))

    return frequent_patterns_df

def process_data(input_file, separator, min_all_conf_count, min_sup_count_list):
    result = pd.DataFrame(columns=['algorithm', 'minSup', 'minAllConf', 'patterns', 'runtime', 'memory'])
    
    for min_sup_count in min_sup_count_list:
        obj = alg.CoMinePlus(input_file, minSup=min_sup_count, minAllConf=min_all_conf_count, sep=separator)
        obj.mine()
        
        result.loc[result.shape[0]] = [
            'CoMinePlus',
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
    
    # Analyze database and plot distributions
    db_stats_obj = analyze_database(input_file, separator)
    output_dir = os.path.join('src', 'GRAPHS')
    plot_distributions(db_stats_obj, output_dir)
    
    # Mine patterns and save them
    frequent_patterns_df = mine_patterns(input_file, separator, min_sup=100, min_all_conf_count=min_all_conf_count, output_file='correlatedPatternsAtMinSupCount100.txt')
    
    # Process data for different minimum support counts and plot results
    result = process_data(input_file, separator, min_all_conf_count, min_sup_count_list)
    print(result)
    plot_results(result, output_dir)
