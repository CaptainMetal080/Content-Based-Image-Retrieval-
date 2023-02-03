import pygame  # import pygame for image processing
import timeit
import sys

run = True

input_number = input("Enter the Number (0-9): ")
input_iteration_str = input("Enter the Iteration (0-9): ")
input_iteration = int(input_iteration_str)

window = pygame.display.set_mode((1200, 600))  # create and display a window that is 1800*900
start = timeit.default_timer()


class Number:  # class Number holds the definitions needed to turn image of the numbers into barcodes
    def __init__(self, image_list):
        self.barcode_array = []  # will hold the barcodes for a number
        self.image_list = image_list  # holds the images from the library
        self.list_of_color_array = []
        for n, image in enumerate(image_list):  # ---
            self.color_array = []  # -
            for i in range(28):  # -
                self.color_array.append(
                    [])  # ---> will take images and make an array of 10*10 squares from the gray-scale values
                for j in range(28):  # -
                    rectangle = pygame.Rect((j * 10, i * 10), (10, 10))  # -
                    color = pygame.transform.average_color(self.image_list[n], rectangle)  # -
                    self.color_array[-1].append(color[0])  # ---

            self.list_of_color_array.append(self.color_array)

    def c1(self, array_index):  # creates c1
        sum_list = []  # creates empty array
        for row in self.list_of_color_array[array_index]:  # Increments list_of_color_array and sets value as row
            val_sum = 0
            sum_list.append(None)
            for val in row:  # Sets Val as incremented row values
                val_sum += val  # Sets val_sum equal to val and add val each time it iterates
                sum_list[-1] = val_sum  # Sets last element in sum_list to val_sum

        return self.generate_c(sum_list)  # Sends sum_list to generate_c and returns that value

    def c2(self, array_index):
        sum_list = []
        for i in range(28):  # Sets i as a number incremented from 0 to 28
            val_sum = 0
            sum_list.append(None)
            for j, row in enumerate(self.list_of_color_array[array_index]):  # For loop to get diagonal values
                # from the main diagonal and up
                if i - j < 0:
                    break
                val_sum += row[i - j]  # Sets val_sum as row array value of i - j
                sum_list[-1] = val_sum  # Sets last element in sum_list as val_sum

        for k, i in enumerate(range(27)[::-1]):  # For loop to get diagonal values under the main diagonal
            val_sum = 0
            sum_list.append(None)
            temporary_list = self.list_of_color_array[array_index][k + 1:-1]  # Assigns temporary_list to lower triangle of list_of_color_array
            for j, row in enumerate(temporary_list):  # Increments temporary_list and j, and sets row as the value
                # of temporary_list
                if i - j < 0:
                    break
                val_sum += row[i - j]  # Sets val_sum as row array value of i - j
                sum_list[-1] = val_sum  # Sets last element in sum_list as val_sum

        sum_list = sum_list[11:45]
        return self.generate_c(sum_list)  # Sends sum_list to generate_c and returns that value

    def c3(self, array_index):
        sum_list = []  # Creates empty array
        for i in range(28):
            val_sum = 0
            sum_list.append(None)
            for row in self.list_of_color_array[array_index]:  # Increments list_of_color_array and sets value as row
                val_sum += row[i]  # Sets val_sum as row array value of i
                sum_list[-1] = val_sum  # Sets last element in sum_list to val_sum
        return self.generate_c(sum_list)  # Sends sum_list to generate_c and returns that value

    def c4(self, array_index):
        sum_list = []
        for i in range(28)[::-1]:  # Sets i as a integer from 28 to 0 (reversed going from the bottom most row to top)
            val_sum = 0
            sum_list.append(None)
            for j, row in enumerate(self.list_of_color_array[array_index]):  # For loop to get diagonal values
                # from the main diagonal and up
                if i + j > 27:
                    break
                val_sum += row[i + j]  # Sets val_sum as row array value of i + j
                sum_list[-1] = val_sum  # Sets last element in sum_list as val_sum

        for k, i in enumerate(range(28)):  # For loop to get diagonal values under the main diagonal
            val_sum = 0
            sum_list.append(None)
            temporary_list = self.list_of_color_array[array_index][k + 1:-1]  # Assigns temporary_list to lower
            # triangle of list_of_color_array
            for j, row in enumerate(temporary_list):  # Increments temporary_list and j, and sets row as the value
                # of temporary_list
                if i + j > 27:
                    break
                val_sum += row[i + j]  # Sets val_sum as row array value of i + j
                sum_list[-1] = val_sum  # Sets last element in sum_list as val_sum

        sum_list = sum_list[11:45]  # Gets rid of extra unnecessary zero's on the edges of the image
        return self.generate_c(sum_list)  # Sends sum_list to generate_c and returns that value

    def generate_barcodes(self):
        for array in range(len(self.list_of_color_array)):
            barcode = [self.c1(array), self.c2(array), self.c3(array),
                       self.c4(array)]  # Strings c1, c2, c3, c4 together
            self.barcode_array.append(barcode)  # Inputs barcode into the barcode array

    @staticmethod
    def generate_c(sum_list):
        sum_val = 0
        for val in sum_list:  # For loop to find the average of the rgb values
            sum_val += val
        average_val = sum_val / len(sum_list)
        for x, val in enumerate(sum_list):
            if val > average_val:  # If the value of val is greater than the average rgb values, it will input 1
                sum_list[x] = 1
            else:  # Else it will input 0
                sum_list[x] = 0

        return sum_list


