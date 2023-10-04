import subprocess

def get_gpu_info(partition):
    cmd = f"sinfo -p {partition} -o '%.10R %.8D %.10m %.5c %7z %8G %130f %N'"
    result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')[1:]  # Skip the header line
    gpu_info = []
    for line in result:
        parts = line.split()
        node = parts[-1]
        features = parts[-2]
        
        # Extract GPU model and RAM from features
        gpu_model = None
        gpu_ram = None
        for feature in features.split(','):
            if "GPU_SKU:" in feature:
                gpu_model = feature.split("GPU_SKU:")[1]
            if "GPU_MEM:" in feature:
                gpu_ram = feature.split("GPU_MEM:")[1]
        
        if gpu_model and gpu_ram:
            gpu_info.append((partition, node, gpu_model, gpu_ram))
        else:
            print(f"Could not extract GPU information for node {node} in partition {partition}")
            
    return gpu_info

all_gpu_info = []
partitions = ["kobilka", "rondror", "cobarnes", "gpu"]
for partition in partitions:
    all_gpu_info.extend(get_gpu_info(partition))

# Print the GPU information
print("\nGPU Information:")
for partition, node, gpu_model, gpu_ram in all_gpu_info:
    print(f"Partition: {partition}, Node: {node}, GPU Model: {gpu_model}, GPU RAM: {gpu_ram}")


