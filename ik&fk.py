import numpy as np

# COM_OFFSET = -np.array([0.012731, 0.002186, 0.000515])
COM_OFFSET = -np.array([0.0, 0.0, 0.0])
HIP_OFFSETS = np.array([[0.183, -0.047, 0.], [0.183, 0.047, 0.],
                        [-0.183, -0.047, 0.], [-0.183, 0.047, 0.]
                        ]) + COM_OFFSET
# HIP_OFFSETS = np.array([[0.1805, -0.047, 0.], [0.1805, 0.047, 0.],
#                         [-0.1805, -0.047, 0.], [-0.1805, 0.047, 0.]
#                         ]) + COM_OFFSET
# print(HIP_OFFSETS)
_motor_offset= np.array([ [0.,  -0.6,   0.66],[  0.,   -0.6,   0.66], [ 0.,   -0.6,   0.66], [ 0.,   -0.6,   0.66]])
_motor_direction= np.array([[-1,  1,  1],  [1,  1,  1], [-1,  1,  1],  [1,  1,  1]])

# ik2
def foot_position_in_hip_frame_to_joint_angle(foot_position, l_hip_sign=1):
    l_up = 0.2
    l_low = 0.2
    l_hip = 0.08505 * l_hip_sign
    x, y, z = foot_position[0], foot_position[1], foot_position[2]
    # print(l_hip)
    theta_knee = -np.arccos(
        (x**2 + y**2 + z**2 - l_hip**2 - l_low**2 - l_up**2) /(2 * l_low * l_up))
    l = np.sqrt(l_up**2 + l_low**2 + 2 * l_up * l_low * np.cos(theta_knee))
    # print(l)
    theta_hip = np.arcsin(-x / l) - theta_knee / 2
    c1 = l_hip * y - l * np.cos(theta_hip + theta_knee / 2) * z
    s1 = l * np.cos(theta_hip + theta_knee / 2) * y + l_hip * z
    c=np.cos(1)
    print(c1,s1,c)
    theta_ab = np.arctan2(s1, c1)
    return np.array([theta_ab, theta_hip, theta_knee])


# ik1
def ComputeMotorAnglesFromFootLocalPosition( leg_id,
                                            foot_local_position):
    """Use IK to compute the motor angles, given the foot link's local position.

    Args:
      leg_id: The leg index.
      foot_local_position: The foot link's position in the base frame.

    Returns:
      A tuple. The position indices and the angles for all joints along the
      leg. The position indices is consistent with the joint orders as returned
      by GetMotorAngles API.
    """
    # assert len(_foot_link_ids) == 4
    # toe_id = self._foot_link_ids[leg_id]

    motors_per_leg = 3
    joint_position_idxs = [0,1,2,3,4,5,6,7,8,9,10,11]
    joint_angles = foot_position_in_hip_frame_to_joint_angle(
                foot_local_position - HIP_OFFSETS[leg_id],
                l_hip_sign=(-1)**(leg_id+1))

    # Joint offset is necessary for Laikago.
    # joint_angles = np.multiply(
    #         np.asarray(joint_angles) -
    #         np.asarray(_motor_offset)[joint_position_idxs[leg_id]],
    #         _motor_direction[joint_position_idxs[leg_id]])

    # Return the join index (the same as when calling GetMotorAngles) as well
    # as the angles.
    return  joint_angles.tolist()
# //fk
def foot_position_in_hip_frame(angles, l_hip_sign=1):
    theta_ab, theta_hip, theta_knee = angles[0], angles[1], angles[2]
    l_up = 0.2
    l_low = 0.2
    l_hip = 0.08505 * l_hip_sign
    leg_distance = np.sqrt(l_up**2 + l_low**2 +
                           2 * l_up * l_low * np.cos(theta_knee))
    eff_swing = theta_hip + theta_knee / 2

    off_x_hip = -leg_distance * np.sin(eff_swing)
    off_z_hip = -leg_distance * np.cos(eff_swing)
    off_y_hip = l_hip

    off_x = off_x_hip
    off_y = np.cos(theta_ab) * off_y_hip - np.sin(theta_ab) * off_z_hip
    off_z = np.sin(theta_ab) * off_y_hip + np.cos(theta_ab) * off_z_hip
    return np.array([off_x, off_y, off_z])


if __name__ == '__main__':
    leg=[0,1,2,3]
    foot_position=[[0.16840759, -0.13204999, -0.32405686],
                    [0.16840759, 0.13204999, -0.32405686],
                    [-0.19759241, -0.13204999, -0.32405686],
                    [-0.19759241, 0.13204999, -0.32405686]]
    for i in {0,1,2,3}:
        jointangle=ComputeMotorAnglesFromFootLocalPosition( leg[i],foot_position[i])
        print(jointangle)
        position=foot_position_in_hip_frame(np.multiply(np.array(jointangle+_motor_offset[i]),_motor_direction[i]), l_hip_sign=(-1)**(leg[i]+1))

        # print(position)
    # angle=foot_position_in_hip_frame_to_joint_angle(foot_position[0],1)
    # print(angle)
    # position=foot_position_in_hip_frame(angle,1)
        position=position+HIP_OFFSETS[i]
        # print(position)