import numpy as np
from scipy.signal import savgol_filter

def detect_shock_front(density, radius_edges, time_edges, density_threshold=1.1):
    '''
    检测主冲击波界面轨迹，返回每个时刻的冲击波半径坐标数组
    - density: shape (nt, nr)
    - radius_edges: shape (nt, nr+1) 或 (nr+1, nt) 或 (nt, nr)
    - time_edges: shape (nt+1,)
    - density_threshold: 密度跳跃阈值
    返回: shock_pos, shape (nt,)
    '''
    shock_pos = []
    nt = density.shape[0]
    for t in range(nt):
        rho = density[t, :]
        grad = np.gradient(rho)
        max_neg_grad_idx = np.argmin(grad)
        rho_smooth = np.convolve(rho, np.ones(3)/3, mode='same')
        density_ratio = np.zeros_like(rho)
        for i in range(1, len(rho)-1):
            if rho_smooth[i+1] > 0:
                density_ratio[i] = rho_smooth[i-1] / rho_smooth[i+1]
        valid_indices = np.where((grad < 0) & (density_ratio > density_threshold))[0]
        if len(valid_indices) > 0:
            local_grad = grad[valid_indices]
            relative_idx = np.argmin(local_grad)
            idx = valid_indices[relative_idx]
        else:
            idx = max_neg_grad_idx if grad[max_neg_grad_idx] < 0 else np.argmin(grad)
        idx = max(0, min(idx, len(rho)-1))
        # 计算对应的半径位置
        if radius_edges.shape[0] == density.shape[0] + 1:
            r = 0.5 * (radius_edges[t, idx] + radius_edges[t, idx+1])
        elif radius_edges.shape[1] == density.shape[0]:
            r = radius_edges[idx, t]
        else:
            r = radius_edges[t, idx]
        shock_pos.append(r)
    # 替换第一个为0
    if len(shock_pos) > 0:
        shock_pos[0] = 0
    return np.array(shock_pos)

def max_pressure(pressure, smooth=True, window_length=11, polyorder=3):
    """
    计算每个时刻的最大压力，并可选用savgol_filter平滑
    """
    max_p = np.max(pressure, axis=1)
    if smooth:
        # window_length必须为奇数且小于等于max_p长度
        wl = min(window_length, len(max_p) if len(max_p)%2==1 else len(max_p)-1)
        if wl < 3: wl = 3
        if wl % 2 == 0: wl += 1
        return savgol_filter(max_p, window_length=wl, polyorder=polyorder)
    return max_p

def max_density(mass_density, smooth=True, window_length=11, polyorder=3):
    """
    计算每个时刻的最大质量密度，并可选用savgol_filter平滑
    """
    max_d = np.max(mass_density, axis=1)
    if smooth:
        wl = min(window_length, len(max_d) if len(max_d)%2==1 else len(max_d)-1)
        if wl < 3: wl = 3
        if wl % 2 == 0: wl += 1
        return savgol_filter(max_d, window_length=wl, polyorder=polyorder)
    return max_d 