def generate_images(number):
    img_array = []
    for iteration in range(10):  # Iterates through 10 images in each individual file
        img = pygame.image.load("{}/img_{}.jpg".format(number, iteration))
        img = pygame.transform.scale(img, (280, 280))
        img_array.append(img)  # Inserts the scaled image to img_array

    return img_array


zero_array = generate_images(0)  # Iterates through the 10 images in file 0
zero = Number(zero_array)  # Goes through creating c1, c2, c3, c4
zero.generate_barcodes()  # Strings c1, c2, c3, c4 together to create barcode for 0

one_array = generate_images(1)  # Iterates through the 10 images in file 1
one = Number(one_array)  # Goes through creating c1, c2, c3, c4
one.generate_barcodes()  # Strings c1, c2, c3, c4 together to create barcode for 1

two_array = generate_images(2)  # Iterates through the 10 images in file 2
two = Number(two_array)  # Goes through creating c1, c2, c3, c4
two.generate_barcodes()  # Strings c1, c2, c3, c4 together to create barcode for 2

three_array = generate_images(3)  # Iterates through the 10 images in file 3
three = Number(three_array)  # Goes through creating c1, c2, c3, c4
three.generate_barcodes()  # Strings c1, c2, c3, c4 together to create barcode for 3

four_array = generate_images(4)  # Iterates through the 10 images in file 4
four = Number(four_array)  # Goes through creating c1, c2, c3, c4
four.generate_barcodes()  # Strings c1, c2, c3, c4 together to create barcode for 4

five_array = generate_images(5)  # Iterates through the 10 images in file 5
five = Number(five_array)  # Goes through creating c1, c2, c3, c4
five.generate_barcodes()  # Strings c1, c2, c3, c4 together to create barcode for 5

six_array = generate_images(6)  # Iterates through the 10 images in file 6
six = Number(six_array)  # Goes through creating c1, c2, c3, c4
six.generate_barcodes()  # Strings c1, c2, c3, c4 together to create barcode for 6

seven_array = generate_images(7)  # Iterates through the 10 images in file 7
seven = Number(seven_array)  # Goes through creating c1, c2, c3, c4
seven.generate_barcodes()  # Strings c1, c2, c3, c4 together to create barcode for 7

eight_array = generate_images(8)  # Iterates through the 10 images in file 8
eight = Number(eight_array)  # Goes through creating c1, c2, c3, c4
eight.generate_barcodes()  # Strings c1, c2, c3, c4 together to create barcode for 8

nine_array = generate_images(9)  # Iterates through the 10 images in file 9
nine = Number(nine_array)  # Goes through creating c1, c2, c3, c4
nine.generate_barcodes()  # Strings c1, c2, c3, c4 together to create barcode for 9

test_image = pygame.image.load("{}/img_{}.jpg".format(input_number, input_iteration_str))  # Gets user input
test_image = pygame.transform.scale(test_image, (280, 280))  # Scales user image
test_array = [test_image]  # Puts user image into test_array
test = Number(test_array)  # Goes through creating c1, c2, c3, c4

