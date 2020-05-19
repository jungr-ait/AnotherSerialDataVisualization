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

class CoordinateReferenceFrame():
    def __init__(self, title="title"):

        self.fig = plt.figure(figsize=(10, 5), dpi=50)
        self.fig.suptitle(title, fontsize=16)
        self.fig.set_label("over time")#
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_aspect('equal')

    def draw(self, px, py, pz, len=1):
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.set_zlim(0, 10)

        plt.show()


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


def plot_arrow3d(ax, length=1, width=0.05, head=0.2, headwidth=2,
                theta_x=0, theta_z=0, offset=(0,0,0), **kw):
    w = width
    h = head
    hw = headwidth
    theta_x = np.deg2rad(theta_x)
    theta_z = np.deg2rad(theta_z)

    a = [[0,0],[w,0],[w,(1-h)*length],[hw*w,(1-h)*length],[0,length]]
    a = np.array(a)

    r, theta = np.meshgrid(a[:,0], np.linspace(0,2*np.pi,30))
    z = np.tile(a[:,1],r.shape[0]).reshape(r.shape)
    x = r*np.sin(theta)
    y = r*np.cos(theta)

    rot_x = np.array([[1,0,0],[0,np.cos(theta_x),-np.sin(theta_x) ],
                      [0,np.sin(theta_x) ,np.cos(theta_x) ]])
    rot_z = np.array([[np.cos(theta_z),-np.sin(theta_z),0 ],
                      [np.sin(theta_z) ,np.cos(theta_z),0 ],[0,0,1]])

    b1 = np.dot(rot_x, np.c_[x.flatten(),y.flatten(),z.flatten()].T)
    b2 = np.dot(rot_z, b1)
    b2 = b2.T+np.array(offset)
    x = b2[:,0].reshape(r.shape);
    y = b2[:,1].reshape(r.shape);
    z = b2[:,2].reshape(r.shape);
    ax.plot_surface(x,y,z, **kw)



if __name__ == '__main__':
    # CoordinateReferenceFrame("frame1")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # plot_arrow3d(ax)
    #
    # plot_arrow3d(ax, length=2, width=0.02, head=0.1, headwidth=1.5, offset=[1, 1, 0],
    #         theta_x=40, color="crimson")
    #
    # plot_arrow3d(ax, length=1.4, width=0.03, head=0.15, headwidth=1.8, offset=[1, 0.1, 0],
    #         theta_x=-60, theta_z=60, color="limegreen")

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

