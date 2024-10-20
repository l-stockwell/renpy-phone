define nvl_mode = "phone"  ##Allow the NVL mode to become a phone conversation
define MC_Name = "MC" ##The name of the main character

transform phonePosition:
    xalign 1.0
    yalign 0.005

init -1 python:
    currentCharacter = None
    currentLine = None
    lastLine = None

    def get_mouse():
        global mouse_xy
        mouse_xy = renpy.get_mouse_pos()

    # Character callback ; Play a sound when a message is received
    def Phone_ReceiveSound(event, interact=True, **kwargs):
        if event == "show_done":
            renpy.sound.play("audio/ReceiveText.ogg")

    def Phone_SendSound(event, interact=True, **kwargs):
        if event == "show_done":
            renpy.sound.play("audio/SendText.ogg")   

    def getLastLine():
        return getattr(store, '_last_raw_what', '')

label showPhone:
    show screen PhoneHomescreen
    return

label showContacts:
    hide screen messages
    show screen PhoneContacts
    return

default mouse_xy = (0, 0)


# Phone Homescreen
screen PhoneHomescreen(): 
    zorder 1
    modal True
    add "UI/home_bg.png" at phonePosition

    grid 4 2:
        xalign 0.5
        yalign 2
        spacing 70
        top_margin 200
        imagebutton:
            auto "buttons/messenger_%s.png"
            action [Hide("PhoneHomescreen"), Show("PhoneContacts")]
            tooltip "Messages"

        imagebutton:
            auto "buttons/browser_%s.png"
            #action [Hide("PhoneHomescreen"),Show("settings")]
            tooltip "Internet"

        imagebutton: 
            auto "buttons/notes_%s.png"
            #action [Hide("PhoneHomescreen"), Show("PhoneContacts")]
            tooltip "Notes"
 
        imagebutton: #settings
            auto "buttons/settings_%s.png"
            action ShowMenu("preferences")
            tooltip "Settings"

        null 

        imagebutton: 
            auto "buttons/phone_%s.png"
            #action [Hide("PhoneHomescreen"), Show("PhoneContacts")]
            tooltip "Phone"

        imagebutton:
            auto "buttons/gallery_%s.png"
            action [Hide("PhoneHomescreen"), Show("PhoneGallery")]
            tooltip "Gallery"

        null
    
    imagebutton:
        xalign 0.5
        ypos 0.96
        auto "buttons/swipe_bar_%s.png"
        action Quit(confirm = True)
    

    $ tooltip = GetTooltip()

    if tooltip:
        timer 0.1 repeat True action Function(get_mouse)
        $ mx = mouse_xy[0] - 30 # LR
        $ my = mouse_xy[1] + 30 # UD
        text tooltip:
            pos(mx, my)
            color "#fff"
            size 40
            outlines [(2, "#000005", 0, 0)]

    # Status bar
    add "UI/status_bar.png" xpos 0 ypos 0 xsize 1.0 ysize 126

# Phone contact screen
screen PhoneContacts():
    zorder 1
    modal True
    add "UI/contacts_bg.png" at phonePosition

    grid 1 3:
        top_margin 350
        spacing 10

        imagebutton:
            ysize(200)
            auto "UI/contact_bar_mom_%s.png"
            sensitive mom_enabled
            action [
                Hide("PhoneContacts"), 
                Call("character_history_load", "Mom"),
                Show("messages"),
            ]

        imagebutton:
            ysize(200)
            auto "UI/contact_bar1_%s.png"
            sensitive luci_enabled
            action [
                Hide("PhoneContacts"), 
                Call("character_history_load", "Luci"),
                Show("messages"),
            ]

        imagebutton: 
            ysize(200)
            sensitive elysia_enabled
            auto "UI/contact_bar2_%s.png"
            action [
                Hide("PhoneContacts"), 
                Call("character_history_load", "Elysia"),
                Show("messages"),
            ]

    text "[mom_status]" xpos 0.22 ypos 450 color "#E2E2E2" size 30

    text "[luci_status]" xpos 0.22 ypos 665 color "#E2E2E2" size 30

    text "[elysia_status]" xpos 0.22 ypos 880 color "#E2E2E2" size 30

    # Status bar
    add "UI/status_bar.png" xpos 0 ypos 0 xsize 1.0 ysize 126

    # Button to return
    imagebutton:
        xpos 15
        ypos 15
        auto "buttons/back_%s.png"
        action Hide("PhoneContacts"), Show("PhoneHomescreen")

