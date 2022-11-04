import cv2 as cv
import numpy as np
import environment

def make_map(row,column):


    dimension = (column,row)
    map_img_original = cv.imread("map/01.png")
    map_img = cv.resize(map_img_original, dimension)

    map_table = environment.generate_grid(dimension[1],dimension[0],fill_element="1")
    for column in range(dimension[1]):
        for row in range(dimension[0]):
            r,g,b = map_img[column][row]
            if r>200 and g>200 and b>200:
                map_table[column][row] = 1
            elif r<50 and g<50 and b<50:
                map_table[column][row] = 0
            elif r>200 and g<50 and b<50:
                destination_state = [column,row]
                # map_table[column][row] = "D"
            elif r<50 and g<50 and b>200:
                start_state = [column, row]
                # map_table[column][row] = "S"





    map_table_np = np.array(map_table)
    np.save('map_table.npy',map_table_np)

    start_state_np = np.array(start_state)
    np.save('start_state.npy',start_state_np)

    destination_state_np = np.array(destination_state)
    np.save('destination_state.npy',destination_state_np)

    environment.display(map_table)
    print("start_state:",start_state,"\ndestination_state:",destination_state)


    # cv.imshow('map_img', map_img_original)
    # cv.waitKey(0)
if __name__ == "__main__":
    make_map(10,10)