if input_number == "0":
    for j, c in enumerate(zero.barcode_array[0]):
        for z, bit in enumerate(c):
            zero.barcode_array[input_iteration][j][z] = 0  # Makes the barcode the user chose void in the search library
if input_number == "1":
    for j, c in enumerate(one.barcode_array[0]):
        for z, bit in enumerate(c):
            one.barcode_array[input_iteration][j][z] = 0  # Makes the barcode the user chose void in the search library
if input_number == "2":
    for j, c in enumerate(two.barcode_array[0]):
        for z, bit in enumerate(c):
            two.barcode_array[input_iteration][j][z] = 0  # Makes the barcode the user chose void in the search library
if input_number == "3":
    for j, c in enumerate(three.barcode_array[0]):
        for z, bit in enumerate(c):
            three.barcode_array[input_iteration][j][
                z] = 0  # Makes the barcode the user chose void in the search library
if input_number == "4":
    for j, c in enumerate(four.barcode_array[0]):
        for z, bit in enumerate(c):
            four.barcode_array[input_iteration][j][z] = 0  # Makes the barcode the user chose void in the search library
if input_number == "5":
    for j, c in enumerate(five.barcode_array[0]):
        for z, bit in enumerate(c):
            five.barcode_array[input_iteration][j][z] = 0  # Makes the barcode the user chose void in the search library
if input_number == "6":
    for j in range(4):
        for j, c in enumerate(six.barcode_array[0]):
            for z, bit in enumerate(c):
                six.barcode_array[input_iteration][j][
                    z] = 0  # Makes the barcode the user chose void in the search library
if input_number == "7":
    for j in range(4):
        for j, c in enumerate(seven.barcode_array[0]):
            for z, bit in enumerate(c):
                seven.barcode_array[input_iteration][j][
                    z] = 0  # Makes the barcode the user chose void in the search library
if input_number == "8":
    for j, c in enumerate(eight.barcode_array[0]):
        for z, bit in enumerate(c):
            eight.barcode_array[input_iteration][j][
                z] = 0  # Makes the barcode the user chose void in the search library
if input_number == "9":
    for j, c in enumerate(nine.barcode_array[0]):
        for z, bit in enumerate(c):
            nine.barcode_array[input_iteration][j][z] = 0  # Makes the barcode the user chose void in the search library

test.generate_barcodes()  # Generates the barcode for the user's image


