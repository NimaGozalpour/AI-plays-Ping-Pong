import pygame
import time
import random
import math
import numpy as np
import random
np.random.seed(293423)

#GA Parameter
pop=10

#neural hyper parameter
input_num=2
bais=True
hidden_neuron=10
if bais:
    weight_num=(input_num+1)*hidden_neuron+hidden_neuron+1
else:
    weight_num=input_num*hidden_neuron+hidden_neuron
    
pygame.init()
display_width=900
display_height=700

white=(255,255,255)
black=(0,0,0)
red=(255,0,0)

gamedisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Ping Pong')
clock=pygame.time.Clock()

#table
tableImg=pygame.image.load('table_2.png')
(a,b)=tableImg.get_rect().size
tableImg= pygame.transform.scale(tableImg, (math.floor(a*0.4),math.floor(b*0.4)))
(table_w,table_h)=tableImg.get_rect().size

#red rocket
redImg=pygame.image.load('Red_Rocket.png')
(a,b)=redImg.get_rect().size
redImg= pygame.transform.scale(redImg, (math.floor(a*0.4),math.floor(b*0.4)))
(red_w,red_h)=redImg.get_rect().size

#ball
ballImg=pygame.image.load('Ball.png')
(a,b)=ballImg.get_rect().size
ball= pygame.transform.scale(ballImg, (math.floor(a*0.4),math.floor(b*0.4)))
(ball_w,ball_h)=ballImg.get_rect().size



def img_draw(img,x,y):
    gamedisplay.blit(img,(x,y))


def thing_point(count,genaration,num_c):
    font=pygame.font.SysFont(None,25)
    text=font.render('point: '+str(count),True,white)
    gamedisplay.blit(text,(0,0))
    text=font.render('genaration: '+str(genaration),True,white)
    gamedisplay.blit(text,(0,30))
    text=font.render('choromosome: '+str(num_c+1),True,white)
    gamedisplay.blit(text,(0,60))



def text_objects(text,font):
    textSurface=font.render(text,True,black)
    return textSurface,textSurface.get_rect()


def massage_display(text):
    largeText=pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect=text_objects(text,largeText)
    TextRect.center=(display_width/2,display_height/2)
    gamedisplay.blit(TextSurf,TextRect)
    
    pygame.display.update()
    time.sleep(0.5)
    

def game_over():
    massage_display('Game Over')


def game_loop(chromosome,genaration,num_c):
    table_x=display_width/2-table_w/2
    table_y=display_height/2-table_h/2
    
    
    red_x=table_x+10
    red_y=table_y+table_h/2+6

    sign_1=random.randint(0,1)
    signer=[-1,1]
    horiz=signer[sign_1]
    sign_1=random.randint(0,1)
    verti=-1
    ball_x=table_x+table_w-40
    ball_y=display_height/2+random.randint(0,20)*7

    y_changed=0
    frame_speed=240

    points=0
    gameExit= False


    distance_x_min=red_w+1
    distance_x_max=table_w-ball_w-12
    distance_y_min=-table_h+red_h+12
    distance_y_max=table_h-ball_h-16
    ball_speed=3;
    tictac=-20
    while not gameExit:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        #red_y_norm=(red_y-table_y-6)/(table_y+table_h-10-red_h-table_y-6)
        #ball_x_norm=(ball_x-red_x-red_w-1)/(table_x+table_w-2-ball_w-red_x-red_w-1)
        #ball_y_norm=(ball_y-table_y-2)/(table_y+table_h-10-ball_h-table_y-2)
        distance_x=(ball_x-red_x-distance_x_min)/(distance_x_max-distance_x_min)
        distance_y=(ball_y-red_y-distance_y_min)/(distance_y_max-distance_y_min)
        #print(distance_x*2-1,distance_y*2-1)
        if bais:
            o2=feedforward_bais(np.array([[distance_x*2-1],[distance_y*2-1]]),chromosome,input_num,hidden_neuron)
        else:
            o2=feedforward(np.array([[distance_x*2-1],[distance_y*2-1]]),chromosome,input_num,hidden_neuron)
        if o2>=0.5:
            y_changed=5
        elif o2<0.5:
            y_changed=-5
        else:
            y_changed=0
        #print(o2)
        red_y+=y_changed
        
        if red_y<table_y-red_h:
            red_y=table_y-red_h
            
            #game_over()
            #gameExit=True
            #break
            
        elif red_y>table_y+table_h-red_h+red_h:
            red_y=table_y+table_h-red_h+red_h
            
            #game_over()
            #gameExit=True
            #break
    

        if ball_x<=red_x+red_w+1:
            
            if ball_y<red_y+red_h and ball_y+ball_h>red_y:
                verti=1
                points+=1
                if points%10==0 and ball_speed<5:
                    frame_speed=math.floor(frame_speed*1.02)
                    ball_speed+=1
                    
            else:
                
                game_over()
                gameExit=True
                break
        if ball_x+ball_w>=table_x+table_w-2:
            verti=-1
        
        if ball_y<=table_y+2:
            horiz=1
        if ball_y+ball_h>=table_y+table_h-10:
            horiz=-1
        ball_x+=(verti*ball_speed)
        ball_y+=(horiz*ball_speed)
    
        
            
        gamedisplay.fill(black)
        img_draw(tableImg,table_x,table_y)
        
        img_draw(redImg,red_x,red_y)
        img_draw(ballImg,ball_x,ball_y)
        thing_point(points,genaration,num_c)
        
        pygame.display.update()
        tictac+=1
        clock.tick(frame_speed)
    
    tictac-=abs(ball_x-red_x)
    tictac-=abs(ball_y-red_y)
    tictac+=points*100
    return tictac






