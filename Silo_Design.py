import sys, shelve, math, os, pathlib
from sheet_calculator import rectangle, cone
from decimal import Decimal


file_name = input('Please enter a name to save your design: ')
file_name_with_ext = file_name + '.txt' # Adds extension .txt
path = str(pathlib.Path(__file__).parent.absolute()) + '\\'
FILE = open(path + file_name_with_ext, 'a')
project = input('Enter name of silo: ')




class CaselessDict(dict):
    """A dictionary sub-class with case-insensitive keys """ #copied this online, I don't understand it

    def __setitem__(self, key, value):
        if isinstance(key, str):
            key = key.casefold()
        super().__setitem__(key, value)

    def __getitem__(self, key):
        if isinstance(key, str):
            key = key.casefold()
        return super().__getitem__(key)


grain_data = {}
grain_data = CaselessDict()
properties = {}
properties = CaselessDict()
 
def store_grain(dbM, grain, dbm):
    dbM[grain] = dbm
    

# Unit Lists
length_units      = ['meters'.casefold(), 'metres'.casefold(), 'm'.casefold(), 'centimeters'.casefold(),
                    'centimetres'.casefold(),'cm'.casefold(), 'millimeters'.casefold(),
                    'millimetres'.casefold(), 'mm'.casefold(), 'inches'.casefold(), 'inch'.casefold(),
                     'in'.casefold(), 'feet'.casefold(), 'foot'.casefold(), 'ft'.casefold()]    # Holds unit of length

bulkdensity_units = ['Kg/m3'.casefold(), 'Kg/cm3'.casefold(),
                    'g/m3'.casefold(), 'g/cm3'.casefold()]     # Holds units of bulk density

mass_units        = ['Tonnes'.casefold(), 'T'.casefold(), 'Kilograms'.casefold(),
                    'kg'.casefold(), 'Grams'.casefold(), 'g'.casefold()]

def float_check(s, txt): # checks parameter and converts to float
    while True:
        try:
            float(s)
        except ValueError:
            print('Invalid Input!')
            s = input(f'{txt}')
        else: break
    return float(s)

def unit_check(s, unit_list, txt): # Checks unit
    while s not in unit_list:
        print('Invalid unit!')
        s = input(f'{txt}').casefold()

def cone_angle(incl_txt): # Collects angle of repose of grain or inclination of cone
    cone_incl = input(f'{incl_txt}') 
    cone_incl = float_check(cone_incl, incl_txt)
    return cone_incl              

def para_conv(para_txt, para_unit_txt): # Collects linear parameter info
    para = input(f'{para_txt}')
    para = float_check(para, para_txt)              
    para_unit = input(f'{para_unit_txt}'.casefold())
    unit_check(para_unit, length_units, para_unit_txt)
    if para_unit in ('millimeters', 'millimetres', 'mm'):
        para = para / 1000
    elif para_unit in ('centimeters', 'centimetres', 'cm'):
        para = para / 100
    elif para_unit in ('inches', 'inch', 'in'):
        para = para / 39.37
    elif para_unit in ('feet', 'foot', 'ft'):
        para = para / 3.281
    else:
        para = para
    return para

def grain_store(grain_name):
    grain_data = shelve.open(path + 'grain_base.dat')
    try:
        return grain_data[grain_name]
    except KeyError:
        print('Grain information not in database')
    grain_data.close()

