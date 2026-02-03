import matplotlib.pyplot as plt

def plot_motion(df, state):
    plt.figure(figsize=(14,6))
    plt.plot(df["C"], color="gray", alpha=0.3)
    plt.plot(state.ML_index, state.ML, color="gold", linewidth=2)
    plt.scatter(state.TP_index, state.TP_price, color="red")
    plt.title("Akash Waves Motion Line")
    plt.show()
