import random
#############################################
########### Random File generator ###########
#############################################
def generate_random_number_file (min_size, max_size, path):
    with open(path, 'w') as f:
        numbers_to_generate = random.randint(min_size*1024*1024/4,
                                             max_size*1024*1024/4)
        for i in range(numbers_to_generate):
            f.write(str(random.randint(-1000, 1000)) + " ")
        #print numbers_to_generate*4/1024/1024
    return numbers_to_generate*4/1024/1024


def generate_files (total_size, min_size, max_size, path):
    counter = 0
    file_id = 1
    while counter < total_size:
        counter += generate_random_number_file(min_size, max_size,
                                               path+"/"+str(file_id)+".dat")
        file_id += 1


# for testing
if __name__ == "__main__" :
    # generate_random_number_file(10, 100, "./test_file.txt")
    generate_files(2000, 10, 100, "./source")
