import matplotlib.pyplot as plt
import numpy as np
import csv
import time
import audio
import headpose
import keyboard

PLOT_LENGTH = 200

GLOBAL_CHEAT = 0
PERCENTAGE_CHEAT = 0
CHEAT_THRESH = 0.6
XDATA = list(range(200))
YDATA = [0]*200

def avg(current, previous):
    if previous > 1:
        return 0.65
    if current == 0:
        if previous < 0.01:
            return 0.01
        return previous / 1.01
    if previous == 0:
        return current
    return 1 * previous + 0.1 * current

def process():
    global GLOBAL_CHEAT, PERCENTAGE_CHEAT
    if GLOBAL_CHEAT == 0:
        if headpose.X_AXIS_CHEAT == 0:
            if headpose.Y_AXIS_CHEAT == 0:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.2, PERCENTAGE_CHEAT)
            else:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0.2, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.4, PERCENTAGE_CHEAT)
        else:
            if headpose.Y_AXIS_CHEAT == 0:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0.1, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.4, PERCENTAGE_CHEAT)
            else:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0.15, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.25, PERCENTAGE_CHEAT)
    else:
        if headpose.X_AXIS_CHEAT == 0:
            if headpose.Y_AXIS_CHEAT == 0:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.55, PERCENTAGE_CHEAT)
            else:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0.55, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.85, PERCENTAGE_CHEAT)
        else:
            if headpose.Y_AXIS_CHEAT == 0:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0.6, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.85, PERCENTAGE_CHEAT)
            else:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0.5, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.85, PERCENTAGE_CHEAT)

    if PERCENTAGE_CHEAT > CHEAT_THRESH:
        GLOBAL_CHEAT = 1
        print("CHEATING")
    else:
        GLOBAL_CHEAT = 0
    print("Cheat percent: ", PERCENTAGE_CHEAT, GLOBAL_CHEAT)

def save_session_data(session_number, data, cheated):
    with open(f'session_{session_number}_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Cheat Probability'])
        for entry in data:
            writer.writerow(entry)

def save_final_result(session_number, cheated):
    with open('final_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ 'Cheated' if cheated else 'Not Cheated'])

def run_detection():
    global XDATA, YDATA
    plt.show()
    axes = plt.gca()
    axes.set_xlim(0, 200)
    axes.set_ylim(0, 1)
    line, = axes.plot(XDATA, YDATA, 'r-')
    plt.title("Suspicious Behaviour Detection")
    plt.xlabel("Time")
    plt.ylabel("Cheat Probability")
    session_number = 1
    session_data = []
    i = 0
    exceed_count = 0
    iterations_without_cheat = 0
    cheating_occurred = False  # Flag to track if cheating occurred during the session
    while True:
        if keyboard.is_pressed('q'):  # Press 'q' to quit the program
            break

        YDATA.pop(0)
        YDATA.append(PERCENTAGE_CHEAT)
        line.set_xdata(XDATA)
        line.set_ydata(YDATA)
        plt.draw()
        plt.pause(1e-17)
        time.sleep(1/5)
        process()
        session_data.append([i, PERCENTAGE_CHEAT])
        if PERCENTAGE_CHEAT > CHEAT_THRESH:
            exceed_count += 1
            if exceed_count >= 10:
                cheating_occurred = True
        else:
            iterations_without_cheat += 1
                
        if i % PLOT_LENGTH == 0 and i != 0:
            break
        i += 1

    # Write session data to session_data.csv
    save_session_data(session_number, session_data, cheating_occurred)

    if cheating_occurred:
        save_final_result(session_number, True)
    else:
        save_final_result(session_number, False)

    plt.close()  # Close the graph window when the detection is complete


