import random
import matplotlib.pyplot as plt
from feedback import PController, PIController, PIDController

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

# Closed loop with PID
def closed_loop(target_completion_rate, num_servers, num_iterations,controller_type):
    server_pool = ServerPool(num_servers, complete_work, generate_work)
    completion_rates = []
    control_inputs = []
    server_counts = []
    #PI Controller Initialization
    controller = PController(goal=target_completion_rate,p=3 )
    piController = PIController(goal=target_completion_rate, p=0.6 , i=0.9, dt=1)
    pid_controller = PIDController(goal=target_completion_rate, p=0.31, i=1.01, d=0.23, dt=1)
    current_output=0

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

if __name__ == '__main__':
    '''
TA will only type "python server.py k N T C"
k - Number of time steps to simulate
N - Number of initial server instances
T - Type of test (s, c) - s = static test, c = simulate feedback-based
system
C - Controller to run (p, pi, pid)
p = proportional controller; pi = proportional-integral controller; pid =
proportional-integral-derivative controller
Note: You must handle any errors in the user input
'''

    
    global_time = 0  # Global time for generate_work function
    controller_type = "p"  # Can be 'p', 'pi', or 'pid'
    target_completion_rate = 0.9
    num_iterations = 5000
    initial_num_servers = 10

    completion_rates, control_inputs, server_counts = closed_loop( target_completion_rate, initial_num_servers, num_iterations,controller_type)
    plot_data(completion_rates, control_inputs, server_counts)


# def plot_data(completion_rates, control_inputs, server_counts):
#     time_steps = list(range(len(completion_rates)))
    
#     fig, ax1 = plt.subplots(figsize=(10, 7))

#     color = 'tab:blue'
#     ax1.set_xlabel('Time Steps')
#     ax1.set_ylabel('Completion Rate', color=color)
#     ax1.plot(time_steps, completion_rates, label='Completion Rate', color=color)
#     ax1.tick_params(axis='y', labelcolor=color)
    
#     ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#     color = 'tab:orange'
#     ax2.set_ylabel('Control Input', color=color)  # we already handled the x-label with ax1
#     ax2.plot(time_steps, control_inputs, label='Control Input', color=color)
#     ax2.tick_params(axis='y', labelcolor=color)
    
#     ax3 = ax1.twinx()  # instantiate a third axes that shares the same x-axis
#     ax3.spines['right'].set_position(('outward', 60))  # Offset the right y-axis
#     color = 'tab:green'
#     ax3.set_ylabel('Server Instances', color=color)
#     ax3.plot(time_steps, server_counts, label='Server Instances', color=color)
#     ax3.tick_params(axis='y', labelcolor=color)
    
#     fig.tight_layout()  # to ensure the right y-label is not clipped
#     plt.title('System Performance Over Time')
#     plt.show()
