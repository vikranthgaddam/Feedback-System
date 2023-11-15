
import math
import numpy as np

SamplingInterval = None # Sampling interval - defaults to None, must be set explicitly

# ============================================================
# Controllers

'''
    Include your controller(s) code here
'''
class PController:
    def __init__(self, goal, p=2):
        self.p = p  # Proportional gain
        self.goal = goal  # Desired goal (setpoint)

    def next(self, output):
        error = self.goal - output  # Calculate the error
        control_signal = self.p * error  # Proportional control signal
        return control_signal

class PIController:
    def __init__(self, goal, p=1, i=1, dt=0.1):
        self.p = p
        self.i = i
        self.dt = dt
        self.goal = goal
        self.integral = 0

    def next(self, output):
        error = self.goal - output
        self.integral += error * self.dt
        control_signal = self.p * error + self.i * self.integral
        return control_signal

class PIDController:
    def __init__(self, goal, p=1, i=1, d=0, dt=0.1):
        self.p = p
        self.i = i
        self.d = d
        self.dt = dt
        self.goal = goal
        self.integral = 0
        self.last_error = 0

    def next(self, output):
        error = self.goal - output
        self.integral += error * self.dt
        derivative = (error - self.last_error) / self.dt
        
        control_signal = (self.p * error) + (self.i * self.integral) + (self.d * derivative)
        
        self.last_error = error
        return control_signal

# ============================================================
# # Input signals

'''
    If you test your target system with various input signals, include
    the code here. You will only invoke the input signal that you 
    finalized, when you submit your code. 
'''

# # ============================================================
# # Loop functions


def static_test(target_ctor, ctor_args, umax, steps, repeats, tmax):
    u_values = []  # Array for u values
    averaged_y_values = []  # Array for averaged y values

    for i in range(steps):
        u = float(i) * umax / float(steps)
        print("u values",u)
       # angle=(math.pi*2*i)/steps
        #u=(math.sin(angle)+1)*0.5*umax
        sum_y = 0.0

        for r in range(repeats):
            target = target_ctor(*ctor_args)
            for t in range(tmax):
                y = target.work(u)
            sum_y += y
        
        avg_y = sum_y / repeats

        u_values.append(u)
        averaged_y_values.append(avg_y)

        if avg_y >= 1.0:
            break  # Stop if y reaches or exceeds 1

    return parameter_estimation(u_values, averaged_y_values)
def parameter_estimation(u_values, averaged_y_values):
   
    u_values = np.array(u_values)
    averaged_y_values = np.array(averaged_y_values)

    mu_u = np.mean(u_values[:-1])
    mu_y = np.mean(averaged_y_values[1:])

    
    u = u_values - mu_u
    y = averaged_y_values - mu_y
    print("Y values" ,y)
    print("U values",u)


    
    S1 = np.sum(y ** 2)
    S2 = np.sum(u * y)
    S3 = np.sum(u ** 2)
    S4 = np.sum(y[:-1] * y[1:])
    S5 = np.sum(u[:-1] * y[1:])

   
    denominator = S1 * S3 - S2 ** 2
    a = (S3 * S4 - S2 * S5) / denominator
    b = (S1 * S5 - S2 * S4) / denominator
    #y(k+1)= averaged_y_values
    y_next_values = [a * y[i] + b * u[i] for i in range(len(y) - 1)]

    rmse = math.sqrt(sum((y[i] - y_next_values[i]) ** 2 for i in range(len(y_next_values))) / len(y_next_values))
    
    # Calculate R^2 value
    total_sum_of_squares = sum((y_i - mu_y) ** 2 for y_i in y[:-1])
    sum_of_squares_of_residuals = sum((y[i] - y_next_values[i]) ** 2 for i in range(len(y_next_values)))
    r_squared = 1 - (sum_of_squares_of_residuals / total_sum_of_squares)

    return  a, b ,rmse ,r_squared
def closed_loop():
    '''
        Your feedback loop code goes here
    '''
    quit()