import matplotlib.pyplot as plt
import csv

def plot_session_data(file_path):
    # Read data from CSV file
    time_data = []
    cheat_probability_data = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            time_data.append(int(row[0]))
            cheat_probability_data.append(float(row[1]))

    # Plot the data
    plt.plot(time_data, cheat_probability_data)
    plt.title("Session Data")
    plt.xlabel("Time")
    plt.ylabel("Cheat Probability")
    plt.grid(True)

    # Save the plot as an image file
    plt.savefig("session_1_plot.png")
    plt.show()

if __name__ == "__main__":
    plot_session_data("session_1_data.csv")
