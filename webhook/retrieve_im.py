from .server import initServer, retrieve
from chatbot.settings import BASE_DIR
import os

base_path = os.path.join(BASE_DIR)


def im_retrieve():
    initServer(128, 2, "{}/Clustering_l2_1000000_13516675_128_50it.hdf5", "clusters", "{}/index.hdf5", 1000000,"{}/im_data","{}/temp_feat".
               format(base_path, base_path, base_path, base_path))


def chatbot_retrieve(im_path):
    res = retrieve(im_path, 1)
    if res[0].score() < 0.2:
        return "bla bla bla"
    product_name = res[0].name()
    product_name = product_name.split('.')[0]
    return product_name

