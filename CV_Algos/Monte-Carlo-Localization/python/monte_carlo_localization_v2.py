#!/usr/bin/env python
import rospy
import tf
import tf.transformations as tr
from std_msgs.msg import String, Header, ColorRGBA
from nav_msgs.msg import OccupancyGrid, MapMetaData, Odometry
from geometry_msgs.msg import Twist, PoseStamped, Point
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker, MarkerArray
from math import sqrt, cos, sin, pi, atan2
from threading import Thread, Lock
from math import pi, log, exp
import random
import numpy as np
import sys
import pickle


class Particle(object):
    def __init__(self, id, x,y, theta):
        self.x = x
        self.y = y
        self.id = id
        self.theta = theta

class ParticleFilter(object):
    def __init__(self, num_particles, occ_grid_map, xmin, xmax, ymin, ymax,
                 laser_min_range, laser_max_range, laser_min_angle, laser_max_angle,
                 dynamics_translation_noise_std_dev,
                 dynamics_orientation_noise_std_dev,
                 beam_range_measurement_noise_std_dev):

        self.num_particles = num_particles
        self.ogm = occ_grid_map
        self.grid_map = np.array(self.ogm.data, dtype='int8')
        self.grid_map = self.grid_map.reshape((self.ogm.info.height, self.ogm.info.width))
        self.grid_bin = (self.grid_map == 0).astype('uint8')  # Cell is True iff probability of being occupied is zero

        # Workspace boundaries
        self.xmax = xmax
        self.xmin = xmin
        self.ymin = ymin
        self.ymax = ymax

        self.laser_max_angle = laser_max_angle
        self.laser_min_angle = laser_min_angle
        self.laser_max_range = laser_max_range
        self.laser_min_range = laser_min_range

        # Std deviation of noise affecting translation in the dynamics model for particles
        self.dynamics_translation_noise_std_dev = dynamics_translation_noise_std_dev

        # Std deviation of noise affecting orientation in the dynamics model for particles
        self.dynamics_orientation_noise_std_dev = dynamics_orientation_noise_std_dev

        # Std deviation of noise affecting measured range from the laser measurement model
        self.beam_range_measurement_noise_std_dev = beam_range_measurement_noise_std_dev

        # Number of laser beams to simulate when predicting what a
        # particle's measurement is going to be
        self.eval_beams = 32

        # Previous odometry measurement of the robot
        self.last_robot_odom = None

        # Current odometry measurement of the robot
        self.robot_odom = None

        # Relative motion since the last time particles were updated
        self.dx = 0
        self.dy = 0
        self.dyaw = 0

        self.particles = []
        self.weights = []

    def get_random_free_state(self):
        while True:
            # Note: we initialize particles closer to the robot's initial
            # position in order to make the initialization easier
            xrand = np.random.uniform(self.xmin*0.2, self.xmax*0.2)
            yrand = np.random.uniform(self.ymin*0.2, self.ymax*0.2)
            row, col = self.metric_to_grid_coords(xrand, yrand)
            if self.grid_bin[row, col]:
                theta = np.random.uniform(0, 2*pi)
                return xrand, yrand, theta

    def init_particles(self):
        """Initializes particles uniformly randomly with map frame coordinates,
        within the boundaries set by xmin,xmax, ymin,ymax"""
        for i in xrange(self.num_particles):
            xrand, yrand, theta = self.get_random_free_state()
            # Note: same orientation as the initial orientation of the robot
            # to make initialization easier
            self.particles.append(Particle(i, xrand, yrand, 0))

    def handle_observation(self, laser_scan, dt):
        """Does prediction, weight update, and resampling."""

        # TODO: for every particle
        # 1) Predict its relative motion since the last time an observation was received using
        # predict_particle_odometry().
        # 2) Compute the squared norm of the difference between the particle's predicted laser scan
        # and the actual laser scan

        # TODO: exponentiate the prediction errors you computed above
        # using numerical stability tricks such as
        # http://timvieira.github.io/blog/post/2014/02/11/exp-normalize-trick/
        # if you think it is necessary

        errors = []
        #self.weights = [0] * len(self.particles)
        for particle in self.particles:
            self.predict_particle_odometry(particle)
            #for each particle, compute the laser scan difference
            error = self.get_prediction_error_squared(laser_scan, particle)
            #sig_error = self.sigmoid(error)
            errors.append(error)
            #self.weights.append(exp(-error))

        self.weights = [exp(-error) for error in errors]
        weight_sum = sum(self.weights)
        N_eff = 0
        #N_eff = sum([1 / ((weight / weight_sum) ** 2) for weight in self.weights])
        #print "effective sample size", N_eff

        # Do resampling. Depending on how you implement it you might
        # or might not need to normalize your weights by their sum, so
        # they are treated as probabilities

        # particle deprivation:
        # approach 1: calculate sample size by variance
        # get the partice id among the survived particles after resampling
        new_particles = []
        self.resample(new_particles)
        #particle_indexes = self.resample(new_particles)
        #remove duplicates
        """
        N_eff_id = set(particle_indexes)
        print "N_eff_id",[id for id in N_eff_id]
        #effective sample size based on particle's contribution
        N_eff_size = len(N_eff_id)
        #print "N_eff_size", N_eff_size
        """

        # approach 2: calculate the effective sample size by weight
        sig_weight = [self.sigmoid(error) for error in errors]
        N_eff_weight = sum([1 / (weight ** 2) for weight in sig_weight])
        #print "N_eff_weight", N_eff_weight

        N_eff = N_eff_weight
        #N_eff = N_eff_size

        # address particle deprivation
        # 1. resample only when N_eff > N_thresh
        if N_eff > 50:
            self.particles = new_particles

        #print [particle.id for particle in self.particles]
        #print "weight", self.weights

    def divide_up(self, id, particle, num, particle_list):
        for i in xrange(int(num)):
            xrand = np.random.uniform(particle.x*-0.5, particle.x*0.5)
            yrand = np.random.uniform(particle.y*-0.5, particle.y*0.5)
            theta = np.random.uniform(particle.theta*-0.5, particle.theta*0.5)
            particle_list.append(Particle(id, xrand, yrand, theta))
            id += 1

    def sigmoid(self, x):
        """Numerically-stable sigmoid function."""
        if x >= 0:
            z = exp(-x)
            return 1 / (1 + z)
        else:
            # if x is less than zero then z will be small, denom can't be
            # zero because it's 1+z.
            z = exp(x)
            return z / (1 + z)

    def resample(self, new_particles):

        # TODO: sample particle i with probability that
        # is proportional to its weight w_i. Sampling
        # can be done with repetition/replacement, so
        # you can sample the same particle more than once.

        #particle_indexes = []
        sample_u = np.random.uniform(0,1)
        index = int(sample_u * (self.num_particles - 1))
        beta = 0.0
        if self.weights == []:
            self.weights = [1] * self.num_particles
            print self.weights
        max_w = max(self.weights)
        #print "max_w", max_w
        #print "weight", self.weights
        for particle in self.particles:
            beta += np.random.uniform(0,1) * 2.0 * max_w
            while beta > self.weights[index]:
                beta -= self.weights[index]
                index = (index + 1) % self.num_particles

            particle = self.particles[index]
            #particle_indexes.append(particle.id)
            new_particles.append(Particle(particle.id, particle.x, particle.y, particle.theta))

        #self.particles = new_particles
        #return particle_indexes

    def simulate_laser_scan_for_particle(self, x, y, yaw_in_map, angles, min_range, max_range):
        """If the robot was at the given particle, what would its laser scan
        be (in the known map)? Returns the predicted laser ranges if a particle with state (x,y,yaw_in_map)
        is to scan along relative angles in angles."""
        # for every relative angle in angles
        # 1. The absolute angle based on the robot's orientation is computed
        # 2. Ray tracing from (x,y) along the abosulte angle using step size range_step is done
        #    (a) If the currently examined point is within the bounds of the workspace
        #        stop if it meets an obstacle or if it reaches max_range
        #    (b) If the currently examined point is outside the bounds of the workspace
        #        stop if it reaches max_range
        # 3. The computed collection of ranges corresponding to the given angles is returned

        ranges = []
        range_step = self.ogm.info.resolution

        for angle in angles:
            phi = yaw_in_map + angle

            r = min_range
            while r <= max_range:
                xm = x + r*cos(phi)
                ym = y + r*sin(phi)

                if xm > self.xmax or xm < self.xmin:
                    break

                if ym > self.ymax or ym < self.ymin:
                    break

                row, col = self.metric_to_grid_coords(xm, ym)
                free = self.grid_bin[row, col].all()
                if not free:
                    break

                r += range_step

            ranges.append(r)

        return ranges


    def subsample_laser_scan(self, laser_scan_msg):
        """Subsamples a set number of beams (self.eval_beams) from the incoming actual laser scan. It also
        converts the Inf range measurements into max_range range measurements, in order to be able to
        compute a difference."""

        # To convert the laser points from the husky_1/base_laser frame, whose z-axis points downwards
        # to the same frame pointing upwards

        N = len(laser_scan_msg.ranges)
        ranges_in_upwards_baselaser_frame = laser_scan_msg.ranges
        angles_in_baselaser_frame = [(laser_scan_msg.angle_max - laser_scan_msg.angle_min)*float(i)/N + laser_scan_msg.angle_min for i in xrange(N)]

        step = N/self.eval_beams
        angles_in_upwards_baselaser_frame = angles_in_baselaser_frame[::step]
        ranges_in_upwards_baselaser_frame = ranges_in_upwards_baselaser_frame[::-step]

        assert (len(ranges_in_upwards_baselaser_frame) == len(angles_in_upwards_baselaser_frame))

        actual_ranges = []
        for r in ranges_in_upwards_baselaser_frame:
            if r >= self.laser_min_range and r <= self.laser_max_range:
                actual_ranges.append(r)

            if r < self.laser_min_range:
                actual_ranges.append(self.laser_min_range)

            if r > self.laser_max_range:
                actual_ranges.append(self.laser_max_range)


        return actual_ranges, angles_in_upwards_baselaser_frame

    def get_prediction_error_squared(self, laser_scan_msg, particle):
        """
        This function evaluates the squared norm of the difference/error between the
        scan in laser_scan_msg and the one that was predicted by the given particle.

        Assume that the bearing of each beam relative to the robot's orientation has zero noise,
        so the only noise in the measurement comes from the range of each beam and is
        distributed as N(0, beam_range_measurement_std_dev^2)
        """

        # If the particle is out of the bounds of the workspace
        # give it a large error
        if particle.x < self.xmin or particle.x > self.xmax:
            return 300

        if particle.y < self.ymin or particle.y > self.ymax:
            return 300

        # If the particle falls inside an obstacle
        # give it a large error
        row, col = self.metric_to_grid_coords(particle.x, particle.y)
        if row >= 201 or col >=201:
            return 300

        if not self.grid_bin[row, col]:
            return 300

        assert (self.laser_min_range >= 0)
        assert (self.laser_max_range > 0)

        # TODO: subsample the recived actual laser scan using the
        # subsample_laser_scan method above
        # actual ranges and angles
        [actual_ranges, angles] = self.subsample_laser_scan(laser_scan_msg)

        min_range = min(actual_ranges)
        max_range = max(actual_ranges)
        #print "min_range", min_range
        #print "max_range", max_range
        # TODO: simulate a laser scan using one of the methods of this class
        predict_ranges = self.simulate_laser_scan_for_particle(particle.x, particle.y, particle.theta, angles, self.laser_min_range, self.laser_max_range)
        #predict_ranges = self.simulate_laser_scan_for_particle(particle.x, particle.y, particle.theta, angles, min_range, max_range)

        # TODO: compute the difference bwteen predicted ranges and actual ranges

        diff = [actual_range - predict_range for actual_range, predict_range in zip(actual_ranges, predict_ranges)]
        #print "diff", diff
        # Take the squared norm of that difference
        norm_error = 0
        norm_error = np.linalg.norm(diff)
        print "norm_error", norm_error
        return norm_error**2

    def handle_odometry(self, robot_odom):
        """Compute the relative motion of the robot from the previous odometry measurement
        to the current odometry measurement."""
        self.last_robot_odom = self.robot_odom
        self.robot_odom = robot_odom

        if self.last_robot_odom:

            p_map_currbaselink = np.array([self.robot_odom.pose.pose.position.x,
                                           self.robot_odom.pose.pose.position.y,
                                           self.robot_odom.pose.pose.position.z])

            p_map_lastbaselink = np.array([self.last_robot_odom.pose.pose.position.x,
                                           self.last_robot_odom.pose.pose.position.y,
                                           self.last_robot_odom.pose.pose.position.z])

            q_map_lastbaselink = np.array([self.last_robot_odom.pose.pose.orientation.x,
                                           self.last_robot_odom.pose.pose.orientation.y,
                                           self.last_robot_odom.pose.pose.orientation.z,
                                           self.last_robot_odom.pose.pose.orientation.w])

            q_map_currbaselink = np.array([self.robot_odom.pose.pose.orientation.x,
                                           self.robot_odom.pose.pose.orientation.y,
                                           self.robot_odom.pose.pose.orientation.z,
                                           self.robot_odom.pose.pose.orientation.w])

            R_map_lastbaselink = tr.quaternion_matrix(q_map_lastbaselink)[0:3,0:3]

            p_lastbaselink_currbaselink = R_map_lastbaselink.transpose().dot(p_map_currbaselink - p_map_lastbaselink)
            q_lastbaselink_currbaselink = tr.quaternion_multiply(tr.quaternion_inverse(q_map_lastbaselink), q_map_currbaselink)

            _, _, yaw_diff = tr.euler_from_quaternion(q_lastbaselink_currbaselink)

            self.dyaw += yaw_diff
            self.dx += p_lastbaselink_currbaselink[0]
            self.dy += p_lastbaselink_currbaselink[1]


    def predict_particle_odometry(self, particle):
        """
        Where will the particle go after time dt passes?
        This function modifies the particle's state by simulating the effects
        of the given control forward in time.

        Assume Dubins dynamics with variable forward velocity for the Husky.
        """

        nx = random.gauss(0, self.dynamics_translation_noise_std_dev)
        ny = random.gauss(0, self.dynamics_translation_noise_std_dev)
        ntheta = random.gauss(0, self.dynamics_orientation_noise_std_dev)

        v = sqrt(self.dx**2 + self.dy**2)

        # Don't let the particle propagation be dominated by noise
        if abs(v) < 1e-10 and abs(self.dyaw) < 1e-5:
            return

        particle.x += v * cos(particle.theta) + nx
        particle.y += v * sin(particle.theta) + ny
        particle.theta += self.dyaw + ntheta


    def metric_to_grid_coords(self, x, y):
        """Converts metric coordinates to occupancy grid coordinates"""

        gx = (x - self.ogm.info.origin.position.x) / self.ogm.info.resolution
        gy = (y - self.ogm.info.origin.position.y) / self.ogm.info.resolution
        row = min(max(int(gy), 0), self.ogm.info.height)
        col = min(max(int(gx), 0), self.ogm.info.width)
        return (row, col)