# Messenger screen
screen messages(dialogue=None, items=None):
    style_prefix "phoneFrame"

    vbox:
        spacing 0

        frame:
            if items is not None and len(items) >= 2:
                ysize 1600 - (len(items) - 2) * (120 + 10) - 20 
            else:
                ymaximum 1700
            viewport:
                draggable True
                mousewheel True
                # cols 1
                yinitial 1.0
                # scrollbars "vertical"
                vbox:
                    xalign 0.5
                    null height 120
                    if dialogue is not None and items is not None:
                        use nvl_phonetext(dialogue,items)
                    null height 100
        
        # Button to progress
        if items is not None and len(items)==0: #If we don't have a menu
            button:
                padding (0,0)
                add "UI/message_bar.png"
                action RollForward()
        else:
            # Phone Menu Choice
            frame:
                background Solid("#404040")
                foreground None

                vbox:
                    yalign 0.5
                    if items is not None:
                        for i in items: #For each choice
                            button:
                                action i.action
                                xalign 0.5
                                frame:
                                    background  Solid("#eeeeee")
                                    hover_background Solid("#c5c5c5")
                                    xysize (1000,120)
                                    foreground None
                                    text i.caption:
                                        color "#000000"
                                        align (0.5,0.5)
                                        text_align 0.5
                                        size 40

    #Status bar
    add "UI/status_bar.png" xpos 0 ypos -0 xsize 1.0 ysize 126

    # Button to return
    imagebutton:
        xpos 15
        ypos 15
        auto "buttons/back_%s.png"
        action [
            Hide("messages"), 
            Show("PhoneContacts"), 
            Call("history_save", currentCharacter),
            SetVariable("currentLine", getattr(store, '_last_raw_what', ''))
        ]

# Phone text screen
screen nvl_phonetext(dialogue,items):
    style_prefix None

    python:
        print(renpy.roll_forward_info())
        if currentLine is not None:
            for line in dialogue:
                #print(line)
                if currentLine != line:
                    RollForward()
                else:
                    #print("success")
                    break                

    $ previous_d_who = None
    for id_d, d in enumerate(dialogue):
        if d.who == None: # If it's the narrator talking
            null height 30
            text d.what:
                    xalign 0.5
                    ypos 0.0
                    xsize 650
                    color "#B6C3D4"
                    text_align 0.5
                    italic True
                    size 40
                    slow_cps False
                    id d.what_id
                    if d.current and len(items)==0:
                        at message_narrator
            null height 30
        elif d.who == 'System': # If it's the system talking
            null height 30
            text d.what:
                    xalign 0.5
                    ypos 0.0
                    xsize 650
                    color "#b809F5"
                    text_align 0.5
                    size 40
                    slow_cps False
                    id d.what_id
                    if d.current and len(items)==0:
                        at message_narrator
                    at transform:
                        pause 0.5

            null height 30
        else:
            if d.who == MC_Name:
                $ message_frame = "phone_send_frame.png"
            else:
                $ message_frame = "phone_received_frame.png"

            hbox:
                spacing 10
                if d.who == MC_Name:
                    box_reverse True
                    xalign 1.0
                
                #If this is the first message of the character, show an icon
                if previous_d_who != d.who:
                    if d.who == MC_Name:
                        $ message_icon = "UI/mc_icon.png"
                    elif d.who == "Luci":
                        $ message_icon = "UI/luci_icon.png"
                    elif d.who == "Mom":
                        $ message_icon = "UI/mom_icon.png"
                    elif d.who == "Elysia":
                        $ message_icon = "UI/elysia_icon.png"
                    else:
                        $ message_icon = "phone_received_icon.png"

                    add message_icon:
                        if d.current  and len(items)==0:
                            at message_appear_icon()
                        
                else:
                    null width 107

                vbox:
                    yalign 1.0
                    if d.who != MC_Name and previous_d_who != d.who:
                        text d.who:
                            size 30
                            color "#DADADA"

                    frame:
                        padding (20,20)
                        background Frame(message_frame, 23,23,23,23)
                        # xsize 750

                        if d.current and len(items)==0:
                            if d.who == MC_Name:
                                at message_appear(1)
                            else:
                                at message_appear(-1)

                        text d.what:
                            pos (0,0)
                            # xsize 750
                            slow_cps False
                            size 45
                            

                            if d.who == MC_Name :
                                color "#FFF"
                                text_align 1.0
                                xanchor 1.0
                                xpos 1.0
                            else:
                                color "#FFF"

                                
                            id d.what_id
        $ previous_d_who = d.who
                    
