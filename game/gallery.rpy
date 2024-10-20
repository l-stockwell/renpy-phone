image CG_red = "CGs/red.jpg"
image CG_blue = "CGs/blue.png"
image CG_green = "CGs/green.png"
image CG_orange = "CGs/orange.jpg"
image CG_pink = "CGs/pink.jpg"
image gallery_bg = "UI/base_bg.png"

init python:
    gallery = Gallery()

    gallery.button("red") 
    gallery.unlock_image("CG_red") 

    gallery.button("blue") 
    gallery.image("CG_blue")
    gallery.condition("persistent.blue_unlocked") 

    gallery.button("green_and_orange")
    gallery.unlock_image("CG_green")
    gallery.unlock_image("CG_orange") 

    gallery.button("green_and_orange2") 
    gallery.condition("persistent.green_unlocked and persistent.orange_unlocked") 
    gallery.image("CG_green")
    gallery.image("CG_orange") 
    gallery.image("CG_pink") 
    gallery.condition("persistent.pink_unlocked") 

screen PhoneGallery:
    zorder 1
    modal True
    add "gallery_bg" at phonePosition

    grid 4 2:
        xfill True
        spacing 20
        xmargin 20
        ymargin 150

        add gallery.make_button(name="red",unlocked="CGs/small/red_small.jpg",locked="CGs/small/locked.png") 
        add gallery.make_button(name="blue",unlocked="CGs/small/blue_small.png",locked="CGs/small/locked.png") 
        add gallery.make_button(name="green_and_orange",unlocked="CGs/small/green_small.png",locked="CGs/small/locked.png") 
        add gallery.make_button(name="green_and_orange2",unlocked="CGs/small/red_small.jpg",locked="CGs/small/locked.png") 

        add gallery.make_button(name="red",unlocked="CGs/small/red_small.jpg",locked="CGs/small/locked.png") 

    #Status bar
    add "UI/status_bar.png" xpos 0 ypos -0 xsize 1.0 ysize 126

    # Button to return
    imagebutton:
        xpos 15
        ypos 15
        auto "buttons/back_%s.png"
        action Hide("PhoneGallery"), Show("PhoneHomescreen")