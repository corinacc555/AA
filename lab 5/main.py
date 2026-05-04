"""Small CLI to run experiments or plotting."""
import argparse
import experiment
import plot_results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment', action='store_true', help='Run experiments and write results.csv')
    parser.add_argument('--plot', action='store_true', help='Plot results.csv')
    args = parser.parse_args()

    if args.experiment:
        experiment.run_experiments()
    if args.plot:
        plot_results.main() if hasattr(plot_results, 'main') else plot_results.plot(plot_results.load_results())

if __name__ == '__main__':
    main()
