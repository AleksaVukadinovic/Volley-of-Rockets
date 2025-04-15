# Tornado Projectile Simulation

This project is a **3D simulation of projectile motion influenced by a tornado vortex**, created as part of the **"Introduction to Mechanics" course** at the **Faculty of Mathematics, University of Belgrade**. It was developed by a team of two students: **Aleksa Vukadinović** and **Masa Lazić**, to explore and visualize complex motion under the influence of wind and air resistance.

## 🌀 Overview

The simulation models the motion of multiple projectiles launched into a **tornado-like wind field**, taking into account:

- **Gravitational acceleration**
- **Air resistance (drag force)**
- **Wind velocity field (circular, tornado-shaped vortex)**

Each projectile has randomized initial speed and launch angle (except for one reference projectile), and their resulting trajectories are visualized in a 3D plot.

The tornado's wind behaves as a **circular vector field** that varies depending on the projectile's distance from the tornado's center. The airflow is modeled to decrease outside the tornado's radius and increase inside it.

---

## 📸 Example Output

The simulation produces a 3D plot where:

- The **reference trajectory** is highlighted in **red**.
- All other projectiles are colored based on their **initial speed**.
- The **impact points** are marked with crosses.
- A **circular tornado disk** and **vector field arrows** represent the wind field.

---

## 📦 Features

- Accurate modeling of **drag force** proportional to velocity squared.
- Realistic tornado wind model using a radial vector field.
- Clear 3D visualization of all trajectories and wind field.
- Color-mapped initial speeds with a legend.
- Interactive view using `matplotlib`’s 3D toolkit.

---

## 🚀 How to Run

### 1. Requirements

Make sure you have **Python 3.x** installed with the following libraries:

```bash
pip install numpy matplotlib
```

### 2. Run the Simulation

```bash
python simulation.py
```

You'll be prompted to enter the number of additional projectiles to simulate:

```txt
Enter the number of additional projectiles: 15
```

After input, the simulation will run and a 3D plot will be displayed.

## ⚙️ Parameters Used

| Parameter      | Value       | Description                               |
| -------------- | ----------- | ----------------------------------------- |
| m              | 0.2 kg      | Mass of each projectile                   |
| diameter       | 0.025 m     | Diameter of the projectile                |
| air_density    | 1.293 kg/m³ | Air density at sea level                  |
| tornado_radius | 5 m         | Radius of the tornado vortex              |
| reference_v0   | 100 m/s     | Initial speed of the reference projectile |
| dt             | 0.001 s     | Time step for simulation                  |
| duration       | 10 s        | Total simulation time                     |

---

## 🧠 Concepts Demonstrated

Newton's second law applied in 3D with variable forces

Effects of drag force on trajectory (nonlinear ODE)

Interaction of projectiles with a simulated vortex flow

3D vector field representation and particle trajectory analysis

---

## 👨‍🏫 Academic Context

This project was completed as part of the "Introduction to Mechanics" course during the 2rd year of undergraduate studies. It was a team project by three students, aiming to bridge programming with physical modeling and numerical simulation techniques.
