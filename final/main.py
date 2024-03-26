# @Author: Xiaoxiao Jiang > xjiang3@scu.edu

# @Usage
# Run 'python main.py' in terminal


from logger_helper import setup_logger
from distance_vector import DistanceVector

logger = setup_logger('csen233finalJiangXiaoxiao.log')

if __name__ == "__main__":
    net = DistanceVector()
    net.rtInit("net.json")
    net.distance_vector()

    # User input for sending data
    print("Please enter the details for sending data:")
    source_router_name = input("Enter the source router (e.g., R01): ")
    dest_router_name = input("Enter the destination router (e.g., R20): ")
    if source_router_name in net.routers and dest_router_name in net.routers:
        router = net.routers[source_router_name]
        data = router.pack(dest_router_name, False, "hello")
        logger.info(f"Router {source_router_name} is going to send data to {dest_router_name} with data: {data}")
        success = router.sendData(dest_router_name, data)
        
        if success:
            logger.info(f"Router {router.name}: Sent data to {dest_router_name} successfully!!")
        else:
            logger.info(f"Router {router.name}: Failed to send data to {dest_router_name}")
    
    else:
        print("Invalid router name(s).")

    # User decision to mark link down
    mark_down = input("Do you want to mark a link as down? (yes/no): ").lower()

    if mark_down == 'yes':

        affected_router_name = input("Enter the router to mark a link down (e.g., R01): ")

        if affected_router_name in net.routers:

            affected_router = net.routers[affected_router_name]
            logger.info(f'Router {affected_router_name} Original FIB: {affected_router.fib}')
            logger.info(f'CHOOSE THE LINK FROM: {affected_router.links}')
            down_link_name = input(f"Enter the link in {affected_router_name} to mark down (e.g., R07): ")
            
            if down_link_name in affected_router.links:

                logger.info(f"Link from {affected_router_name} to {down_link_name} marked as down")
                
                affected_router.markLinkDown(down_link_name)
                
                logger.info(f"All routers updated!!")
                logger.info(f'Router {affected_router_name} FIB after markdown: {affected_router.fib}')
                
                
                logger.info(f" ----- After markdown -----")
                logger.info(f"Router {router.name}: Sent data to {dest_router_name}")
                router = net.routers[source_router_name]
                data = router.pack(dest_router_name, False, "hello")
                router.sendData(dest_router_name, data)

            else:
                logger.error(f'{down_link_name} router not in {affected_router_name} link')
        else:
            logger.error(f'Router {affected_router_name} not found')


    logger.info(f"Program End")