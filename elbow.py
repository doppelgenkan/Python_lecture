import numpy as np
import matplotlib.pyplot as plt

class Elbow:
    '''
    Elbowクラスのインスタンスの生成.

    Parameters
    ----------
    body_mass      : 体質量[kg]
    forearm_length : 前腕長[m]
    '''
    def __init__(self, body_mass, forearm_length): #body_massは体質量，forearm_lengthは前腕の長さ
        self.__g = 9.8
        beta, load = 0, 0 #デフォルト肩屈曲角:0°，デフォルト負荷:0kg
        m = body_mass * 0.025 #前腕と手の質量
        d = forearm_length * 0.125 #肘関節からの上腕筋の腱が付いている場所の距離
        h = forearm_length * 0.5 #肘関節から前腕と手の重心までの距離
        self.parameters = np.array([
            body_mass,         # 0: 体質量
            m,                 # 1: 前腕と手の質量
            d,                 # 2: 肘関節からの上腕筋の腱が付いている場所の距離
            h,                 # 3: 肘関節から前腕と手の重心までの距離
            forearm_length,    # 4: 前腕の長さ
            beta,              # 5: 肩屈曲角
            load               # 6: 負荷(錘質量)
        ])


    def print_parameters(self):
        '''
        Return None.
        設定されているパラメータの出力.
        '''
        print(f'体質量　: {self.parameters[0]}[kg]')
        print(f'前腕質量: {self.parameters[1]}[kg]')
        print(f'前腕長　: {self.parameters[4]}[m]')
        print(f'肩屈曲角: {self.parameters[5]}[degrees]')
        print(f'負荷　　: {self.parameters[6]}[kg]')


    def set_beta(self, new_angle): #肩屈曲角の変更
        '''
        Return None.
        肩屈曲角の変更. デフォルトは0[degrees].

        Parameters
        ----------
        new_angle : 肩屈曲角[degrees].
        '''
        self.parameters[5] = new_angle


    def set_load(self, new_load): #錘質量の変更
        '''
        Return None.
        錘質量の変更. デフォルトは0[kg].

        Parameters
        ----------
        new_load : 錘質量[kg].
        '''
        self.parameters[6] = new_load


    def torque(self, theta):
        '''
        Return float.
        肘関節トルクの回転軸成分[Nm].

        Parameters
        ----------
        theta : 肘関節屈曲角[degrees].
        '''
        m = self.parameters[1]
        h = self.parameters[3]
        l = self.parameters[4]
        beta = self.parameters[5]
        w = self.parameters[6]
        return self.__g * (m * h + w * l) * np.sin(np.radians(beta) + np.radians(theta))


    def force_mag(self, theta):
        '''
        Return float.
        上腕筋力の大きさ[N].

        Parameters
        ----------
        theta : 肘関節屈曲角[degrees].
        '''
        d = self.parameters[2]
        return self.torque(theta) / (d * np.sin(np.radians(theta)))


    def force_x(self, theta):
        '''
        Return float.
        上腕筋力のx成分[N].

        Parameters
        ----------
        theta : 肘関節屈曲角[degrees].
        '''
        beta = self.parameters[5]
        return -self.force_mag(theta) * np.sin(np.radians(beta))


    def force_y(self, theta):
        '''
        Return float.
        上腕筋力のy成分[N].

        Parameters
        ----------
        theta : 肘関節屈曲角[degrees].
        '''
        beta = self.parameters[5]
        return self.force_mag(theta) * np.cos(np.radians(beta))


    def force_vector(self, theta):
        '''
        Return 1-dim NDarray.
        上腕筋力ベクトル[N].

        Parameters
        ----------
        theta : 肘関節屈曲角[degrees].
        '''
        return np.array([self.force_x(theta), self.force_y(theta)])


    def resiatance_x(self, theta):
        '''
        Return float.
        肘関節抗力のx成分[N].

        Parameters
        ----------
        theta : 肘関節屈曲角[degrees].
        '''
        beta = self.parameters[5]
        return -self.force_x(theta)


    def resiatance_y(self, theta):
        '''
        Return float.
        肘関節抗力のy成分[N].

        Parameters
        ----------
        theta : 肘関節屈曲角[degrees].
        '''
        m = self.parameters[1]
        w = self.parameters[6]
        return (m + w)*self.__g - self.force_y(theta)


    def resiatance_mag(self, theta):
        '''
        Return float.
        肘関節抗力の大きさ[N].

        Parameters
        ----------
        theta : 肘関節屈曲角[degrees].
        '''
        return np.sqrt(self.resiatance_x(theta)**2 + self.resiatance_y(theta)**2)


    def resiatance_vector(self, theta):
        '''
        Return 1-dim NDarray.
        肘関節抗力ベクトル[N].

        Parameters
        ----------
        theta : 肘関節屈曲角[degrees].
        '''
        return np.array([self.resiatance_x(theta), self.resiatance_y(theta)])


    def allowed_angles(self):
        '''
        Return 1-dim NDarray.
        与えられた肩屈曲角に対して，可能な(1[degree]刻みの)肘関節屈曲角のNDarrayを返す.
        '''
        beta = self.parameters[5]
        if beta < 45:
            angles = np.arange(10, 136, 1)
        else:
            angles = np.arange(10, 180-beta, 1)
        return angles



