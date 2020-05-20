import time
import threading
from SourceSink.DataFormatParser import DataFormatParser
from SourceSink.MockSource import MockSource

import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle, PathPatch
from pytransform3d.rotations import *



def plot_coordinate_reference_frame(ax, linewidth=1, length=1, t=(0,0,0), q=None, R=None, **kw):
    if (q is None) and (R is None):
        R = np.eye(3)
    else:
        if R is None:
            q = np.array(q)
            R = matrix_from_quaternion(q)

    stop = R.dot(np.array((length, 0, 0))) + t  # rotate x-axis and then translate
    plot_vec3d(ax, linewidth=linewidth*(length*10), start=t, stop=stop, color='red', **kw)
    stop = R.dot(np.array((0, length, 0))) + t  # rotate y-axis and then translate
    plot_vec3d(ax, linewidth=linewidth*(length*10), start=t, stop=stop, color='green', **kw)
    stop = R.dot(np.array((0, 0, length))) + t  # rotate z-axis and then translate
    plot_vec3d(ax, linewidth=linewidth*(length*10), start=t, stop=stop, color='blue', **kw)


def plot_vec3d(ax, linewidth=1, start=(0,0,0), stop=(0,0,1), color='black', **kw):
    start = np.array(start)
    stop = np.array(stop)
    vec = stop - start

    ax.quiver(start[0], start[1], start[2], vec[0], vec[1], vec[2],
               arrow_length_ratio=0.3, pivot='tail', color = color, alpha = .8, capstyle='round', linewidth=linewidth)





if __name__ == '__main__':
    # CoordinateReferenceFrame("frame1")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    plot_vec3d(ax, stop=(1,1,1), linewidth=10)

    plot_coordinate_reference_frame(ax, length=0.1, q=(0,1,0,0))

    deg2rad = 2*np.pi/360
    R = matrix_from_axis_angle([1,0,0, 60*deg2rad])
    plot_coordinate_reference_frame(ax, length=0.5, t=(1,1,0), R=R)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()