class Silo():
    def __init__(self):
        grain_data = shelve.open(path + 'grain_base.dat', writeback=True)
        # Processes Capacity
        txt = 'Enter CAPACITY of SILO: '
        cap = input(f'{txt}')
        cap = float_check(cap, txt)
    
        txt = 'Select UNIT of CAPACITY [Tonnes (T), Kilograms (kg), Grams (g)]: '
        cap_unit = input(f'{txt}').casefold()
        unit_check(cap_unit, mass_units, txt)
        global cap_in_kg
        if cap_unit in ('Tonnes'.casefold(), 'T'.casefold()): # Converts to SI unit
            cap_in_kg = cap * 1000
        elif cap_unit in ('Grams'.casefold(), 'g'.casefold()):
            cap_in_kg = cap / 1000
        else:
            cap_in_kg = cap
        self.design_capacity = cap_in_kg / 1000 

        print('\n')
        self.grain = input('Enter NAME of GRAIN: ') # Collects target grain
        FILE.writelines(f'            ******{self.design_capacity:.1f} Tonnes Capacity Silo for {self.grain}******\n')
        FILE.writelines(f'1.  Design Capacity: {self.design_capacity:.1f} Tonnes\n')
        FILE.writelines(f'2.  Grain   : {self.grain}\n')

        
        
        # Receives and Processes Bulk Density
        try:
            if grain_data[self.grain]['bulk density']:
                self.bulk_density = grain_data[self.grain]['bulk density']
        except KeyError: 
            txt = f'Enter BULK DENSITY of {self.grain}: '
            bulkden = input(f'{txt}')
            bulkden = float_check(bulkden, txt)

            txt = 'Enter UNIT of the BULK DENSITY [Kg/m3, Kg/cm3, g/m3, g/cm3]: ' 
            bulkden_unit = input(f'{txt}').casefold()
            unit_check(bulkden_unit, bulkdensity_units,  txt)
            if bulkden_unit == 'g/cm3'.casefold(): # Converts to SI unit
                self.bulk_density = bulkden * 1000
            elif bulkden_unit == 'g/m3'.casefold():
                self.bulk_density = bulkden / 1000
            elif bulkden_unit == 'kg/cm3'.casefold():
                self.bulk_density = bulkden * 1000000
            else:
                self.bulk_density = bulkden
            properties['bulk density'] = self.bulk_density


        FILE.writelines(f'3.  Bulk Density: {self.bulk_density:.1f} Kg/m\u00b3\n')
        FILE.writelines('\n')
        print('\n')


        # Processes Silo bin information
        
        self.bin_volume = cap_in_kg/self.bulk_density # Calculates Silo bin volume
  
        bin_dia_or_height = input('Enter h for BIN HEIGHT or d for BIN DIAMETER: ').casefold()
        # Collects Bin height or diameter  

        while not (bin_dia_or_height == 'h'.casefold() or bin_dia_or_height == 'd'.casefold()):
            print('Invalid input!')
            bin_dia_or_height = input('Enter (h) for BIN HEIGHT or d for BIN DIAMETER: ').casefold()
        
        if bin_dia_or_height == 'h':
            bin_h_txt = 'Enter assumed BIN HEIGHT: ' 
            bin_h_unit_txt = 'Enter UNIT of BIN HEIGHT [m, cm, mm, inches, ft]: '
            self.bin_height = para_conv(bin_h_txt, bin_h_unit_txt)

            self.bin_radius = math.sqrt(self.bin_volume / (math.pi * self.bin_height))
            self.bin_diameter = self.bin_radius * 2
           
        
        if bin_dia_or_height == 'd':
            bin_d_txt = 'Enter assumed BIN DIAMETER: '
            bin_d_unit_txt = 'Enter UNIT of BIN DIAMETER [m, cm, mm, inches, ft]: ' 
            self.bin_diameter = para_conv(bin_d_txt, bin_d_unit_txt)
            
            self.bin_radius = self.bin_diameter / 2
            self.bin_height = self.bin_volume / (math.pi * self.bin_radius**2)
            print('\n')

        self.bin_surface_area = 2 * math.pi * self.bin_radius * self.bin_height
        self.circumference = math.pi * self.bin_diameter 
        FILE.writelines('        ***Silo Bin Information***\n')
        FILE.writelines(f'4.  Bin Height: {self.bin_height:.3f} m\n')
        FILE.writelines(f'5.  Bin Diameter: {self.bin_diameter:.3f} m\n')
        FILE.writelines(f'6.  Bin Circumference: {self.circumference:.3f} m\n')
        FILE.writelines(f'7.  Bin Surface Area: {self.bin_surface_area:.3f} m\u00b2\n')
        FILE.writelines(f'8.  Bin Volume: {self.bin_volume:.3f} m\u00b3\n')
        FILE.writelines('\n')
        

        # Processes  Silo cone information

        def cone_design_1():
            while True:
                cone_para = input('Enter A, B or C: ').casefold()
                while cone_para not in ['A'.casefold(), 'B'.casefold(), 'C'.casefold()]:
                    print('Invalid Input')
                    cone_para = input('Enter A, B or C: ').casefold()

                if cone_para == 'A'.casefold():
                    try:
                        if grain_data[self.grain]['angle of repose']:
                            cone_incl = grain_data[self.grain]['angle of repose']
                            cone_hei  = para_conv(hei_txt, hei_unit_txt)
                            cone_rad  = ((self.bin_radius*math.tan(math.radians(cone_incl))) -
                                        cone_hei) / math.tan(math.radians(cone_incl))
                    except KeyError:
                        cone_incl = cone_angle(incl_txt)
                        cone_hei  = para_conv(hei_txt, hei_unit_txt)
                        cone_rad  = ((self.bin_radius*math.tan(math.radians(cone_incl))) -
                                    cone_hei) / math.tan(math.radians(cone_incl))
                    # Calculates radius of cone opening
                    cone_dia  = 2 * cone_rad
                elif cone_para == 'B'.casefold():
                    try:
                        cone_incl = grain_data[self.grain]['angle of repose']
                        cone_dia    = para_conv(dia_txt, dia_unit_txt)
                        cone_rad    = cone_dia / 2
                        cone_hei = (self.bin_radius - cone_rad) * math.tan(math.radians(cone_incl))
                    except KeyError:
                        cone_incl   = cone_angle(incl_txt)
                        cone_dia    = para_conv(dia_txt, dia_unit_txt)
                        cone_rad    = cone_dia / 2
                        cone_hei = (self.bin_radius - cone_rad) * math.tan(math.radians(cone_incl))
                    # Calculates truncated cone height
                elif cone_para == 'C'.casefold():
                    cone_hei    = para_conv(hei_txt, hei_unit_txt)
                    cone_dia    = para_conv(dia_txt, dia_unit_txt)
                    cone_rad    = cone_dia / 2
                    cone_incl   = math.degrees(math.atan(cone_hei/((self.bin_diameter - cone_dia)/2)))
                    # Calculates cone inclination

                Ask = input('Do you want to select another option? Y/N ').casefold()
                while Ask not in ('N'.casefold(), 'No'.casefold(), 'Y'.casefold(), 'Yes'.casefold()):
                    print('Invalid Input!')
                    Ask = input('Do you want to select another option? Y/N ').casefold()
                if Ask in ('Y'.casefold(), 'Yes'.casefold()):
                    pass
                elif Ask in ('N'.casefold(), 'No'.casefold()):
                    break
            return cone_incl, cone_dia, cone_rad, cone_hei

        def cone_design_2():
            while True:
                cone_para = input('Enter A, B or C: ').casefold()
                while cone_para not in ['A'.casefold(), 'B'.casefold(), 'C'.casefold()]:
                    print('Invalid Input')
                    cone_para = input('Enter A, B or C: ').casefold()

                if cone_para == 'A'.casefold():
                    cone_incl = cone_angle(incl_txt)
                    cone_hei  = para_conv(hei_txt, hei_unit_txt)
                    cone_rad  = ((self.bin_radius*math.tan(math.radians(cone_incl))) -
                                cone_hei) / math.tan(math.radians(cone_incl))
                    # Calculates radius of cone opening
                    cone_dia  = 2 * cone_rad
                elif cone_para == 'B'.casefold():
                    cone_incl   = cone_angle(incl_txt)
                    cone_dia    = para_conv(dia_txt, dia_unit_txt)
                    cone_rad    = cone_dia / 2
                    cone_hei = (self.bin_radius - cone_rad) * math.tan(math.radians(cone_incl))
                    # Calculates truncated cone height
                elif cone_para == 'C'.casefold():
                    cone_hei    = para_conv(hei_txt, hei_unit_txt)
                    cone_dia    = para_conv(dia_txt, dia_unit_txt)
                    cone_rad    = cone_dia / 2
                    cone_incl   = math.degrees(math.atan(cone_hei/((self.bin_diameter - cone_dia)/2)))
                    # Calculates cone inclination

                Ask = input('Do you want to select another option? Y/N ').casefold()
                while Ask not in ('N'.casefold(), 'No'.casefold(), 'Y'.casefold(), 'Yes'.casefold()):
                    print('Invalid Input!')
                    Ask = input('Do you want to select another option? Y/N ').casefold()
                if Ask in ('Y'.casefold(), 'Yes'.casefold()):
                    pass
                elif Ask in ('N'.casefold(), 'No'.casefold()):
                    break
            return cone_incl, cone_dia, cone_rad, cone_hei

        FILE.writelines('        ***Silo Cone Information***\n')            

        if cap_in_kg <= 10000:
            # Bottom Cone Design
            print('\n')
            print('Options:')
            print(f'Enter "A" for {self.grain}\'s ANGLE OF REPOSE and BOTTOM CONE HEIGHT')
            print(f'Enter "B" for {self.grain}\'s ANGLE OF REPOSE and BOTTOM CONE OPENING DIAMETER')
            print('Enter "C" for bottom cone height and BOTTOM CONE OPENING DIAMETER')

            incl_txt     = f'Enter {self.grain}\'s ANGLE OF REPOSE: ' 
            hei_txt      = 'Enter assumed BOTTOM CONE HEIGHT: '
            hei_unit_txt = 'Enter UNIT of BOTTOM CONE HEIGHT (m, cm, mm, inches, ft): '
            dia_txt      = 'Enter BOTTOM CONE OPENING DIAMETER  : '
            dia_unit_txt = 'Enter unit of BOTTOM CONE OPENING DIAMETER (m, cm, mm, inches, ft): '

            bottom_result = cone_design_1()

            self.bottom_cone_inclination = bottom_result[0]
            self.bottom_cone_diameter    = bottom_result[1]
            self.bottom_cone_radius      = bottom_result[2]
            self.bottom_cone_height      = bottom_result[3]

            try:
                if not grain_data[self.grain]['angle of repose']: pass
            except KeyError:
                properties['angle of repose'] = self.bottom_cone_inclination
            

            self.bottom_cone_slant_height = (self.bin_radius/math.cos(math.radians(self.bottom_cone_inclination))) \
                                            - (self.bottom_cone_radius/math.cos(math.radians(self.bottom_cone_inclination)))

            self.bottom_cone_volume       = (1/3) * math.pi * (self.bin_radius**2 + (self.bin_radius*self.bottom_cone_radius)\
                                            + self.bottom_cone_radius**2) * self.bottom_cone_height

            self.bottom_cone_surface_area = math.pi * (self.bin_radius + self.bottom_cone_radius)\
                                            * math.sqrt(self.bottom_cone_height**2 \
                                            + (self.bin_radius - self.bottom_cone_radius)**2)
            
           

            FILE.writelines('    *Bottom Cone Information*\n')
            FILE.writelines(f'9.  Bottom Cone Inclination: {self.bottom_cone_inclination:.1f}\u00b0\n')
            FILE.writelines(f'10. Bottom Cone Opening Diameter: {self.bottom_cone_diameter:0.3f} m\n')
            FILE.writelines(f'11. Bottom Cone Height: {self.bottom_cone_height:.3f} m\n')
            FILE.writelines(f'12. Bottom Cone Slant Height: {self.bottom_cone_slant_height:.3f} m\n')   
            FILE.writelines(f'13. Bottom Cone Surface Area: {self.bottom_cone_surface_area:.3f} m\u00b2\n')
            FILE.writelines(f'14. Bottom Cone Volume: {self.bottom_cone_volume:.3f} m\u00b3\n')
            FILE.writelines('\n')
            
            
            print('\n')    
            print('Options:')
            print('Enter "A" for TOP CONE INCLINATION and HEIGHT')
            print('Enter "B" for TOP CONE INCLINATION and OPENING DIAMETER')
            print('Enter "C" for TOP CONE HEIGHT and OPENING DIAMETER')

            incl_txt     = 'Enter TOP CONE ANGLE of INCLINATION : '
            hei_txt      = 'Enter assumed TOP CONE HEIGHT: '
            hei_unit_txt = 'Enter UNIT of TOP CONE HEIGHT (m, cm, mm, inches, ft): '
            dia_txt      = 'Enter TOP CONE OPENING DIAMETER: '
            dia_unit_txt = 'Enter unit of TOP CONE OPENING DIAMETER(m, cm, mm, inches, ft): '

            top_result = cone_design_2()

            self.top_cone_inclination = top_result[0]
            self.top_cone_diameter    = top_result[1]
            self.top_cone_radius      = top_result[2]
            self.top_cone_height      = top_result[3]

            self.top_cone_slant_height = (self.bin_radius/math.cos(math.radians(self.top_cone_inclination))) \
                                         - (self.top_cone_radius/math.cos(math.radians(self.top_cone_inclination)))

            self.top_cone_volume       = (1/3) * math.pi * (self.bin_radius**2 + (self.bin_radius*self.top_cone_radius) \
                                         + self.top_cone_radius**2) * self.top_cone_height

            self.top_cone_surface_area = math.pi * (self.bin_radius + self.top_cone_radius)\
                                         * math.sqrt(self.top_cone_height**2 \
                                         + (self.bin_radius - self.top_cone_radius)**2)

            

            self.total_height       = self.bottom_cone_height + self.bin_height + self.top_cone_height 
    
            self.total_volume       = self.bottom_cone_volume + self.bin_volume + self.top_cone_volume

            self.total_surface_area = self.bottom_cone_surface_area + self.bin_surface_area + self.top_cone_surface_area

            self.total_capacity     = self.design_capacity + (self.bulk_density * (self.bottom_cone_volume + self.top_cone_volume)\
                                                              /1000)

            FILE.writelines('    *Top Cone Information*\n')
            FILE.writelines(f'15. Top Cone Angle of Inclination: {self.top_cone_inclination:.1f}\u00b0\n')
            FILE.writelines(f'16. Top Cone Opening Diameter: {self.top_cone_diameter:.3f} m\n')
            FILE.writelines(f'17. Top Cone Height: {self.top_cone_height:.3f} m\n')
            FILE.writelines(f'18. Top Cone Slant Height: {self.top_cone_slant_height:.3f} m\n')
            FILE.writelines(f'19. Top Cone Surface Area: {self.top_cone_surface_area:.3f} m\u00b2\n')
            FILE.writelines(f'20. Top Cone Volume: {self.top_cone_volume:.3f} m\u00b3\n')
            FILE.writelines('\n')

            FILE.writelines(f'21. Total Silo Height: {self.total_height:.3f}\n')
            FILE.writelines(f'22. Total Silo Surface Area: {self.total_surface_area:.3f} m\u00b2\n')
            FILE.writelines(f'23. Total Silo Volume: {self.total_volume:.3f} m\u00b3\n')
            FILE.writelines(f'24. Total Silo Capacity: {self.total_capacity:.3f} Tonnes\n')

            

        if cap_in_kg > 10000:
            print('\n')
            print('Options:')
            print('Enter "A" for CONE INCLINATION and CONE HEIGHT')
            print('Enter "B" for CONE INCLINATION and CONE OPENING DIAMETER')
            print('Enter "C" for CONE HEIGHT and CONE OPENING DIAMETER')

            incl_txt     = 'Enter CONE ANGLE of INCLINATION: '
            hei_txt     = 'Enter assumed CONE HEIGHT: '
            hei_unit_txt = 'Enter UNIT of CONE HEIGHT (m, cm, mm, inches, ft): '
            dia_txt      = 'Enter CONE OPENING DIAMETER: '
            dia_unit_txt = 'Enter unit of CONE OPENING DIAMETER (m, cm, mm, inches, ft): '

            result = cone_design_2()

            self.cone_inclination = result[0]
            self.cone_diameter    = result[1]
            self.cone_radius      = result[2]
            self.cone_height      = result[3]

            self.cone_slant_height = (self.bin_radius/math.cos(math.radians(self.cone_inclination))) \
                                      - (self.cone_radius/math.cos(math.radians(self.cone_inclination)))

            self.cone_volume       = (1/3) * math.pi * (self.bin_radius**2 + (self.bin_radius*self.cone_radius)\
                                     + self.cone_radius**2) * self.cone_height

            self.cone_surface_area = math.pi * (self.bin_radius + self.cone_radius) * math.sqrt(self.cone_height**2 +
                                     (self.bin_radius - self.cone_radius)**2)
            
            self.total_height      = self.cone_height + self.bin_height  
    
            self.total_volume      = self.cone_volume + self.bin_volume 

            self.total_surface_area = self.cone_surface_area + self.bin_surface_area
            self.total_capacity     = self.design_capacity + (self.bulk_density * self.cone_volume / 1000)

            

            FILE.writelines(f'9.  Cone Angle of Inclination: {self.cone_inclination:.1f}\u00b0\n')
            FILE.writelines(f'10. Cone Opening Diameter: {self.cone_diameter:.3f} m\n')
            FILE.writelines(f'11. Cone Height: {self.cone_height:.3f} m\n')
            FILE.writelines(f'12. Cone Slant Height: {self.cone_slant_height:0.3f} m\n')
            FILE.writelines(f'13. Cone Surface Area: {self.cone_surface_area:.3f} m\u00b2\n')
            FILE.writelines(f'14. Cone Volume: {self.cone_volume:.3f} m\u00b3\n')
            FILE.writelines('\n')

            FILE.writelines(f'15. Total Silo Height: {self.total_height:.3f} m\n')
            FILE.writelines(f'16. Total Silo Surface Area: {self.total_surface_area:.3f} m\u00b2\n')
            FILE.writelines(f'17. Total Silo Volume: {self.total_volume:.3f} m\u00b3\n')
            FILE.writelines(f'18. Total Silo Capacity: {self.total_capacity:.3f} Tonnes')
            FILE.writelines('\n')

        # Determines If Deep or Shallow Silo
        if self.bin_height / self.bin_diameter >= 1.5: 
            self.deep_or_shallow = 'Deep Silo'
        else:
            self.deep_or_shallow = 'Shallow Silo'
        
        if cap_in_kg >= 10000:
            FILE.writelines(f'19. Type of Silo: {self.deep_or_shallow}\n')
        else:
            FILE.writelines(f'25. Type of Silo: {self.deep_or_shallow}\n')
            
        FILE.close()

        if self.grain not in grain_data:
            store_grain(grain_data, self.grain, properties)
        grain_data.close()


        '''length_txt      = 'Enter length of metal plate: '
        length_unit_txt = 'Enter unit of length of metal plate(m, cm, mm, inches, ft): '
        breath_txt      = 'Enter breadth of metal plate: '
        breadth_unit_txt = 'Enter unit of breadth of metal plate(m, cm, mm, inches, ft): '

        length = para_conv(length_txt, length_unit_txt)
        breadth = para_conv(breath_txt, breadth_unit_txt)'''
        
            
            
           

    def pressure(self, y):  #Janssen theory
        grain_data = shelve.open(path, writeback=True)
        try:                                                # Gets angle of repose of grain for silo's > 10000kg
            if grain_data[self.grain]['angle of repose']:
                O = grain_data[self.grain]['angle of repose']
        except KeyError:
            txt = f'Enter {self.grain}\'s ANGLE OF REPOSE: '
            O = cone_angle(txt)
            properties['angle of repose'] = O
        w = self.bulk_density
        R = self.bin_diameter/4 #Hydraulic Radius
        K = (1 - math.sin(math.radians(O)))/(1 + math.sin(math.radians(O)))

        try:                                                # Gets static friction coefficient of grain on steel            if grain_data[self.grain]['static friction coefficient']:
                u = grain_data[self.grain]['static friction coefficient']
        except KeyError:
            txt = f'Enter {self.grain}\'s static friction coefficient with mild steel: '
            u = cone_angle(txt)
            properties['static friction coefficient'] = u

        try:                                                # stores angle of rep. grain in database
            if not grain_data[self.grain]['angle of repose']:
                pass
        except KeyError:
            grain_data[self.grain].update({'angle of repose': O})

        try:                                                # stores stat. fric. coeff.of grain in database
            if not grain_data[self.grain]['static friction coefficient']:
                pass
        except KeyError:
            grain_data[self.grain].update({'static friction coefficient': u})
            

        Pv = (w*R*(1-math.exp(-(K*u*y/R))))/(u*K)                           #Vertical pressure exerted by the grain material
        Pvp = (((w*R)/u) * (y + ((R/K*u)*math.exp(-((K*u*y)/R)))))\
             - ((w*R**2)/(K*u**2))                                  #vertical pressure of grain's on per unit wall perimeter
        Pl = K * Pv                                                  #Lateral static pressure on per unit wall perimeter

        FILE = open(path + file_name_with_ext, 'a')
        FILE.writelines('\n')
        FILE.writelines(f'        ***Pessure Exerted by {self.grain} on Silo Bin***\n')
        FILE.writelines(f'1. Vertical Pressure at height {y} m: {Pv:.3f} N/m\u00b2\n')
        FILE.writelines(f'2. Lateral Pressure: {Pl:.3f} N/m\u00b2\n')
        FILE.close()
        grain_data.close()
    

    def metal_sheet_count(self, plate_dimension):
        FILE = open(path + file_name_with_ext, 'a')
        FILE.writelines('\n')
        bin_plates = rectangle([self.circumference, self.bin_height], plate_dimension)[0]
        FILE.writelines('        ***Silo Metal Sheet***\n')
        if bin_plates < 2:
            FILE.writelines(f'1. Number of plates for silo bin: {bin_plates} plate\n')
        else:
            FILE.writelines(f'1. Number of plates for silo bin: {bin_plates} plates\n')
        
        if cap_in_kg <= 10000:
            top_cone_plates = cone(self.bin_diameter, self.top_cone_diameter, self.top_cone_height, plate_dimension)[0]
            bottom_cone_plates = cone(self.bin_diameter, self.bottom_cone_diameter, self.bottom_cone_height, plate_dimension)[0]

            if top_cone_plates < 2:
                FILE.writelines(f'2. Number of plates for top cone: {top_cone_plates} plate\n')
            else:
                FILE.writelines(f'2. Number of plates for top cone: {top_cone_plates} plates\n')
            if bottom_cone_plates:
                FILE.writelines(f'3. Number of plates for bottom cone: {bottom_cone_plates} plate\n')
            else:
                FILE.writelines(f'3. Number of plates for bottom cone: {bottom_cone_plates} plates\n')

            total_plates = bin_plates + top_cone_plates + bottom_cone_plates
            if total_plates < 2:
                FILE.writelines(f'3. Total number of plates: {total_plates} plate\n')
            else:
                FILE.writelines(f'3. Total number of plates: {total_plates} plates\n')

        else:
            cone_plates = cone(self.bin_diameter, self.cone_diameter, self.cone_height, plate_dimension)[0]

            if cone_plates < 2:
                FILE.writelines(f'2. Number of plates for cone: {cone_plates} plate\n')
            else:
                FILE.writelines(f'2. Number of plates for cone: {cone_plates} plates\n')

            total_plates = bin_plates + cone_plates
            if total_plates < 2:
                FILE.writelines(f'3. Total number of plates: {total_plates} plate\n')
            else:
                FILE.writelines(f'3. Total number of plates: {total_plates} plates\n')

        FILE.close()



    

        