def crossOver(a,b):
    #k=random.randint(1,weight_num-1)
    k=random.sample(range(1, weight_num-1), 2)
    k.sort()
    child_one=np.copy(a)
    child_one[k[0]:k[1]]=np.copy(b[k[0]:k[1]])
    child_two=np.copy(b)
    child_two[k[0]:k[1]]=np.copy(a[k[0]:k[1]])
    if random.randint(0,1)==1:
         return child_one
    else:
         return child_two
    
   

def mutation(a):
    mutation_rate=0.2
    b=np.copy(a)
    for i in range(len(a)):
        if random.random()<mutation_rate:
            mute_factor=1 + (random.random()-0.5)*3+(random.random()-0.5)
            b[i]*=mute_factor
    return b
    
def selection(fitness,pop,counts):
    fitness=fitness[fitness[:,1].argsort()]
    fitness=np.copy(fitness[::-1,:])
    new_genaration=np.zeros([10,weight_num])
    if counts==1 and fitness[0,1]<0:
        return create_pop(),fitness,1
    for i in range(4):
        new_genaration[i,:]=np.copy(pop[int(fitness[i,0])])
    
    new_genaration[4,:]=crossOver(new_genaration[1,:],new_genaration[2,:])
    a=random.sample(range(0, 4), 2)
    new_genaration[5,:]=crossOver(new_genaration[a[0],:],new_genaration[a[1],:])
    a=random.sample(range(0, 4), 2)
    new_genaration[6,:]=crossOver(new_genaration[a[0],:],new_genaration[a[1],:])
    a=random.sample(range(0, 4), 2)
    new_genaration[7,:]=crossOver(new_genaration[a[0],:],new_genaration[a[1],:])
    
    new_genaration[8,:]=np.copy(new_genaration[random.randint(0,3),:])
    new_genaration[9,:]=np.copy(new_genaration[random.randint(0,3),:])

    new_genaration[4,:]=mutation(new_genaration[4,:])
    new_genaration[5,:]=mutation(new_genaration[5,:])
    new_genaration[6,:]=mutation(new_genaration[6,:])
    new_genaration[7,:]=mutation(new_genaration[7,:])
    new_genaration[8,:]=mutation(new_genaration[8,:])
    new_genaration[9,:]=mutation(new_genaration[9,:])
    
    return new_genaration,fitness,0
    

def sigmoid(x):
    return 1/(1+np.exp(-x))
def sigmoid_two(x):
    return (1-np.exp(-x))/(1+np.exp(-x))

def feedforward(in_data,gen,input_num,hidden_neuron):
    w1=gen[:input_num*hidden_neuron].reshape((hidden_neuron,input_num))
    w2=gen[input_num*hidden_neuron:].reshape((1,hidden_neuron))
    net1=np.dot(w1,in_data)
    o1=sigmoid_two(net1)
    net2=np.dot(w2,o1)
    o2=sigmoid(net2)
    return o2

def feedforward_bais(in_data,gen,input_num,hidden_neuron):
    w1=gen[:input_num*hidden_neuron].reshape((hidden_neuron,input_num))
    b1=gen[input_num*hidden_neuron:(input_num+1)*hidden_neuron].reshape((hidden_neuron,1))
    w2=gen[(input_num+1)*hidden_neuron:(input_num+1)*hidden_neuron+hidden_neuron].reshape((1,hidden_neuron))
    b2=gen[(input_num+1)*hidden_neuron+hidden_neuron:].reshape((1,1))
    net1=np.dot(w1,in_data)+b1
    o1=sigmoid_two(net1)
    net2=np.dot(w2,o1)+b2
    o2=sigmoid(net2)
    return o2


def create_pop():
    print("New Generation on road")
    return (np.random.rand(pop,weight_num)*2-1)*0.8


def main():

    prime_pop=np.copy(create_pop())
    
    fitness=np.zeros([pop,2])
    
    
    counts=1
    iran=True
    while iran:
        fitness[:,0]=np.array(range(pop))
        for i in range(10):
            fitness[i,1]=game_loop(prime_pop[i,:],counts,i)
            print('i: '+str(fitness[i,1]))
        
        prime_pop,fitness,k=np.copy(selection(fitness,prime_pop,counts))
        print(fitness)
        if k==1:
            counts=0
        counts+=1

main()

