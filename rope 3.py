import pygame as pg
import sys
pg.init()
clock=pg.time.Clock()
font = pg.font.Font(None, 50)
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
left_mouse_down=right_mouse_down=False

# parameters
scw,sch=1500,1000
segments=2
legs=8
seg_size=10
drag=0.8
gravity=-10
sr=10
step_size=200
base_max_speed=7

base=[scw//2,sch//2,0,0]
base_target_pos=[0,0]
segment=pg.rect.Rect(0,0,seg_size,seg_size)
screen=pg.display.set_mode((scw,sch))

# segment list creation
leg_target_list=[]
leg_list=[]
for i in range(legs):
    leg_target_list.append([i*scw/legs,i*sch/legs])
    leg_list.append([[0,0,0,0]for j in range(segments)])     

print(legs*segments*len(leg_list[0][0]))
while True:
    start_time = pg.time.get_ticks()
    
# drawing segments, positions and such
    screen.fill(black)   
    #for pos in leg_target_list:
    #    segment.center=(pos)
    #    pg.draw.ellipse(screen,red,segment)    
    for i in range(legs):
        seg_pos_list=[base[:2]]
        for j in range(segments):
            seg_pos_list.append(leg_list[i][j][:2])
        pg.draw.lines(screen,white,False,seg_pos_list,3)  

    segment.center=(base[0],base[1])
    pg.draw.ellipse(screen,green, segment)
    segment.center=(base_target_pos)
    pg.draw.ellipse(screen,blue, segment)
# leg movement math
    for i in range(legs):
        leg_list[i][0][0],leg_list[i][0][1]=leg_list[i][0][0]+leg_list[i][0][2],leg_list[i][0][1]+leg_list[i][0][3]
        leg_list[i][0][2]=(leg_list[i][0][2]+(((base[0]-leg_list[i][0][0])+(leg_list[i][1][0]-leg_list[i][0][0]))/sr))*drag
        leg_list[i][0][3]=(leg_list[i][0][3]+(((base[1]-leg_list[i][0][1])+(leg_list[i][1][1]-leg_list[i][0][1]))/sr))*drag+gravity
        for x in range(1,segments-1):
            leg_list[i][x][0],leg_list[i][x][1]=leg_list[i][x][0]+leg_list[i][x][2],leg_list[i][x][1]+leg_list[i][x][3]
            leg_list[i][x][2]=(leg_list[i][x][2]+(((leg_list[i][x-1][0]-leg_list[i][x][0])+(leg_list[i][x+1][0]-leg_list[i][x][0]))/sr))*drag
            leg_list[i][x][3]=(leg_list[i][x][3]+(((leg_list[i][x-1][1]-leg_list[i][x][1])+(leg_list[i][x+1][1]-leg_list[i][x][1]))/sr))*drag+gravity
        leg_list[i][-1][0]=leg_list[i][-1][0]+((leg_target_list[i][0]-leg_list[i][-1][0])/(sr/1))*drag
        leg_list[i][-1][1]=leg_list[i][-1][1]+((leg_target_list[i][1]-leg_list[i][-1][1])/(sr/1))*drag-abs(leg_target_list[i][0]-leg_list[i][-1][0])/30

# input handling
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type==pg.MOUSEBUTTONDOWN and event.button==1:
            left_mouse_down=True
        if event.type==pg.MOUSEBUTTONUP and event.button==1:
            left_mouse_down=False
        if event.type==pg.MOUSEBUTTONDOWN and event.button==3:
            right_mouse_down=True
        if event.type==pg.MOUSEBUTTONUP and event.button==3:
            right_mouse_down=False
    if left_mouse_down:
        cursor_x,cursor_y=event.pos
        base_target_pos=[cursor_x,cursor_y]
    if right_mouse_down:
        cursor_x,cursor_y=event.pos
        leg_target_list[0]=[cursor_x,cursor_y]

# base movement math
    base[2]=max(-base_max_speed,min(base_max_speed,(base[2]+(((base_target_pos[0]-base[0])+(base_target_pos[0]-base[0]))/sr))*drag*0.2))
    base[3]=max(-base_max_speed,min(base_max_speed,(base[3]+(((base_target_pos[1]-base[1])+(base_target_pos[1]-base[1]))/sr))*drag*0.2))
    base[0]+=base[2]
    base[1]+=base[3]

# leg automatic movement
    for target in leg_target_list:
        if target[0]-base[0]>0:
            target[0]-=step_size*2
        if target[0]-base[0]<-step_size*1.2:
            target[0]+=step_size*2
        if target[1]-base[1]>step_size*1.2:
            target[1]-=step_size*2
        if target[1]-base[1]<-step_size/3:
            target[1]+=step_size*2


# display related things
    clock.tick(60) 
    screen.blit((font.render("ms: "+str(pg.time.get_ticks()-start_time),True, white)),(20, 20))
    pg.display.flip() 




#  scrap yard
        #leg_list[i][-1][0],leg_list[i][-1][1]=leg_list[i][-1][0]+leg_list[i][-1][2],leg_list[i][-1][1]+leg_list[i][-1][3]
        #leg_list[i][-1][2]=(leg_list[i][-1][2]+(((leg_target_list[i][0]-leg_list[i][-1][0]))/sr))*drag
        #leg_list[i][-1][3]=(leg_list[i][-1][3]+(((leg_target_list[i][1]-leg_list[i][-1][1]))/sr))*drag    

