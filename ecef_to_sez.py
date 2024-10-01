# ecef_to_sez.py
# Usage: python3 script_name.py arg1 arg2 ...
#  Text explaining script usage
# Parameters:
#  arg1: description of argument 1
#  arg2: description of argument 2
#  ...
# Output:
#  A description of the script output
#
# Written by First Last
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
# e.g., import math # math module
import sys # argv
import math

# "constants"
# e.g., R_E_KM = 6378.137
R_E_KM = 6378.137
E_E = 0.081819221456
# helper functions

## function description
# def calc_something(param1, param2):
#   pass

# initialize script arguments
# arg1 = '' # description of argument 1
# arg2 = '' # description of argument 2

# parse script arguments
# if len(sys.argv)==3:
#   arg1 = sys.argv[1]
#   arg2 = sys.argv[2]
#   ...
# else:
#   print(\
#    'Usage: '\
#    'python3 arg1 arg2 ...'\
#   )
#   exit()

# write script below this line

def calc_denom(ecc, lat_rad):
    return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad))**2)
def ecef_to_llh(r_x_km, r_y_km, r_z_km):
    
    # calculate longitude
    lon_rad = math.atan2(r_y_km,r_x_km)
    lon_deg = lon_rad*180.0/math.pi

    # initialize lat_rad, r_lon_km, r_z_km
    lat_rad = math.asin(r_z_km/math.sqrt(r_x_km**2+r_y_km**2+r_z_km**2))
    r_lon_km = math.sqrt(r_x_km**2+r_y_km**2)
    prev_lat_rad = float('nan')

    # iteratively find latitude
    c_E = float('nan')
    count = 0
    while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
        denom = calc_denom(E_E,lat_rad)
        c_E = R_E_KM/denom
        prev_lat_rad = lat_rad
        lat_rad = math.atan((r_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
        count = count+1
    
    # calculate hae
    hae_km = r_lon_km/math.cos(lat_rad)-c_E

    return lat_rad, lon_rad

def ecef_to_sez(o_x_km, o_y_km, o_z_km, x_km, y_km, z_km):
    lat_o_rad, lon_o_rad = ecef_to_llh(o_x_km, o_y_km, o_z_km)

    dx = x_km - o_x_km
    dy = y_km - o_y_km
    dz = z_km - o_z_km

    s_km = (-dz*math.cos(lat_o_rad)) + (dx*math.cos(lon_o_rad)*math.sin(lat_o_rad)) + (dy*math.sin(lat_o_rad)*math.sin(lon_o_rad))
    e_km = (dy*math.cos(lon_o_rad)) - (dx*math.sin(lon_o_rad))
    z_km = (dx*math.cos(lat_o_rad)*math.cos(lon_o_rad)) + (dz*math.sin(lat_o_rad)) + (dy*math.cos(lat_o_rad)*math.sin(lon_o_rad))

    return s_km, e_km, z_km

if len(sys.argv) == 7:
    o_x_km = float(sys.argv[1])
    o_y_km = float(sys.argv[2])
    o_z_km = float(sys.argv[3])
    x_km = float(sys.argv[4])
    y_km = float(sys.argv[5])
    z_km = float(sys.argv[6])
else:
    print('Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km')

s_km, e_km, z_km = ecef_to_sez(o_x_km, o_y_km, o_z_km, x_km, y_km, z_km)

print(s_km)
print(e_km)
print(z_km)
