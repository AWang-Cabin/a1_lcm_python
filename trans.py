import numpy as np

class FTG(object):
    def __init__(self,):
        # self.phi_range = [0,2*np.pi]
        self.f_0 = np.array([1.25])
        # self.phi_0 = 2*np.pi*np.random.random(size=4)
        phi_fr_rl = np.squeeze(2*np.pi*np.random.random(size=1))
        # phi_fl_rr = np.squeeze(2 * np.pi * np.random.random(size=1))
        self.phi_0 = np.array([phi_fr_rl,phi_fr_rl+np.pi,phi_fr_rl+np.pi,phi_fr_rl])
        self.phi = self.phi_0
        self.h = np.array([0.2])
        self.z_H = np.array([0.648])
        # self.z_H = np.array([-0.324])
        # self.foot_position_targets = np.array([0.16840759, -0.13204999, -0.32405686,
        #                                        0.16840759, 0.13204999, -0.32405686,
        #                                        -0.19759241, -0.13204999, -0.32405686,
        #                                        -0.19759241, 0.13204999, -0.32405686])


    def HorizonToBodyFrame(self,foot_pos_horizon,rpy):
        r,p,y = rpy
        R_p = np.array([[np.cos(p),0,np.sin(p)],
                        [0,1,0],
                        [-np.sin(p),0,np.cos(p)]])
        R_r = np.array([[1,0,0],
                        [0,np.cos(r),-np.sin(r)],
                        [0,np.sin(r),np.cos(r)]])
        H_B_R = np.dot(R_p, R_r)

        H_B_T = np.zeros(shape=(4, 4))
        H_B_T[0:3, 0:3] = H_B_R
        H_B_T[3, 3] = 1

        foot_pos_body = np.zeros(shape=12)
        for i in range(4):
            L_half = 0.#183
            W_half = 0.#047+0.08505
            H_z_offset = 0
            # if i in [0,1]:
            #     L_half *= -1
            # if i in [1,3]:
            #     W_half *= -1
            H_B_P = np.array([L_half, W_half, H_z_offset]).T
            H_B_T[0:3, 3] = H_B_P
            B_H_T=np.linalg.inv(H_B_T)#1204
            H_P_augmented = np.hstack((foot_pos_horizon[3*i:3*(i+1)],np.array([1]))).T
            # print(B_H_T)
            B_P_augmented = np.dot(B_H_T,H_P_augmented)
            B_P = B_P_augmented[:3]
            foot_pos_body[3*i:3*(i+1)] = B_P
        return foot_pos_body



if __name__ == '__main__':


    foot_pos_horizon = np.array([0,1,1,0,1,1,0,1,1,0,1,1])
        # ([0.16840759, -0.13204999, -0.32405686,
        #                          0.16840759, 0.13204999, -0.32405686,
        #                          -0.19759241, -0.13204999, -0.32405686,
        #                          -0.19759241, 0.13204999, -0.32405686])
    #([1,0,1,1,0,1,1,0,1,1,0,1])
    #

    rpy = np.array([0,0,np.pi/4]).T
    for i in [0,3,6,9]:
        L_half = 0.#183
        W_half = 0.#047 + 0.08505
        # if i in [6,9]:
        #     L_half *= -1
        # if i in [0,6]:
        #     W_half *= -1
        foot_pos_horizon[i] -= L_half
        foot_pos_horizon[i+1] -= W_half

    print(foot_pos_horizon)
    ftg = FTG()
    foot_pos_body = ftg.HorizonToBodyFrame(foot_pos_horizon,rpy)
    print(foot_pos_body)