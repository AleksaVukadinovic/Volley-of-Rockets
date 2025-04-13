import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.colors as colors

def simulate_projectiles(num_projectiles, reference_v0):
    m = 0.2  # kg, mass of the projectile
    diameter = 0.025  # m, projectile diameter
    air_density = 1.293  # kg/m^3, density of air
    D = 3.0 * air_density * diameter ** 2  # air resistance prefactor
    Dm = D / m  # air resistance factor per unit mass
    g = np.array([0.0, 0.0, 9.8])  # gravity vector
    tornado_radius = 5.0  # radius of tornado in meters
    start_position = np.array([-100.0, 0.0, 0.0])  # initial position of projectile
    duration = 10.0  # simulation time in seconds
    dt = 0.001  # time step

    results = []  # all projectile paths
    v0_speeds = []  # initial speeds of all projectiles

    # Simulate reference trajectory
    v0_ref = reference_v0 * np.array([np.cos(np.pi/4), 0, np.sin(np.pi/4)])
    reference_result = simulate_trajectory(start_position, v0_ref, m, Dm, g, tornado_radius, duration, dt)
    results.append(reference_result)
    v0_speeds.append(np.linalg.norm(v0_ref))

    # Simulate additional projectiles
    for _ in range(num_projectiles):
        u0 = np.random.uniform(20, 140)
        angle = np.random.uniform(10, 90) * np.pi / 180
        v0 = u0 * np.array([np.cos(angle), 0, np.sin(angle)])
        result = simulate_trajectory(start_position, v0, m, Dm, g, tornado_radius, duration, dt)
        results.append(result)
        v0_speeds.append(np.linalg.norm(v0))

    return results, v0_speeds

def simulate_trajectory(start_position, initial_velocity, m, Dm, g, tornado_radius, duration, dt):
    n = int(round(duration / dt))
    position = np.zeros((n, 3), float)
    velocity = np.zeros((n, 3), float)
    acceleration = np.zeros((n, 3), float)
    time = np.zeros(n, float)
    position[0] = start_position
    velocity[0] = initial_velocity
    i = 1
    while (position[i-1, 2] >= 0.0) and (i < n):
        radial_distance = np.linalg.norm(position[i-1][:2])
        if radial_distance > tornado_radius:
            U = reference_v0 * (tornado_radius / radial_distance)
        else:
            U = reference_v0 * radial_distance / tornado_radius
        if radial_distance != 0.0:
            wind = U * np.array([-position[i-1, 1] / radial_distance, position[i-1, 0] / radial_distance, 0.0])
        else:
            wind = np.zeros(3)
        relative_velocity = velocity[i-1] - wind
        acc = -g - Dm * np.linalg.norm(relative_velocity) * relative_velocity
        acceleration[i] = acc
        velocity[i] = velocity[i-1] + dt * acc
        position[i] = position[i-1] + dt * velocity[i]
        time[i] = time[i-1] + dt
        i += 1
    imax = i
    return (position[:imax, 0], position[:imax, 1], position[:imax, 2])

def plot_projectiles(results, v0_speeds):
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(12, 10), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    
    norm = colors.Normalize(vmin=min(v0_speeds), vmax=max(v0_speeds))
    cmap = cm.plasma

    # Tornado base (circular disk)
    tornado_r = np.linspace(0, 5, 100)
    tornado_theta = np.linspace(0, 2*np.pi, 100)
    tornado_r, tornado_theta = np.meshgrid(tornado_r, tornado_theta)
    tornado_x = tornado_r * np.cos(tornado_theta)
    tornado_y = tornado_r * np.sin(tornado_theta)
    tornado_z = np.zeros_like(tornado_x)

    ax.plot_surface(
        tornado_x, tornado_y, tornado_z, 
        alpha=0.15, color='cyan', 
        linewidth=0, antialiased=True
    )
    
    for i, (trajectory, v0) in enumerate(zip(results, v0_speeds)):
        color = cmap(norm(v0))
        if i == 0:
            ax.plot(trajectory[0], trajectory[1], trajectory[2], color='red', linewidth=3, label='Reference trajectory')
            ax.scatter(trajectory[0][0], trajectory[1][0], trajectory[2][0], color='red', s=80, marker='o')
            ax.scatter(trajectory[0][-1], trajectory[1][-1], trajectory[2][-1], color='red', s=120, marker='x')
        else:
            ax.plot(trajectory[0], trajectory[1], trajectory[2], color=color, linewidth=1.5, alpha=0.8)
            ax.scatter(trajectory[0][-1], trajectory[1][-1], trajectory[2][-1], color=color, s=30, marker='x')
    
    resolution = 15
    x = np.linspace(-20, 20, resolution)
    y = np.linspace(-20, 20, resolution)
    x, y = np.meshgrid(x, y)
    z = np.zeros_like(x)

    uoc = np.sqrt(x**2 + y**2)
    mask = uoc > 0.01
    u = np.zeros_like(x)
    v = np.zeros_like(y)
    
    u[mask] = -y[mask] / uoc[mask] * reference_v0 * np.minimum(1, 5/uoc[mask])
    v[mask] = x[mask] / uoc[mask] * reference_v0 * np.minimum(1, 5/uoc[mask])

    ax.quiver(x, y, z, u, v, np.zeros_like(u), length=2, 
              color='cyan', alpha=0.6, arrow_length_ratio=0.3, 
              normalize=True, linewidth=1.5)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, pad=0.1, shrink=0.7, aspect=15)
    cbar.set_label('Initial speed (m/s)', fontsize=12, color='white')

    ax.set_xlabel('X [m]', fontsize=14, labelpad=10)
    ax.set_ylabel('Y [m]', fontsize=14, labelpad=10)
    ax.set_zlabel('Z [m]', fontsize=14, labelpad=10)
    ax.set_title('Simulation of projectile trajectory in a tornado vortex', fontsize=16, pad=20)
    
    ax.set_xlim(-120, 20)
    ax.set_ylim(-70, 70)
    ax.set_zlim(0, 70)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', fontsize=12)
    ax.view_init(elev=25, azim=-35)

    xx, yy = np.meshgrid(np.linspace(-120, 20, 10), np.linspace(-70, 70, 10))
    zz = np.zeros_like(xx)
    ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray')
    
    ax.text(-100, 0, 2, "Starting\nposition", color='white', fontsize=10, ha='center')
    
    plt.tight_layout()
    plt.show()

# Main program
num_projectiles = int(input("Enter the number of additional projectiles: "))
reference_v0 = 100  # m/s, reference speed
results, v0_speeds = simulate_projectiles(num_projectiles, reference_v0)
plot_projectiles(results, v0_speeds)
