# rdp-algorithm

## What it does

Runs a python program that takes in 2 arguments: 
* a file path to a rosbag file containing ```nav_msgs/Path``` messages. 

    Default: ```data/path_test```
* an integer specifiying the number of points to simplify to. 

    Default: ```50```


## How it works

Using the Ramer-Douglas-Peucker algorithm, the points provided by the rosbag message is simplified. In the original RDP algorithm, the parameter used to simply the path is a value ```ε```, that represents a distance dimension. In this algorithm, a similar method of simplification is adopted but instead of using a value of ```ε```, the number of points to keep is specified instead.

## Setting up
1. Depending on the version of ```pip``` you are using, run the following command:

``` pip install -r requirements.txt ```

2. Move the ```.bag``` file into the folder ```rdp/data/```. You can use any other folder or file name as long as it is correctly provided to the program when ran

3. Run the program using the following command for defualt settings: ```python path.py```

## Running the Program
* For help with the parameters, run ```python path.py -h``` or ```python path.py --help```

```
usage: path.py [-h] [-p FILE_PATH] [-n NUMPOINTS]

Simplify path using Ramer-Douglas-Peuker algorithm

optional arguments:
  -h, --help            show this help message and exit
  -p FILE_PATH, --file_path FILE_PATH
                        path to rosbag file
  -n NUMPOINTS, --numpoints NUMPOINTS
                        number of points
```