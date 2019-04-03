import os

CURRENTDIR = os.path.dirname(__file__)
DEPLOYMDIR = os.path.join(CURRENTDIR, "../deployments")


def start(type):
    all_files = os.listdir(DEPLOYMDIR)
    # filter only matched keyword
    selected_configs = [f for f in all_files if type in f]
    for selected_config in selected_configs:
        run(selected_config)


def run(configure_name):
    os.system("kubectl apply -f " + os.path.join(DEPLOYMDIR, configure_name))


# currently there are persistent_volume, deployment
start("persistent_volume")
