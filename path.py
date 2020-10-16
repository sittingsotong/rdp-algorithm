import bagpy
from bagpy import bagreader
import pandas as pd
import numpy as np 
from numpy.linalg import norm
import argparse

# for visualisation
import matplotlib.pyplot as plt

def read_data_into_csv(csvfiles, file_path):
    b = bagreader(file_path)

    for topic in b.topics:
        raw_data = b.message_by_topic(topic)
        csvfiles.append(raw_data)

# get perpendicular dist bw line (p1, p2) and p3
def perpendicular_dist(p1, p2, p3):
    p1 = np.asarray(p1)
    p2 = np.asarray(p2)
    p3 = np.asarray(p3)

    return np.abs(np.cross(p2-p1, p1-p3)) / norm(p2-p1)

# using the Ramer-Douglas-Peuker algorithm
def rdp(pointList, n):
    weights = []
    length = len(pointList)

    def get_weights(start, end):
        if(end > start+1):
            dmax = 0
            index = 0

            for i in range(start+1, end):
                d = perpendicular_dist(pointList[start], pointList[end], pointList[i])
                if d > dmax:
                    dmax = d 
                    index = i

            weights.insert(index, dmax)

            get_weights(start, index)
            get_weights(index, end)

    get_weights(0, length-1)
    weights.insert(0, float("inf"))
    weights.append(float("inf"))

    weightsDecending = weights
    
    # sorts in decending order
    weightsDecending = sorted(weightsDecending, reverse=True)

    max_dist = weightsDecending[n-1]

    result = [
        point for i, point in enumerate(pointList) if weights[i] >= max_dist
    ]

    return result

def visualise_path(path, numPoints):
    img = np.zeros(shape=(512, 512, 3), dtype=np.float32)

    x_values = []
    y_values = []

    for point in path:
        x_values.append(point[0])
        y_values.append(point[1])

    plt.plot(x_values, y_values)
    plt.title(f"Simplified Path with {numPoints} points")
    plt.xlabel("x coordinate")
    plt.ylabel("y coordinate")
    plt.show()

def main(numpoints, file_path):
    # list of path to csv files
    csvfiles = []

    read_data_into_csv(csvfiles, file_path)

    df = pd.read_csv(csvfiles[0], ',', header=0, index_col=False)
    df['Coordinates'] = [[x, y] for x, y in zip(df['pose.position.x'], df['pose.position.y'])]
    coord = df['Coordinates'].to_numpy()

    # visualise_path(coord, 1000)
    result = rdp(coord, numpoints)

    print(result)

    visualise_path(result, numpoints)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simplify path using Ramer-Douglas-Peuker algorithm')
    parser.add_argument('-p', '--file_path', dest='file_path', type=str, default='data/path_test.bag', help='path to rosbag file')
    parser.add_argument('-n', '--numpoints', dest='Numpoints', type=int, default=50, help='number of points')
    
    args = parser.parse_args()
    numpoints = args.Numpoints
    file_path = args.file_path
    main(numpoints, file_path)  