class MonteCarloLocalization(object):

    def __init__(self, num_particles, xmin, xmax, ymin, ymax):
        rospy.init_node('monte_carlo_localization', anonymous=True)
        self.map_file = rospy.get_param("~map_file")

        dynamics_translation_noise_std_dev   = rospy.get_param("~dynamics_translation_noise_std_dev")
        dynamics_orientation_noise_std_dev   = rospy.get_param("~dynamics_orientation_noise_std_dev")
        beam_range_measurement_noise_std_dev = rospy.get_param("~beam_range_measurement_noise_std_dev")

        pkl_file = open(self.map_file, 'rb')
        self.ogm = pickle.load(pkl_file)
        pkl_file.close()

        self.q_baselink_baselaser = np.array([1.0, 0, 0, 0])
        self.R_baselink_baselaser = tr.quaternion_matrix(self.q_baselink_baselaser)[0:3,0:3]
        self.p_baselink_baselaser = np.array([0.337, 0.0, 0.308])

        self.pf = ParticleFilter(num_particles, self.ogm, xmin, xmax, ymin, ymax, 0, 0, 0, 0,
                                 dynamics_translation_noise_std_dev,
                                 dynamics_orientation_noise_std_dev,
                                 beam_range_measurement_noise_std_dev)

        self.pf.init_particles()
        self.last_scan = None
        self.mutex = Lock()

        self.laser_points_marker_pub = rospy.Publisher('/husky_1/debug/laser_points', Marker, queue_size=1)
        self.particles_pub = rospy.Publisher('/husky_1/particle_filter/particles', MarkerArray, queue_size=1)
        self.odom_sub = rospy.Subscriber('/husky_1/odometry/ground_truth', Odometry, self.odometry_callback, queue_size=1)
        self.laser_sub = rospy.Subscriber('/husky_1/scan', LaserScan, self.laser_scan_callback, queue_size=1)

    def odometry_callback(self, msg):
        self.mutex.acquire()
        self.pf.handle_odometry(msg)
        self.mutex.release()

    def get_2d_laser_points_marker(self, timestamp, frame_id, pts_in_map, marker_id, rgba):
        msg = Marker()
        msg.header.stamp = timestamp
        msg.header.frame_id = frame_id
        msg.ns = 'laser_points'
        msg.id = marker_id
        msg.type = 6
        msg.action = 0
        msg.points = [Point(pt[0], pt[1], pt[2]) for pt in pts_in_map]
        msg.colors = [rgba for pt in pts_in_map]

        for pt in pts_in_map:
            assert((not np.isnan(pt).any()) and np.isfinite(pt).all())

        msg.scale.x = 0.1
        msg.scale.y = 0.1
        msg.scale.z = 0.1
        return msg


    def laser_scan_callback(self, msg):
        self.pf.laser_min_angle = msg.angle_min
        self.pf.laser_max_angle = msg.angle_max
        self.pf.laser_min_range = msg.range_min
        self.pf.laser_max_range = msg.range_max

        dt_since_last_scan = 0

        if self.last_scan:
            dt_since_last_scan = (msg.header.stamp - self.last_scan.header.stamp).to_sec()

        self.mutex.acquire()
        self.publish_laser_pts(msg)
        self.pf.handle_observation(msg, dt_since_last_scan)

        self.pf.dx = 0
        self.pf.dy = 0
        self.pf.dyaw = 0

        self.mutex.release()
        self.last_scan = msg

    def publish_laser_pts(self, msg):
        """Publishes the currently received laser scan points from the robot, after we subsampled
        them in order to comparse them with the expected laser scan from each particle."""
        if self.pf.robot_odom is None:
            return

        subsampled_ranges, subsampled_angles = self.pf.subsample_laser_scan(msg)

        N = len(subsampled_ranges)
        x = self.pf.robot_odom.pose.pose.position.x
        y = self.pf.robot_odom.pose.pose.position.y
        _, _ , yaw_in_map = tr.euler_from_quaternion(np.array([self.pf.robot_odom.pose.pose.orientation.x,
                                                               self.pf.robot_odom.pose.pose.orientation.y,
                                                               self.pf.robot_odom.pose.pose.orientation.z,
                                                               self.pf.robot_odom.pose.pose.orientation.w]))

        pts_in_map = [ (x + r*cos(theta + yaw_in_map),
                        y + r*sin(theta + yaw_in_map),
                        0.3) for r,theta in zip(subsampled_ranges, subsampled_angles)]

        lpmarker = self.get_2d_laser_points_marker(msg.header.stamp, 'map', pts_in_map, 30000, ColorRGBA(1.0, 0.0, 0, 1.0))
        self.laser_points_marker_pub.publish(lpmarker)


    def get_particle_marker(self, timestamp, particle, marker_id):
        """Returns an rviz marker that visualizes a single particle"""
        msg = Marker()
        msg.header.stamp = timestamp
        msg.header.frame_id = 'map'
        msg.ns = 'particles'
        msg.id = marker_id
        msg.type = 0  # arrow
        msg.action = 0 # add/modify
        msg.lifetime = rospy.Duration(1)

        yaw_in_map = particle.theta
        vx = cos(yaw_in_map)
        vy = sin(yaw_in_map)

        msg.color = ColorRGBA(0, 1.0, 0, 1.0)

        msg.points.append(Point(particle.x, particle.y, 0.2))
        msg.points.append(Point(particle.x + 0.3*vx, particle.y + 0.3*vy, 0.2))

        msg.scale.x = 0.05
        msg.scale.y = 0.15
        msg.scale.z = 0.1
        return msg

    def publish_particle_markers(self):
        """ Publishes the particles of the particle filter in rviz"""
        ma = MarkerArray()
        ts = rospy.Time.now()
        for i in xrange(len(self.pf.particles)):
            ma.markers.append(self.get_particle_marker(ts, self.pf.particles[i], i))

        self.particles_pub.publish(ma)

    def run(self):
        rate = rospy.Rate(20)
        while not rospy.is_shutdown():
            self.publish_particle_markers()
            rate.sleep()


if __name__ == '__main__':
    num_particles = 50

    # Workspace boundaries in meters
    xmin = -20
    xmax = 20
    ymin = -20
    ymax = 20

    mcl = MonteCarloLocalization(num_particles, xmin, xmax, ymin, ymax)
    mcl.run()