style phoneFrame is default

style phoneFrame_frame:
    background "UI/base_bg.png"
    foreground "messenger_fg.png"
    
    yfill True
    xfill True
    # ysize 815
    # xsize 495

    padding (20,0)


style phoneFrame_viewport:
    yfill True
    xfill True

    # yoffset -20

style phoneFrame_vbox:
    spacing 10
    xfill True

style phoneChoice


transform phone_transform(pXalign=0.5, pYalign=0.5):
    xcenter pXalign
    yalign pYalign

transform phone_appear(pXalign=0.5, pYalign=0.5): #Used only when the dialogue have one element
    xcenter pXalign
    yalign pYalign

    on show:
        yoffset 1080
        easein_back 1.0 yoffset 0

    
transform message_appear(pDirection):
    alpha 0.0
    xoffset 50 * pDirection
    parallel:
        ease 0.5 alpha 1.0
    parallel:
        easein_back 0.5 xoffset 0

transform message_appear_icon():
    zoom 0.0
    easein_back 0.5 zoom 1.0
    

transform message_narrator:
    alpha 0.0
    yoffset -50

    parallel:
        ease 0.5 alpha 1.0
    parallel:
        easein_back 0.5 yoffset 0

screen enterName:
    add "UI/base_bg.png" at phonePosition

    vbox:
        xalign 0.5
        yalign 0.4
        text "What's your name?": 
            color "#FFF"
            size 50 
            at transform:
                    alpha 0 
                    center
                    pause 0.2
                    linear 2 alpha 1.0

        null height 30

        input default "":
            color "#d1d1d1"
            size 40
            pixel_width(800)
            value VariableInputValue("player")
            at transform:
                    center

        null height 20

        textbutton "OK":
            text_size 20
            action Hide("enterName"), Show("messages"), Jump("Mom_2")
            keysym('K_RETURN', 'K_KP_ENTER')
            at transform:
                    center

    #Status bar
    add "UI/status_bar.png" xpos 0 ypos -0 xsize 1.0 ysize 126


screen ending(endingText):
    add "UI/base_bg.png" at phonePosition

    vbox:
        xalign 0.5
        yalign 0.5
        text (endingText):
            color "#FFF"
            size 50 
            at transform:
                    alpha 0 
                    center
                    pause 0.2
                    linear 2 alpha 1.0

        null height 30

        hbox:
            xalign 0.9
            textbutton "Play again?":
                text_size 30
                action Hide("ending"), Show("messages"), Jump("start")
                at transform:
                        alpha 0 
                        center
                        pause 0.3
                        linear 2 alpha 1.0

            textbutton "Quit":
                text_size 30
                xoffset 20
                action Quit(confirm = True)
                at transform:
                        alpha 0 
                        center
                        pause 0.3
                        linear 2 alpha 1.0
