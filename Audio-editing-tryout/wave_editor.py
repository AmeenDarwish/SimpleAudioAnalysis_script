import numpy as np

import math
from scipy.io import wavfile
import wave_helper
import os
import pathlib
import shutil
import sys

MAX_VOL = 32767
MIN_VOL = 32768
VOL_UP,VOL_DOWN = 1.2
ONE_SIXTEENTHS_PER_SEC = 1 / 16
SAMPLE_RATE = 2000
frequencies = {"A": 440, "B": 494, "C": 523, "D": 587, "E": 659, "F": 698,
               "G": 784, "Q": 0}
List_of_valid_choices1=[1,2,3,4]
List_of_valid_choices=['1','2','3','4','5','6']
List_of_valid_notes = ['A','B','C','E','F','G','Q']


def reverse_sounds(sounds_list):
    return sounds_list[::1]
    #functoin that returns the sound data but reversed

def speed_up(sounds_list):
    #function that speeds up the sound by cutting out the singular indexes
    result_list = []
    for indexes in range(len(sounds_list)):
        if indexes % 2 == 0:
            result_list.append(sounds_list[indexes])
    return result_list


def slow_down(sounds_list):
    #function that slows down the sound by taking the average of every two lists in the data and adding
    #it in between them , making a longer more continues list
    result_list = []
    for list_index in range(len(sounds_list)):
        if list_index + 1 == len(sounds_list):
            result_list.append(sounds_list[1])
            break
        else:
            result_list.append(sounds_list[list_index])
            x = (sounds_list[list_index][0] + sounds_list[list_index + 1][
                0]) / 2
            y = (sounds_list[list_index][1] + sounds_list[list_index + 1][
                1]) / 2
            result_list.append([int(x), int(y)])
    return result_list


def volume_up(sounds_list):
    #the function increases the volume of the sound by multipling all the values in the lists inside
    #the data by 1.2 up to an assigned global maximum
    result_list = []
    for lists in sounds_list:
        temp_list = []
        if lists[0] * VOL_UP > MAX_VOL:

            temp_list.append(MAX_VOL)

        elif lists[0] * VOL_UP < MIN_VOL:

            temp_list.append(MIN_VOL)
        else:
            temp_list.append(int(lists[0] * VOL_UP))

        if lists[1] * VOL_UP > MAX_VOL:
            temp_list.append(MAX_VOL)

        elif lists[1] * VOL_UP < MIN_VOL:

            temp_list.append(MIN_VOL)

        else:
            temp_list.append(int(lists[1] * VOL_UP))

        result_list.append(temp_list)

    return result_list


def volume_down(sounds_list):#the function increases the volume of the sound by multipling all the values in the lists inside
    #the data by 1.2 up to an assigned global minimum
    result_list = []
    for lists in sounds_list:
        temp_list = []
        temp_list.append(int(lists[0] / VOL_DOWN))
        temp_list.append(int(lists[1] / VOL_DOWN))
        result_list.append(temp_list)
    return result_list


def dimming(sounds_list):
    result_list = []
    for lists in range(len(sounds_list)):
        temp_list = []
        temp_list.append(int((sounds_list[0][0] + sounds_list[1][0]) / 2),
                        int((sounds_list[0][1] + sounds_list[1][1]) / 2))
        result_list.append(result_list)
    return result_list

#########
# Part2 #
#########

def helper_merging_audios(sound1, sound2):
    #helper functoin for getting an average of 2 lists from different data files
    #and returning a list of the average values
    left = int((sound1[0] + sound2[0]) / 2)
    right = int((sound1[1] + sound2[1]) / 2)
    return [left, right]

def helper_merging_audios(sound1, sound2):
    """ getting the average of the two sounds (that's how we merge) """
    left = int((sound1[0] + sound2[0]) / 2)
    right = int((sound1[1] + sound2[1]) / 2)
    return [left, right]


def new_audio_rate(file, higher_rate, lower_rate):
    """ making a new audio with same Frame-rate as the lower rate"""
    new_audio = []
    i = 0
    while i < len(file):
        for j in range(int(higher_rate)):
            if j < lower_rate:
                new_audio.append(file[int(i + j)])
                # to avoid index out of list
                if file[i+j] == file[1]:
                    break
        i += higher_rate
    return new_audio


