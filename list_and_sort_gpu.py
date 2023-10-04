import subprocess

# Fetch GPU information using sinfo
partitions = ["kobilka", "rondror", "barnes", "gpu", "owners"]
cmd_template = 'sinfo -p {} -o "%.10R %N %.130f"'

all_gpu_info = []

for partition in partitions:
    cmd = cmd_template.format(partition)
    result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')[1:]
    for line in result:
        partition_name, node, features = line.split()
        if "GPU_SKU:" in features and "GPU_MEM:" in features:
            gpu_model = features.split("GPU_SKU:")[1].split(",")[0]
            gpu_ram = features.split("GPU_MEM:")[1].split(",")[0]
            all_gpu_info.append(f"Partition: {partition_name}, Node: {node}, GPU Model: {gpu_model}, GPU RAM: {gpu_ram}")

# Define a ranking for the GPUs
gpu_ranking = {
    "A100_SXM4": 1,
    "A100_PCIE": 2,
    "V100S_PCIE": 3,
    "V100_SXM2": 4,
    "V100_PCIE": 5,
    "A40": 6,
    "RTX_3090": 7,
    "TITAN_V": 8,
    "RTX_2080Ti": 9,
    "TITAN_Xp": 10,
    "P100_PCIE": 11,
    "P40": 12
}

# Sort the data based on GPU ranking
sorted_gpu_info = sorted(all_gpu_info, key=lambda x: gpu_ranking[x.split("GPU Model: ")[1].split(",")[0]])

# Print the sorted list
for entry in sorted_gpu_info:
    print(entry)

