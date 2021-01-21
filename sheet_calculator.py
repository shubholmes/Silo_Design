import numpy as np
from math import sqrt
from length_calculator import lengths

def rectangle(area_dimension, standard_plate_dimension):
    offcuts = []

    plate_dim = np.array(standard_plate_dimension)
    plate_length = plate_dim.max()
    plate_breadth = plate_dim.min()
    
    area = np.array(area_dimension)
        
    if area.max() % plate_length == 0:
        area_length = area.max()
        area_breadth = area.min()

    elif area.min() % plate_length == 0:
        area_length = area.min()
        area_breadth = area.max()

    elif area.max() % plate_breadth == 0:
        area_length = area.min()
        area_breadth = area.max()

    elif area.min() % plate_breadth == 0:
        area_length = area.max()
        area_breadth = area.min()    
    
    elif (plate_length - (area.max() % plate_length)) >= (area.min() % plate_breadth):
        area_length = area.max()
        area_breadth = area.min()

    elif (plate_length - (area.min() % plate_length)) >= (area.max() % plate_breadth):
        area_length = area.min()
        area_breadth = area.max()
    else:
        area_length = area.max()
        area_breadth = area.min()

    
    length_remains = np.array([])
    breadth_remains = np.array([])
    
    length_offcuts = np.array([])
    breadth_offcuts = np.array([])

    count = 0
    
    # Determines whole plates, remainders and offcuts
    major_length_number = int(area_length // plate_length)
    length_remain = area_length % plate_length
    if major_length_number == 0:
        major_length_number += 1
        length_remain = 0
        length_offcut = plate_length - area_length
    elif major_length_number > 0 and length_remain == 0:
        length_offcut = 0
    else:
        length_offcut = plate_length - length_remain
    

    major_breadth_number = int(area_breadth // plate_breadth)
    breadth_remain = area_breadth % plate_breadth
    if major_breadth_number == 0:
        major_breadth_number += 1
        breadth_remain = 0
        breadth_offcut = plate_breadth - area_breadth
    elif major_breadth_number and breadth_remain == 0:
        breadth_offcut = 0
    else:
        breadth_offcut = plate_breadth - breadth_remain
  

    options = np.array([length_offcut, breadth_offcut])
    choice = options.max()
    
    if choice == length_offcut:
        if length_remain == 0:
            if length_offcut != 0:
              length_offcuts = np.append(length_offcuts, length_offcut)
              
        if length_remain > 0 and major_breadth_number == 1:
            count += 1
            length_offcuts = np.append(length_offcuts, length_offcut)
            
        elif length_remain > 0 and major_breadth_number > 1:
            for i in range(major_breadth_number):
                length_remains = np.append(length_remains, length_remain)
            if length_offcut // length_remain >= len(length_remains):
                count += 1
                offcut = length_offcut % length_remain
                length_offcuts = np.append(length_offcuts, offcut)
            else:
                count_, result_offcuts = lengths(length_remains, plate_length)
                count = count_ // (plate_length // length_remain)
                if count_ % (plate_length // length_remain) > 0:
                    count += 1
                if len(result_offcuts) > 0:
                    for offcut in result_offcuts:
                        length_offcuts = np.append(length_offcuts, offcut)
                        

        if breadth_remain == 0:
            new_count = 0
            if breadth_offcut != 0:
                breadth_offcuts = np.append(breadth_offcuts, breadth_offcut)
        else:
            for i in range(major_length_number):
                breadth_remains = np.append(breadth_remains, breadth_remain)

            if len(length_offcuts) > 0:
                lst = length_offcuts[length_offcuts >= breadth_remain]
                lst_ = len(lst) // 2
                if len(breadth_remains) >= lst_:
                    for i in range(lst_):
                        breadth_remains = np.delete(breadth_remains, -1)
                        length_offcuts = np.delete(length_offcuts, -1)
                        length_offcuts = np.delete(length_offcuts, -1)
                    if length_offcut - breadth_remain > 0:
                        for i in range(len(breadth_remains)):
                            length_offcuts = np.append(length_offcuts, length_offcut - breadth_remain)
                            length_offcuts = np.append(length_offcuts, length_offcut - breadth_remain)
                            
                elif len(breadth_remains) < lst_:
                    breadth_remains = np.array([])
                    for i in range(len(breadth_remains)):
                        length_offcuts = np.delete(length_offcuts, -1)
                        length_offcuts = np.delete(length_offcuts, -1)
                    if length_offcut - breadth_remain > 0:
                        for i in range(len(breadth_remains)):
                            length_offcuts = np.append(length_offcuts, length_offcut - breadth_remain)
                            length_offcuts = np.append(length_offcuts, length_offcut - breadth_remain)
            
            if len(breadth_remains) > 0:
                new_count_, result_offcuts = lengths(breadth_remains, plate_breadth)
                new_count = new_count_ // (plate_breadth // breadth_remain)
                if new_count_ % (plate_breadth // breadth_remain) > 0:
                    new_count += 1
                if len(result_offcuts) > 0:
                    for offcut in result_offcuts:
                        breadth_offcuts = np.append(breadth_offcuts, offcut)
        small_cut = False            
            
    else :
        if breadth_remain == 0:
            if breadth_offcut != 0:
                breadth_offcuts = np.append(breadth_offcuts, breadth_offcut)
        
        if breadth_remain > 0 and major_length_number == 1:
            count += 1
            breadth_offcuts = np.append(breadth_offcuts, breadth_offcut)
            
        elif breadth_remain > 0 and major_length_number > 1:
            for i in range(major_length_number):
                breadth_remains = np.append(breadth_remains, breadth_remain)
            if breadth_offcut // breadth_remain >= len(breadth_remains):
                count += 1
                offcut = breadth_offcut % breadth_remain
                breadth_offcuts = np.append(breadth_offcuts, offcut)
            else:
                count_, result_offcuts = lengths(breadth_remains, plate_breadth)
                count = count_ // (plate_breadth // breadth_remain)
                if count_ % (plate_breadth // breadth_remain) > 0:
                    count += 1
                if len(result_offcuts) > 0:
                    for offcut in result_offcuts:
                        breadth_offcuts = np.append(breadth_offcuts, offcut)
            

        if length_remain == 0:
            new_count = 0
            if length_offcut != 0:
              length_offcuts = np.append(length_offcuts, length_offcut)
            small_cut = False
        else:
            for i in range(major_breadth_number):
                length_remains = np.append(length_remains, length_remain)

            if len(breadth_offcuts) > 0:
                lst = breadth_offcuts[breadth_offcuts >= length_remain]
                lst_ = len(lst) * 2
                
                if len(length_remains) >= lst_: 
                    for i in range(lst_):
                        length_remains = np.delete(length_remains, -1) 
                        breadth_offcuts = np.delete(breadth_offcuts, -1)
                    
                    if breadth_offcut - length_remain > 0:
                        for i in range(len(lst_ // 2)):
                            breadth_offcuts = np.append(breadth_offcuts, breadth_offcut - length_remain)

                elif len(length_remains) < lst_:
                    length_remains = np.array([])
                    for i in range(len(length_remains) // 2):
                        breadth_offcuts = np.delete(breadth_offcuts, -1)
                    if len(lst) % 2 > 0:
                        breadth_offcuts = np.delete(breadth_offcuts, -1)
                        
                    if breadth_offcut - length_remain > 0:
                        for i in range(len(length_remains) // 2):
                            breadth_offcuts = np.append(breadth_offcuts, breadth_offcut - length_remain)

                if len(lst) % 2 > 0:
                    small_cut = True
                    small_cut1 = [round(plate_length / 2, 2), breadth_offcut].sort(reverse=True)
                    small_cut1 = f'[{small_cut1[0]} x {small_cut1[1]}]'
                    small_cut2 = [round(plate_length / 2, 2), breadth_offcut - length_remain].sort(reverse=True)
                    small_cut2 = f'[{small_cut2[0]} x {small_cut2[1]}]'
                   
                else:
                    small_cut = False
                           
            if len(length_remains) > 0:
                new_count_, result_offcuts = lengths(length_remains, plate_length)
                new_count = new_count_ // (plate_length // length_remain)
                if new_count_ % (plate_length // length_remain) > 0:
                    new_count += 1
                if len(result_offcuts) > 0:
                    for offcut in result_offcuts:
                        length_offcuts = np.append(length_offcuts, offcut)

    if length_remain > 0 and breadth_remain > 0:
        extra_dim = [length_remain, breadth_remain]
        extra_offcuts_length = []
        extra_offcuts_breadth = []
        
        for i in length_offcuts:
            extra_off_length = extra_offcuts_length.append([round(i, 2), plate_breadth])
        for i in breadth_offcuts:
            extra_off_breadth = extra_offcuts_breadth.append([plate_breadth, round(i, 2)])

        extra_list = np.concatenate([extra_offcuts_length, extra_offcuts_breadth])
        new_lst = []
        for i in extra_list:
            if extra_dim[0] <= i[0]:
                if extra_dim[1] <= i[1]:
                    new_lst.append(i)
                    if len(new_lst) == 1:
                        
                        break
            if extra_dim[1] <= i[0]:
                if extra_dim[0] <= i[1]:
                    new_lst.append(i)
                    if len(new_lst) == 1:
                        break
        if len(new_lst) > 0:
            extra = 0
        else:
            extra = 1
    else:
        extra = 0
   
    Length_offcuts = []
    Breadth_offcuts = []
        
    for i in length_offcuts:
        if i > 0:
            off_length = f'{round(i, 2)} x {plate_breadth}'
            Length_offcuts.append(off_length)
    for i in breadth_offcuts:
        if i > 0:
            off_breadth = f'{plate_length} x {round(i, 2)}'
            Breadth_offcuts.append(off_breadth)

    if small_cut == True:    
        Breadth_offcuts = np.append(Breadth_offcuts, small_cut1)
        Breadth_offcuts = np.append(Breadth_offcuts, small_cut2)
        
    Offcuts = Length_offcuts + Breadth_offcuts
    OFfcuts, COunts = np.unique(np.array(Offcuts), return_counts=True)
                    
    return int((major_length_number * major_breadth_number) + count + new_count + extra), tuple(zip(COunts, OFfcuts))



def cone(big_diameter, small_diameter, height, plate_dimension):
    # height is truncated cone height
    # h is small cone height
    # r is small cone height
    # H is big cone height
    # R is big cone radius

    Ht = height
    R  = big_diameter / 2
    r  = small_diameter / 2
    h  = (r * Ht) / (R-r)

    # L is big cone slant height

    L = sqrt((h + Ht)**2 + R**2)

    Diameter = 2*L

    side0, offcut0 = lengths([Diameter], plate_dimension[0])
    side1, offcut1 = lengths([Diameter], plate_dimension[1])

    plates  = side0 * side1
    offcut0 = f'{round(offcut0[0], 2)} x {plate_dimension[0]}'
    offcut1 = f'{round(offcut1[0], 2)} x {plate_dimension[1]}'
    offcuts = (offcut0, offcut1)

    return plates, offcuts

    
    
    
   
    