def gcd(x, y):
    """ finding the great common divisor"""
    while y != 0:
        (x, y) = (y, x % y)
    return x


def merging_audios(file1, file2):
    """ it takes two files and merge them into one file on some rules """
    result_list = []
    # dividing frame rate on gcd
    rate1 = int(file1[0])
    rate2 = int(file2[0])
    gc = gcd(rate1, rate2)
    rate1 = int(rate1 / gc)
    rate2 = int(rate2 / gc)
    # finding the higher Frame-rate file
    if rate1 > rate2:
        file1 = (rate2 * gc, new_audio_rate(file1[1], int(rate1), int(rate2)))
    elif rate1 < rate2:
        file2 = (rate1 * gc, new_audio_rate(file2[1], rate2, rate1))
    # finding the shorter file, to iterate over it then over the longer one
    if len(file1[1]) > len(file2[1]):
        for i in range(len(file2[1])):
            result_list.append(helper_merging_audios(file1[1][i], file2[1][i]))

        for i in range(len(file2[1]), len(file1[1])):
            result_list.append(file1[1][i])
    else:
        for i in range(len(file1[1])):
            result_list.append(helper_merging_audios(file1[1][i], file2[1][i]))

        for i in range(len(file1[1]), len(file2[1])):
            result_list.append(file2[1][i])

    return result_list




##########
# part 3 #
##########


def equation(fraction, frequency):
    """ solving the equation of the sample values"""
    samples_per_cycle = SAMPLE_RATE / frequency
    answer = MAX_VOL * math.sin(math.pi * 2 * fraction / samples_per_cycle)
    return [int(answer), int(answer)]


def Tuner(file_melody):
    """ creating an audio for a melody """
    result = []
    # making a list of the file
    melody = file_melody.split()
    # passing over the list, two digits at the time
    for i in range(0, len(melody), 2):
        # getting the frequency for the letter
        frequency = frequencies[melody[i]]
        # calculating the melody long
        time = ONE_SIXTEENTHS_PER_SEC * float(melody[i + 1])
        # solving the equation
        for fraction in range(int(time * SAMPLE_RATE)):
            result.append(equation(fraction, frequency))
    return result

def printer():
    #function that prints options for the programm
    #created to make the programm more readable
    print("Choose an action:")
    print("1. flip the audio")
    print("2. faster the audio by x2")
    print("3. slower the audio by x2")
    print("4. higher the volume by x1.2")
    print("5. lower the volume down x1.2")
    print("6. LOW PASS FILTER")

def user_choice_edit(file_name):
    #function to be used in the main,to be able to make it more readable
    #the function takes a filename as a variable and loads it
    #leaving us the sound data and framerate to use
    #the user is given a choice between six different options
    #if the user doesn't pick a correct option the function will inform the user
    #and ask for a valid choice once again
    while True:
            list_of_sounds = wave_helper.load_wave(file_name)[1]
            current_frame_rate = wave_helper.load_wave(file_name)[0]
            printer()
            second_input = input()
            int_second_input=int(second_input)
            if int_second_input == 1:
                list_of_sounds = reverse_sounds(list_of_sounds)
            elif int_second_input == 2:
                list_of_sounds = speed_up(list_of_sounds)
            elif int_second_input == 3:
                list_of_sounds = slow_down(list_of_sounds)
            elif int_second_input == 4:
                list_of_sounds = volume_up(list_of_sounds)
            elif int_second_input == 5:
                list_of_sounds = volume_down(list_of_sounds)
            elif int_second_input == 6:
                list_of_sounds = dimming(list_of_sounds)

            else:
                second_input = input('choose a valid number')
            last_input=input("Do you want to: 1.Save File or 2.Edit File")
            if last_input is 1:
                new_file = input("Please name your file for saving:")
                wave_helper.save_wave(current_frame_rate,list_of_sounds,new_file)
                sys.exit()

            if last_input is 2:
                continue


def file_path_to_two(path):
    #a helper function to split the given file pathes into two

    while True:

        if ' ' not in path:
            print("Please enter  paths with a space between the two paths")
            continue
        else:
            path1,path2 = path.split(' ',1)
            break
    return path1,path2

