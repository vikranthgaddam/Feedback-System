import random
import matplotlib.pyplot as plt
from feedback import PController, PIController, PIDController 
import feedback as fb

'''
    Feedback structure code. You can use multiple source-codes for each of the controllers.
    Import all the source-codes in this code
'''


class AbstractServerPool:
    def __init__(self, n, server, client):
        self.n = n           # number of server instances to start with
        self.n_requests = 0  # number of arriving requests
        self.server = server # server work function
        self.client = client # queue-loading work function

    def work(self, u):
        self.n = max(0, int(round(u))) # server count: non-negative integer
        completed = 0
        for _ in range(self.n):
            completed += self.server() # each server does some amount of work
            if completed >= self.n_requests:
                completed = self.n_requests
                break
        self.n_requests -= completed
        return completed

    def monitoring(self):
        # Dummy implementation; replace with actual completion rate retrieval
        return random.random()

# Server Pool
class ServerPool(AbstractServerPool):
    def work(self, u):
        load = self.client()
        self.n_requests = load
        if load == 0:
            return 1
        completed = super().work(u)
        return completed/load

def generate_work():
    global global_time
    global_time += 1
    if global_time > 2500:
        return random.gauss(1600, 10)
    if global_time > 2200:
        return random.gauss(1000, 10)
    return random.gauss(1300, 10)

def complete_work():
    a, b = 20, 3
    return 100*random.betavariate(a, b)

def static_test( traffic ):
    def generate_work():
        return random.gauss( traffic, traffic/200 )
    a,b,rmse,r_squared=fb.static_test(ServerPool, (0, complete_work, generate_work),20, 20, 5, 1000) # max u, steps, trials, timesteps
    print(a,b,rmse,r_squared)

# Closed loop with PID
def closed_loop(target_completion_rate, num_servers, num_iterations,controller_type):
    server_pool = ServerPool(num_servers, complete_work, generate_work)
    completion_rates = []
    control_inputs = []
    server_counts = []
    #Controller Initialization
    controller = PController(goal=target_completion_rate,p=2.4)
    piController = PIController(goal=target_completion_rate, p=0.6 , i=0.9, dt=1)
    pid_controller = PIDController(goal=target_completion_rate, p=0.31, i=1.01, d=0.23, dt=1)
    current_output=num_servers

    for _ in range(num_iterations):
        if controller_type == 'p':
            control_signal = controller.next(current_output)
        elif controller_type == 'pi':
            control_signal = piController.next(current_output)
        elif controller_type == 'pid':
            control_signal = pid_controller.next(current_output)
        else:
            raise ValueError("Invalid controller type specified")

        current_output=server_pool.work(control_signal)

        completion_rates.append(current_output)
        control_inputs.append(control_signal)
        server_counts.append(server_pool.n)

    return completion_rates, control_inputs, server_counts

# Plotting function
def plot_data(completion_rates, control_inputs, server_counts):
    time_steps = list(range(len(completion_rates)))
    
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    axs[0].plot(time_steps, completion_rates, label='Completion Rate')
    axs[1].plot(time_steps, control_inputs, label='Control Input', color='orange')
    axs[2].plot(time_steps, server_counts, label='Server Instances', color='green')

    for ax in axs:
        ax.set_xlabel('Time Steps')
        ax.grid(True)
        ax.legend()
    axs[0].set_ylabel('Completion Rate')
    axs[1].set_ylabel('Control Input')
    axs[2].set_ylabel('Server Instances')
    axs[0].set_title('Completion Rate vs. Time Steps')
    axs[1].set_title('Control Input vs. Time Steps')
    axs[2].set_title('Server Instances vs. Time Steps')
    plt.tight_layout()
    plt.show()

import sys


if __name__ == '__main__':
    # Check if the correct number of arguments is passed
    if len(sys.argv) != 5:
        print("Usage: python server.py k N T C")
        sys.exit(1)

    try:
        # Parse command-line arguments
        num_iterations = int(sys.argv[1])  # k - Number of time steps to simulate
        initial_num_servers = int(sys.argv[2])  # N - Number of initial server instances
        test_type = sys.argv[3]  # T - Type of test (s for static, c for closed-loop)
        controller_type = sys.argv[4]  # C - Controller to run (p, pi, pid)

        # Validate test type
        if test_type not in ('s', 'c'):
            raise ValueError("Invalid test type. Use 's' for static or 'c' for closed-loop.")

        # Validate controller type
        if controller_type not in ('p', 'pi', 'pid'):
            raise ValueError("Invalid controller type. Use 'p', 'pi', or 'pid'.")
        target_completion_rate = 0.9
        global_time = 0

        # Depending on the test type, run static test or closed-loop simulation
        if test_type == 's':
            static_test(1000)
        else:
            completion_rates, control_inputs, server_counts = closed_loop(target_completion_rate, initial_num_servers, num_iterations, controller_type)
            plot_data(completion_rates, control_inputs, server_counts)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
