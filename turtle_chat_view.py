'Nisreen'


import turtle

from turtle_chat_client import Client

from turtle_chat_widgets import Button, TextInput


class TextBox(TextInput):

    def draw_box(self):

        self.draw = turtle.clone()
        self.draw.hideturtle()

        self.draw.penup()
        self.draw.goto(self.width/2,0)
        self.draw.pendown()
        self.draw.goto(-self.width/2,0)
        self.draw.goto(-self.width/2,-self.height)
        self.draw.goto(self.width/2,-self.height)
        self.draw.goto(self.width/2,0)

        self.draw_box2()

    def draw_box2(self):
        
        self.draw2 = turtle.clone()
        self.draw2.hideturtle()
        self.draw2.penup()
        self.draw2.goto(self.width/2,100)
        self.draw2.pendown()
        self.draw2.goto(-self.width/2,100)
        self.draw2.goto(-self.width/2,200)
        self.draw2.goto(self.width/2,200)
        self.draw2.goto(self.width/2,100)
    

    def write_msg(self):

        self.writer.clear()
        self.writer.pencolor('white')
        self.writer.write(self.new_msg, font = ('Times New Roman',14,'normal'))

class SendButton(Button):

    def __init__(self,view):
        super(SendButton,self).__init__(my_turtle=None,shape=None,pos=(0,-150))
        self.view=view
        
    def fun(self,x=None,y=None):
        self.view.send_msg()
        
    

class View:
    _MSG_LOG_LENGTH=5 
    _SCREEN_WIDTH=300
    _SCREEN_HEIGHT=600
    _LINE_SPACING=round(_SCREEN_HEIGHT/2/(_MSG_LOG_LENGTH+1))

    def __init__(self,username='Me',partner_name='Partner'):
        '''
        :param username: the name of this chat user
        :param partner_name: the name of the user you are chatting with
        '''
        
        self.username=username
        self.partner_name=partner_name
        self.my_client=Client()
        turtle.setup(width = self._SCREEN_WIDTH, height = self._SCREEN_HEIGHT)

        
        self.msg_queue=[]

       
        self.display=turtle.clone()
        self.display.hideturtle()
        self.display.pencolor('white')
        self.display.penup()
        self.display.goto(-90,180)

        self.background()
        
        self.textbox = TextBox()
        self.send_button = SendButton(self)

        
        self.setup_listeners()

    def background(self):

        turtle.register_shape("disney.gif")
        self.clone=turtle.clone()
        self.clone.shape("disney.gif")

        
    def send_msg(self):
        
        self.my_client.send(self.textbox.new_msg)
        self.msg_queue.insert(0,self.textbox.new_msg)
        self.textbox.clear_msg()
        self.display_msg()
        

    def get_msg(self):
        return self.textbox.get_msg()

    def setup_listeners(self):
        
        turtle.onkeypress(self.send_button.fun, 'Return')
        turtle.listen()
        

    def msg_received(self,msg):
        
        print(msg)
        show_this_msg=self.partner_name+' says:\r'+ msg
        
        self.msg_queue.insert(0,show_this_msg)
        self.display_msg()

    def display_msg(self):
       
        self.display.clear()
        self.display.write(self.msg_queue[0], ('Times New Roman',14,'normal'))

if __name__ == '__main__':
    my_view=View()
    _WAIT_TIME=200 
    def check() :
        msg_in=my_view.my_client.receive()
        if not(msg_in is None):
            if msg_in==my_view.my_client._END_MSG:
                print('End message received')
                sys.exit()
            else:
                my_view.msg_received(msg_in)
        turtle.ontimer(check,_WAIT_TIME) 
    check()
    turtle.mainloop()