def check_file_correct_exists(path):
    #a function that checks if the files exist or not in the directory
    #user in main
    if os.path.isfile(path) == False:
        print("please check if files exist or not and input correct paths:")
        return False
    if wave_helper.load_wave(path) == -1:
        print("Something is wrong with files,please input again:")
        return False


def text_reader(file_path):
    #function that reads the text file and returns the string
    #to be used in the tuner functoin that reads the string
    #and returns a list of sound data
    with open(file_path, 'r') as myfile:
        data = myfile.read()
    return data


print(Tuner(text_reader('sample1.txt')))

def make_wav_from_txt():
    #the optoin allows the user to pick a text including notes for a melody
    #if the file does not exist the option will keep asking the user until valid input is given
    #the file also is saved temporarly and is later changed or saved over
    #this is a helper function for choice 3 in the main and is used only there
    while True:
        note_file_name = input("Please choose a note file:")
        if os.path.isfile(note_file_name) == False:
            print("Please choose an existing file within the directory")
            continue
        else:
            break

    data = text_reader(note_file_name)
    temp_name = 'tuner_temp'

    results_from_notes = Tuner(data)
    wave_helper.save_wave(SAMPLE_RATE,results_from_notes,temp_name)

    last_input_note = int(input("Do you want to: 1.Save File or 2.Edit File"))

    if last_input_note == 1:
        new_file = input("Please name your file for saving:")
        os.rename(temp_name, new_file)
        sys.exit()


    if last_input_note == 2:
        user_choice_edit(temp_name)

def merge_helper_main():
    #if the user picks this option then they will be asked to input the paths of two wav files
    #that he wishes to combine
    #the option uses helper functions and the merging function
    #before doing so the option checks if the files exist or not by using a helper function
    #after merging the sound data using the merge function the optoin checks for the minimum frame rate
    #to be able to save the file using that framerate
    #THIS IS A HELPER FUNCTION USED IN THE MAIN ONLY for readiablity

    while True:
        file_paths = input("Please input file paths:")
        path1,path2= file_path_to_two(file_paths)
        if check_file_correct_exists(path1) == False or check_file_correct_exists(path2) == False:
            continue
    first_file_read = wave_helper.load_wave(path1)

    second_file_read = wave_helper.load_wave(path2)

    first_file_f_rate = first_file_read[0]
    second_file_f_rate = second_file_read[0]

    new_wave = merging_audios(first_file_read, second_file_read)
    current_frame_rate = min(first_file_f_rate,second_file_f_rate)
    temp_file_name = 'merged wave'

    #the function saves the a temporary file with a temp name to be changed later
    #by orders of the ex6 pdf the option has to save before going to the last menu
    wave_helper.save_wave(current_frame_rate,new_wave,temp_file_name)

    last_input_merged=int(input("Do you want to: 1.Save File or 2.Edit File"))

    if last_input_merged == 1:
        new_name = input("Please name your file for saving:")
        #if the user chooses to save then the functoin would just
        #change the temp file name to the user's chosen name
        #and then exit
        os.rename(temp_file_name,new_name)
        sys.exit()

    if last_input_merged == 2:
        #second option takes the user to the editing menu
        user_choice_edit(temp_file_name)

def main():
    #main function starts the entire programm with a loop
    #the user is asked between a list of 4 choices
    #if the user enters invalid input the loop will restart and ask for a valid one
    #if the user picks the fourth option the programm will exit
    while True:

        print("Choose an action:")
        print("1. Change in file WAV")
        print("2. Merge two files WAV")
        print("3. Melody the file WAV")
        print("4. EXIT")
        user_input = int(input())

        if  user_input not in List_of_valid_choices1:
            print('Please Choose a Valid Number:')
            continue

        if int(user_input )== 1:
            #if the user chooses the first option (1)
            #then the function will ask the user for a name and
            #then jump to the helper function that edits the sound data of our choosen file
            while True:
                input_for_file=input("Please Choose File Name:")
                if check_file_correct_exists(input_for_file) == False:
                    continue
            user_choice_edit(input_for_file)


        if int(user_input) == 2:
            #checkout the helper function for details
          merge_helper_main()


        if int(user_input) == 3:
            #checkout the helper function for details
            make_wav_from_txt()


        if int(user_input )== 4:
            sys.exit()



if __name__ == '__main__':
   main()
