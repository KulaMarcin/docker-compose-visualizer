import yaml
from diagrams import Diagram, Cluster
from diagrams.generic.network import Switch
from diagrams.generic.compute import Rack

from diagrams.digitalocean.compute import Containers
from diagrams.digitalocean.storage import Volume


def draw_docker_compose_file(file_path):
    with open(file_path, "r") as file:
        docker_compose_dict = yaml.safe_load(file)
    
    print(docker_compose_dict)
    
    with Diagram("", show=False):
        services = {
            service: Containers(
                f"{service}\nPorts: {details.get('ports', 'Not specified')}\nImage: {details.get('image', 'Not specified')}"
            )
            for service, details in docker_compose_dict["services"].items()
        }
        networks = {}
        for service, details in docker_compose_dict["services"].items():
            if "links" in details:
                for link in details["links"]:
                    services[service] - Volume("LINK") - services[link]
            if "networks" in details:
                for network in details["networks"]:
                    if network not in networks:
                        networks[network] = Volume(network)
                    services[service] - networks[network]


draw_docker_compose_file("docker-compose2.yml")
