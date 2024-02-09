import yaml
from diagrams import Diagram
from diagrams.digitalocean.compute import Containers
from diagrams.digitalocean.storage import Volume


def draw_docker_compose_file(file_path):
    try:
        with open(file_path, "r") as file:
            docker_compose_dict = yaml.safe_load(file)

        with Diagram("", show=False):
            services = {
                service: Containers(
                    f"{service}\nPorts: {details.get('ports', 'Not specified')}\nImage: {details.get('image', details.get('build', 'Not specified'))}",
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

            print("Diagram generated successfully! Check digrams_image.png")
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
    except yaml.YAMLError:
        print(f"ERROR: Error parsing YAML file: {file_path}")
    except Exception as e:
        print(f"ERROR: Problem with YAML structure")


if __name__ == "__main__":
    draw_docker_compose_file("docker-compose.yml")
