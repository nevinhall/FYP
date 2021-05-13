import sign_up_rpc_impl
import login_rpc_impl

from threading import Thread
def laucnher():
    print("Launching sigup")

Thread(target=sign_up_rpc_impl).start()
Thread(target=login_rpc_impl).start()



if __name__ == '__main__':
    laucnher()


