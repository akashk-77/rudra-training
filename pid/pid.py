import numpy as np
import matplotlib.pyplot as plt

class PIDController:
    def __init__(self, Kp, Ki, Kd, dt):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.integral = 0.0
        self.previous_error = 0.0

    def compute(self, setpoint, measured_value):
        error = setpoint - measured_value
        self.integral += error * self.dt
        derivative = (error - self.previous_error) / self.dt
        self.previous_error = error
        
        # Control Law
        u = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
        return u

# --- Simulation Setup ---
dt = 0.01          # Time step (seconds)
time = np.arange(0, 5, dt)

# Tuned for Realistic Damped Oscillation:
# Kp high enough to overshoot, Ki removes gravity offset, Kd provides physical damping
pid = PIDController(Kp=150.0, Ki=80.0, Kd=4.0, dt=dt)

setpoint = np.pi / 6  # ~0.523599 rad (30 degrees)
theta = 0.0
theta_dot = 0.0

# Initialize error to prevent initial derivative kick spike
pid.previous_error = setpoint - theta

theta_history = []
force_history = []

print(f"Target Setpoint: {setpoint:.6f} rad (30.0 degrees)\n")
print(f"{'Time (s)':<10} | {'Angle (rad)':<15} | {'Error (e_t)':<15} | {'Control Force':<15}")
print("-" * 62)

for t in time:
    force = pid.compute(setpoint, theta)
    error = setpoint - theta
    
    theta_history.append(theta)
    force_history.append(force)
    
    if np.isclose(t % 0.1, 0.0, atol=1e-5):
        print(f"{t:<10.2f} | {theta:<15.6f} | {error:<15.6f} | {force:<15.6f}")
    
    # Physics: Pendulum acceleration with physical rotational friction/damping
    damping_friction = 0.5 * theta_dot
    theta_accel = force - 9.81 * np.sin(theta) - damping_friction
    
    # Euler Integration
    theta_dot += theta_accel * dt
    theta += theta_dot * dt

# --- Plotting Results ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# Plot 1: Damped Oscillation Angle
ax1.plot(time, theta_history, label="Actual Angle (rad)", color="tab:orange", linewidth=2)
ax1.axhline(setpoint, color="black", linestyle="--", alpha=0.7, label="Target Setpoint (30°)")
ax1.set_ylabel("Angle (rad)")
ax1.set_title("Realistic PID Response: Damped Oscillation to 30° Setpoint")
ax1.grid(True)
ax1.legend()

# Plot 2: Control Effort
ax2.plot(time, force_history, label="Control Force (N)", color="tab:blue")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Force (N)")
ax2.grid(True)
ax2.legend()

plt.tight_layout()

output_file = "pid_plot.png"
plt.savefig(output_file, dpi=300)
print(f"\n[+] Graph successfully saved to {output_file}")
