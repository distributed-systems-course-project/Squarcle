from squarcle_data import squarcle_data

data = squarcle_data()
##Launch the communication thread here


##once launched, and number of nodes is known in the communication thread, call set_parameters
##Also you need to decide a unique ID for each node, this could be ordering by connection time, like 0, 1, 2 depending on connecting rank
data.set_parameters(5, 1)



##GUI continues
#first thing, set name once u get it from user
data.lock.acquire()
data.set_name("myName")
data.lock.release()


