import rospy
from std_msgs.msg import String


def serialCallbackDrive(data):
	global drive_msg
	drive_msg = data.data

def serialCallbackArm(data):
	global arm_msg
	arm_msg = data.data

def main():

    global drive_msg
    global arm_msg

    rospy.Subscriber("/serial/drive", String, serialCallbackDrive)
    rospy.Subscriber("/serial/robotic_arm", String, serialCallbackArm)

    encoder_drive = rospy.Publisher("/position/drive", String, queue_size=10)
    encoder_arm = rospy.Publisher("/position/robotic_arm", String, queue_size=10)

    while not rospy.is_shutdown():
	    drive_length= len(drive_msg)
	    arm_length= len(arm_msg)


	    # eğer data 18 basamaklı ise buraya düşer

	    if(drive_length==18 and drive_msg[0].lower() == 'a' and drive_msg[17].lower() == 'b'):   #/serial/drive
	                
	        serial_drive = drive_msg[1:17]
	              
	        print("serial_drive : " , serial_drive)
	        
	        processed_data_drive = []

	        for i in range(4):          #Loop for number of data groups
	            serial_data = serial_drive[i*4:i*4+4]
	            

	            if(serial_data[0] == "0"):
	                processed_data_drive.append("+")
	            elif(serial_data[0] == "1"):
	                processed_data_drive.append("-")
	            else:
	                print("Data sign is neither 0 or 1, wrong data..")
	                return
	        
	            if(int(serial_data[1:4]) > 255):
	                temp = "255"
	            else:
	                temp = serial_data[1:4]

	            processed_data_drive.append(temp)
	            processed_data_drive.append(" ")
	        
	        published_data_drive = ''.join(processed_data_drive)
	        encoder_drive.publish(published_data_drive)					#Publish Drive data
	        print("Published Data (/serial/drive):",published_data_drive)

	    else:
	        print("Sensor data is wrong")
	        return
	            
	    if(arm_length==26 and arm_msg[0].lower() == 'a' and arm_msg[17].lower() == 'b'):              #/serial/robotic_arm
	        
	        
	        print("26 basamaklı")
	        
	        serial_robotic_arm = arm_msg[1:25]
	                
	        print("serial_robotic_arm :" , serial_robotic_arm)
	        
	        
	        processed_data_arm = []

	        for i in range(6):          #Loop for number of data groups
	            serial_data = serial_robotic_arm[i*4:i*4+4]
	            

	            if(serial_data[0] == "0"):
	                processed_data_arm.append("+")
	            elif(serial_data[0] == "1"):
	                processed_data_arm.append("-")
	            else:
	                print("Data sign is neither 0 or 1, wrong data..")
	                return
	        
	            if(int(serial_data[1:4]) > 255):
	                temp = "255"
	            else:
	                temp = serial_data[1:4]

	            processed_data_arm.append(temp)
	            processed_data_arm.append(" ")
	        
	        published_data_arm = ''.join(processed_data_arm)
	        encoder_arm.publish(published_data_arm)				#Publish Arm data
	        print("Published Data (/serial/robotic_arm):",published_data_arm)

	    else:
	        print("Sensor data is wrong")
	        return

    rospy.spin()

if __name__ == "__main__":
    main()