## Keyboard input for Jupyter Ros 2

import sys
sys.path.append("./../jupyter-ros")
import jupyros.ros2 as jr2
from ipyevents import Event 
from ipywidgets import Output
from ipycanvas import Canvas
import rclpy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import Vector3



class key_input:
    
    #Initiate values
    def __init__(self, node, msg_type, topic):
        
        # Set default Window size and colors
        self.width = 400
        self.height = 400
        self.color = "gray"
        
        self.msg_type = msg_type
        
        
        ## Initiate values for Ipycanvas to
        self.canvas = Canvas() 
        self.canvas.fill_style = "gray"
        self.canvas.fill_rect(0, 0, self.width , self.height)
                     
        self.out = Output()
        
        
        self.angle = 0;
        self.lin = 0;
        
        self.angle_vel = 0;
        self.lin_vel = 0;
        
        
        twist = Twist
        Twistmsg = twist()
        self.Twistmsg = Twist()
        
        ## Tuple binding
        ## [0] angular increment
        ## [1] linear increment
        ## [2] absolute angular position
        ## [3] Stamped (For future development)
        self.turtle_bindings = {
            'ArrowLeft' :       (       1,      0,      "c",     1),
            'ArrowRight':       (       -1,     0,      "c",     1),     
            'ArrowUp'   :       (       0,      1,      "c",     1),
            'ArrowDown' :       (       0,      -1,     "c",     1),
            'g'         :       (       0,      0,       0,     0),
            'G'         :       (       0,      0,       0,     0),
            't'         :       (       0,      0,      0.7854, 0),     
            'T'         :       (       0,      0,      0.7854, 0),
            'r'         :       (       0,      0,      1.5708, 0),
            'R'         :       (       0,      0,      1.5708, 0),
            'e'         :       (       0,      0,      2.3562, 0),
            'E'         :       (       0,      0,      2.3562, 0),
            'd'         :       (       0,      0,      3.1416, 0),
            'D'         :       (       0,      0,      3.1416, 0),
            'c'         :       (       0,      0,      -2.3562,        0),
            'C'         :       (       0,      0,      -2.3562,        0),
            'v'         :       (       0,      0,      -1.5708, 0),
            'V'         :       (       0,      0,      -1.5708, 0),
            'b'         :       (       0,      0,      -0.7854, 0), 
            'B'         :       (       0,      0,      -0.7854, 0),
            'f'         :       (       0,      0,      0,      0),             
            'F'         :       (       0,      0,      0,      0),
            'q'         :       (       0,      0,      0,      -1),
            'Q'         :       (       0,      0,      0,      -1),

        }

        
        
        
        
        #Using the Ros2 Jupyros Publisher module, create 
        self.key_in = jr2.Publisher(node, msg_type, topic)
        
    # Method to change the window color
    def set_color(self, color):
        self.color = color
    
    
    # Method to change the window width
    def set_width(self, width):
        self.width = width
    
    # Method to change the window height
    def set_height (self, height):
        self.height = height
    
    
    
    
   
        
    def decode(self, key):
        
        if(key not in self.turtle_bindings):
            return 0
        else:
            keycode = self.turtle_bindings[key]
            if(keycode[2] == "c"):
                self.Twistmsg.linear.x += float(keycode[0])
                self.Twistmsg.angular.z += float(keycode[1])
            else:
                self.Twistmsg.angular.z = float(keycode[2])
        return self.Twistmsg    
            
            
            
            
  

    # method to display the screen and to receive keyboard inputs
    def display(self, print_outgoing_msg = None):
        
        if(print_outgoing_msg == None):
            print_outgoing_msg =  False
            
        @self.out.capture()
        def on_keyboard_event(key, shift_key, ctrl_key, meta_key):
            if(self.msg_type == Twist):
                if (key):
                    if(print_outgoing_msg ==  True):
                        print("Keyboard event:", key)
                    self.decode(key)

                    self.key_in.send_msg(self.Twistmsg, print_msg = False)               
            else:
                if (key):
                    if(print_outgoing_msg ==  True):
                        print("Keyboard event:", key)
                    self.key_in.send_msg(str(key), print_msg = print_outgoing_msg)
                
        self.canvas.on_key_down(on_keyboard_event)
        display(self.canvas)
        display(self.out)
        
        
        
    
    
    
     
    
    
    
