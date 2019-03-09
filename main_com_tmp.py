# Temporal main for communication !
from Communication import com_init


com_init_obj = com_init.Com_Init()

print(com_init_obj.get_node_ip())

print(com_init_obj.get_node_nbr())

print(com_init_obj.get_node_tcp_port())

print(com_init_obj.get_can_play())