# Temporal main for communication !
from Communication import com_init


com_init_obj = com_init.Com_Init(2, "test")

print(com_init_obj.get_node_nbr())

print(com_init_obj.get_text())

print(com_init_obj.get_node_ip())

