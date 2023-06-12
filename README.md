# tomo_TSE2023
support structure tomography, submitted for Textile Science Engineering (2023)

#### 1. Download all the files of this repository to your PC ("Code"->"Download Zip")

#### 2. Install software
##### 1) Install Visual Studio Code (VSCode)
##### 2) Install Python 3 (preferably Version 3.7.8)
##### 3) Install Python packages using "requirements.txt".
```
pip install -r requirements.txt
```
#### 3. Open the downloaded folder in Visual Studio Code. Modify  mesh filename,  initial orientation and angle interval(=theta_YP) in "tomo_TSE2023.py".  Run the "tomo_TSE2023.py" (shortcut key, F5)

(1) To see the support structure information for the given (yaw, pitch, roll), set "theta_YP" as zero.
```
#=========================================================================================
DataSet= [( 'MeshData\\(4)Bunny_69k.stl', 247, 46, 0)
theta_YP = 0
#=========================================================================================
```

(2) To search optimal orientation, input "theta_yp" value as "360 / N " (where N = integer).
```
#=========================================================================================
DataSet= [( 'MeshData\\(4)Bunny_69k.stl', 0, 0, 0)
theta_YP = 30
#=========================================================================================
```