def do_calc():
    body_mass = float(input('体質量[kg]を入力してください: '))
    forearm_length = float(input('前腕長[m]を入力してください : '))
    w = float(input('錘質量[kg]を入力してください: '))
    beta= float(input('肩屈曲角[degrees]を入力してください: '))
    theta = float(input('肘屈曲角[degrees]を入力してください: '))
    if beta < 0 or theta < 10 or (beta + theta) >= 180:
        print('計算ストップ：不正な角です.')
    else:
        obj = Elbow(body_mass, forearm_length)
        obj.set_beta(beta)
        obj.set_load(w)
        print('------------------')
        print('【計算結果】')
        print(f'肘関節トルクの回転軸成分[Nm]: {obj.torque(theta)}')
        print(f'上腕筋の力の大きさ[N]: {obj.force_mag(theta)}')
        print(f'肘関節抗力の大きさ[N]: {obj.resiatance_mag(theta)}')
        print(f'上腕筋の力のベクトル[N]]: {obj.force_vector(theta)}')
        print(f'肘関節抗力のベクトル[N]: {obj.resiatance_vector(theta)}')


def draw_effects():
    body_mass = float(input('体質量(kg)を入力してください: '))
    forearm_length = float(input('前腕長(m)を入力してください : '))
    w = float(input('錘質量(kg)を入力してください: '))
    beta = float(input('肩屈曲角(degrees)を入力してください: '))
    obj = Elbow(body_mass, forearm_length)
    obj.set_beta(beta)
    obj.set_load(w)
    angles = obj.allowed_angles()
    '''
    if beta < 45:
        angles = np.arange(10, 136, 1)
    else:
        angles = np.arange(10, 180-beta, 1)
    '''
    #肘関節モーメントのグラフ
    plt.figure()
    plt.plot(angles, obj.torque(angles))
    plt.xlabel('Flection angles of elbow [degrees]')
    plt.ylabel('Moment of force around elbow [Nm]')
    #前腕筋力のグラフ
    plt.figure()
    plt.plot(angles, obj.force_mag(angles))
    plt.xlabel('Flection angles of elbow [degrees]')
    plt.ylabel('Force of forearm mascle [N]')
    #肘関節筋力のグラフ
    plt.figure()
    plt.plot(angles, obj.resiatance_mag(angles))
    plt.xlabel('Flection angles of elbow [degrees]')
    plt.ylabel('Resistance of elbow [N]')