def search_barcodes():
    count_zero = []  # Creates a blank array
    count_one = []  # Creates a blank array
    count_two = []  # Creates a blank array
    count_three = []  # Creates a blank array
    count_four = []  # Creates a blank array
    count_five = []  # Creates a blank array
    count_six = []  # Creates a blank array
    count_seven = []  # Creates a blank array
    count_eight = []  # Creates a blank array
    count_nine = []  # Creates a blank array

    for i in range(10):
        bit_zero = 0
        bit_one = 0
        bit_two = 0
        bit_three = 0
        bit_four = 0
        bit_five = 0
        bit_six = 0
        bit_seven = 0
        bit_eight = 0
        bit_nine = 0

        for j, c in enumerate(test.barcode_array[0]):   # For loop to iterate test.barcode_array, increment j and set c
            # as test.barcode_array value
            for z, bit in enumerate(c):    # For loop to iterate through c, increment z and set bit as c value
                if zero.barcode_array[i][j][z] != bit:
                    bit_zero += 1   # If the bit does not equal to the user's image barcode, 1 is incremented to bit_zero
                if one.barcode_array[i][j][z] != bit:
                    bit_one += 1    # If the bit does not equal to the user's image barcode, 1 is incremented to bit_one
                if two.barcode_array[i][j][z] != bit:
                    bit_two += 1    # If the bit does not equal to the user's image barcode, 1 is incremented to bit_two
                if three.barcode_array[i][j][z] != bit:
                    bit_three += 1  # If the bit does not equal to the user's image barcode, 1 is incremented to bit_three
                if four.barcode_array[i][j][z] != bit:
                    bit_four += 1   # If the bit does not equal to the user's image barcode, 1 is incremented to bit_four
                if five.barcode_array[i][j][z] != bit:
                    bit_five += 1   # If the bit does not equal to the user's image barcode, 1 is incremented to bit_five
                if six.barcode_array[i][j][z] != bit:
                    bit_six += 1    # If the bit does not equal to the user's image barcode, 1 is incremented to bit_six
                if seven.barcode_array[i][j][z] != bit:
                    bit_seven += 1  # If the bit does not equal to the user's image barcode, 1 is incremented to bit_seven
                if eight.barcode_array[i][j][z] != bit:
                    bit_eight += 1  # If the bit does not equal to the user's image barcode, 1 is incremented to bit_eight
                if nine.barcode_array[i][j][z] != bit:
                    bit_nine += 1   # If the bit does not equal to the user's image barcode, 1 is incremented to bit_nine
            count_zero.append(bit_zero)    # Adds the final values of bit_zero to count_zero array
            count_one.append(bit_one)   # Adds the final values of bit_one to count_one array
            count_two.append(bit_two)   # Adds the final values of bit_two to count_two array
            count_three.append(bit_three)   # Adds the final values of bit_three to count_three array
            count_four.append(bit_four)    # Adds the final values of bit_four to count_four array
            count_five.append(bit_five)    # Adds the final values of bit_five to count_five
            count_six.append(bit_six)   # Adds the final values of bit_six to count_six
            count_seven.append(bit_seven)   # Adds the final values of bit_seven to count_seven
            count_eight.append(bit_eight)   # Adds the final values of bit_eight to count_eight
            count_nine.append(bit_nine)    # Adds the final values of bit_nine to count_nine

    counter_zero = []
    chunked_zero = list()
    chunk_size = 4
    for i in range(0, len(count_zero), chunk_size):
        chunked_zero.append(count_zero[i:i + chunk_size])   # Chunks the count_zero together for final hit results
    for i in range(9):
        sum = 0
        for j in range(4):
            sum += (chunked_zero[i][j])    # Sets the array values to an integer
        counter_zero.append(sum)    # Sets sum to a 1D array

    counter_one = []
    chunked_one = list()
    for i in range(0, len(count_one), chunk_size):
        chunked_one.append(count_one[i:i + chunk_size])    # Chunks the count_one together for final hit results
    for i in range(9):
        sum = 0
        for j in range(4):
            sum += (chunked_one[i][j])  # Sets the array values to an integer
        counter_one.append(sum)    # Sets sum to a 1D array

    counter_two = []
    chunked_two = list()
    for i in range(0, len(count_two), chunk_size):
        chunked_two.append(count_two[i:i + chunk_size])    # Chunks the count_two together for final hit results
    for i in range(9):
        sum = 0
        for j in range(4):
            sum += (chunked_two[i][j])  # Sets the array values to an integer
        counter_two.append(sum)    # Sets the array values to an integer

    counter_three = []
    chunked_three = list()
    for i in range(0, len(count_three), chunk_size):
        chunked_three.append(count_three[i:i + chunk_size])    # Chunks the count_three together for final hit results
    for i in range(9):
        sum = 0
        for j in range(4):
            sum += (chunked_three[i][j])    # Sets the array values to an integer
        counter_three.append(sum)   # Sets the array values to an integer

    counter_four = []
    chunked_four = list()
    for i in range(0, len(count_four), chunk_size):
        chunked_four.append(count_four[i:i + chunk_size])   # Chunks the count_four together for final hit results
    for i in range(9):
        sum = 0
        for j in range(4):
            sum += (chunked_four[i][j])    # Sets the array values to an integer
        counter_four.append(sum)    # Sets the array values to an integer

    counter_five = []
    chunked_five = list()
    chunk_size = 4
    for i in range(0, len(count_five), chunk_size):
        chunked_five.append(count_five[i:i + chunk_size])   # Chunks the count_five together for final hit results
    for i in range(9):
        sum = 0
        for j in range(4):
            sum += (chunked_five[i][j])    # Sets the array values to an integer
        counter_five.append(sum)    # Sets the array values to an integer

    counter_six = []
    chunked_six = list()
    chunk_size = 4
    for i in range(0, len(count_six), chunk_size):
        chunked_six.append(count_six[i:i + chunk_size])    # Chunks the count_six together for final hit results
    for i in range(9):
        sum = 0
        for j in range(4):
            sum += (chunked_six[i][j])  # Sets the array values to an integer
        counter_six.append(sum)    # Sets the array values to an integer

    counter_seven = []
    chunked_seven = list()
    chunk_size = 4
    for i in range(0, len(count_seven), chunk_size):
        chunked_seven.append(count_seven[i:i + chunk_size])    # Chunks the count_seven together for final hit results
    for i in range(9):
        sum = 0
        for j in range(4):
            sum += (chunked_seven[i][j])    # Sets the array values to an integer
        counter_seven.append(sum)   # Sets the array values to an integer

    counter_eight = []
    chunked_eight = list()
    chunk_size = 4
    for i in range(0, len(count_eight), chunk_size):
        chunked_eight.append(count_eight[i:i + chunk_size])    # Chunks the count_eight together for final hit results
    for i in range(9):
        sum = 0
        for j in range(4):
            sum += (chunked_eight[i][j])    # Sets the array values to an integer
        counter_eight.append(sum)   # Sets the array values to an integer

    counter_nine = []
    chunked_nine = list()
    chunk_size = 4
    for i in range(0, len(count_nine), chunk_size):
        chunked_nine.append(count_nine[i:i + chunk_size])   # Chunks the count_nine together for final hit results
    for i in range(9):
        sum = 0
        for j in range(4):
            sum += (chunked_nine[i][j])    # Sets the array values to an integer
        counter_nine.append(sum)   # Sets the array values to an integer

    count_list = [min(counter_zero), min(counter_one), min(counter_two), min(counter_three), min(counter_four),
                  min(counter_five), min(counter_six), min(counter_seven), min(counter_eight), min(counter_nine)]
    # Finds the minimum hamming distance for each number and puts it in an array

    accuracy = 100 - (min(count_list) / 1520) * 100  # Finds accuracy percentage
    global found_value
    found_value = count_list.index(min(count_list))    # Finds the minimum hamming distance

    global found_iteration
    found_iteration = 0

    if found_value == 0: found_iteration = counter_zero.index(min(counter_zero))    # Finds iteration number if found_value = 0
    if found_value == 1: found_iteration = counter_one.index(min(counter_one))    # Finds iteration number if found_value = 1
    if found_value == 2: found_iteration = counter_two.index(min(counter_two))    # Finds iteration number if found_value = 2
    if found_value == 3: found_iteration = counter_three.index(min(counter_three))    # Finds iteration number if found_value = 3
    if found_value == 4: found_iteration = counter_four.index(min(counter_four))    # Finds iteration number if found_value = 4
    if found_value == 5: found_iteration = counter_five.index(min(counter_five))    # Finds iteration number if found_value = 5
    if found_value == 6: found_iteration = counter_six.index(min(counter_six))    # Finds iteration number if found_value = 6
    if found_value == 7: found_iteration = counter_seven.index(min(counter_seven))    # Finds iteration number if found_value = 7
    if found_value == 8: found_iteration = counter_eight.index(min(counter_eight))    # Finds iteration number if found_value = 8
    if found_value == 9: found_iteration = counter_nine.index(min(counter_nine))    # Finds iteration number if found_value = 9
    end = timeit.default_timer()

    return "The number is {} with {:.3f}% accuracy, the list of differences are as follows :{} \nIt took {} seconds " \
           "to get this result".format(found_value, accuracy, count_list, end - start)  # Prints the found number,
    # accuracy, hits and time it took to get result


print(search_barcodes())

test_image = pygame.transform.scale(test_image, (600, 600))    # Scales the user selected image to 900 x 900
found_image = pygame.image.load("{}/img_{}.jpg".format(found_value, found_iteration))   # Finds the closest image file
# and iteration
found_image = pygame.transform.scale(found_image, (600, 600))   # Scales closest image to 900 x 900
while True:
    window.fill((0, 0, 0))     # Fills pygame window
    window.blit(test_image, (0, 0))    # shows our input image on the right side of the display
    window.blit(found_image, (600, 0))  # shows our input image on the left side of the display
    pygame.display.update()  # Updates pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Stops pygame window if X is clicked
            pygame.quit()   # Stops pygame loop
            sys.exit()  # Terminates program
