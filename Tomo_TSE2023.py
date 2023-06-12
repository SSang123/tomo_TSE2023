# TomoNV example, C++ Dll version
from  tomoNV_Cpp import *
import os

#-----------------------------------------------
#(1) specify  filename and initial orientation( yaw, pitch, roll) in DEGREE.

#DataSet= [('MeshData\\(1)cone50_63k.obj',     0, 0, 0)]
#DataSet= [('MeshData\\(2)sphere90_39k.obj',    0, 0, 0)]
#DataSet= [('MeshData\\(3)Bunny_69k_2x.obj',    0, 0, 0)]
DataSet= [('MeshData\\(4)Bunny_69k.stl',    0, 0, 0)]
#DataSet= [('MeshData\\(5)Bunny_69k_0.5x.stl',     0, 0, 0)]
#DataSet= [('MeshData\\(6)Bunny_5k.stl',     0, 0, 0)]
#DataSet= [('MeshData\\(7)Bunny_1k.obj',    0, 0, 0)]
#DataSet= [('MeshData\\(8)manikin.obj',    0, 0, 0)]


#-----------------------------------------------
#(2) specify angle interval

theta_YP = 30 #=(360 / N) in DEGREE, N should be integer
#========================================================================================================================
 
for Data in DataSet:
  (g_input_mesh_filename, Yaw, Pitch, Roll) = Data
  if( os.path.isfile(g_input_mesh_filename) ):
    if(theta_YP==0):
      # type 1). seeing a specific orientation.  
      nYPR_Intervals=1
      yaw_range   = np.ones(nYPR_Intervals) * toRadian(Yaw)
      pitch_range = np.ones(nYPR_Intervals) * toRadian(Pitch)
      roll_range  = np.ones(nYPR_Intervals) * toRadian(Roll)
    elif(theta_YP> 0):
      # type 2). search optimal orientation
      nYPR_Intervals= int(360 / theta_YP) +1
      # nYPR_Intervals = 40
      yaw_range   = np.linspace(toRadian(0), toRadian(360), num=nYPR_Intervals, endpoint=True, dtype=np.float32)
      pitch_range = np.linspace(toRadian(0), toRadian(360), num=nYPR_Intervals, endpoint=True, dtype=np.float32)
      roll_range  = np.zeros(1) #for generality. roll direction  is not needed.
    else:
      import sys
      sys.exit(0)

    tomoNV_Cpp1 = tomoNV_Cpp(g_input_mesh_filename, nYPR_Intervals, yaw_range, pitch_range, roll_range , bVerbose=True)# load mesh file and Cpp Dll
    #-----------------------------------------------
    # (3) input parameters.

    #algorithm internal parameters(DO NOT CHANGE THESE VALUES)
    tomoNV_Cpp1.dVoxel  = 1.0 # size of voxel. 
    tomoNV_Cpp1.nVoxel  = 256 # number of voxels. 
    tomoNV_Cpp1.bUseExplicitSS = True #Set as True to see the SS pixels visually.
    tomoNV_Cpp1.wall_thickness = 0.8 # [mm]
    tomoNV_Cpp1.Fclad   = 1.0 # fill ratio of cladding, always 1.0

    #filament parameters (from g-code SW)
    tomoNV_Cpp1.PLA_density    = 0.00121 # density of PLA filament, [g/mm^3]
    tomoNV_Cpp1.Fcore   = 0.15 # fill ratio of core, (0~1.0)
    tomoNV_Cpp1.Fss     = 0.2 # fill ratio of support structure, (0~1.0)

    #Support structure parameter
    tomoNV_Cpp1.theta_c = toRadian(60) #filament critical angle for support structure

    #bed structure parameter
    #tomoNV_Cpp1.BedType = ( enumBedType.ebtSkirt, 2, 5, 1)
    #tomoNV_Cpp1.BedType = ( enumBedType.ebtBrim, 2.5, 5, 1)
    tomoNV_Cpp1.BedType = ( enumBedType.ebtRaft, 2, 5, 1.)
    
    #-----------------------------------------------
    # (4) call C++ engine (TomoNV_Win64.dll)

    tomoNV_Cpp1.Run(cpp_function_name = 'TomoNV_INT3') 
    
    #-----------------------------------------------
    # (5) Rendering

    Plot3DPixels(tomoNV_Cpp1) #show pixels of the 1st optimal
    #PrintSlotInfo( tomoNV_Cpp1, X=8,Y=4) #for debugging. print data in (X,Y) coordinate.
    #tomoNV_Cpp1.Print_table()

    print( FStr(np.append( toDegree(tomoNV_Cpp1.YPR), np.column_stack([tomoNV_Cpp1.Mtotal3D]), axis=1)))#print (yaw, pitch, roll, Mtotal)

    if tomoNV_Cpp1.nYPR_Intervals >= 5:
      (optimal_YPRs,worst_YPRs) = findOptimals(tomoNV_Cpp1.YPR, tomoNV_Cpp1.Mtotal3D, g_nOptimalsToDisplay) #show optimals & worst orientations
      Plot3D(tomoNV_Cpp1.mesh0, yaw_range, pitch_range, tomoNV_Cpp1.Mtotal3D, optimal_YPRs, worst_YPRs) # show the 1st optimal in 3D

# i = 0  
#-----------------------------------------------
