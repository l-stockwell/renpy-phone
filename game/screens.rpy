################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"

    ## Place a character image on the bottom left of the screen
    add SideImage() xalign 0.0 yalign 1.0

    ## Select quick menu style to use.
    ## Show the quick menu only when the say screen is shown
    use quick_menu


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=0.3)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos


## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xalign gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


## When this is true, menu captions will be spoken by the narrator. When false,
## menu captions will be displayed as empty buttons.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

## We need a new variable to control the quick menu when in NVL mode
default in_nvl = False

screen quick_menu():

    ## Ensure the quick menu appears above other screens
    zorder 100

    ## Only show if the quick menu is allowed
    if quick_menu:

        ## The button used to determine textbox or top of screen alignment.
        if config.developer and persistent.quick_menu_style and not in_nvl:
            vbox:
                xalign 1.0
                yalign 0.26
                imagebutton:
                    alt "Toggle quick menu position"
                    hover "gui/button/switch_rotated.png"
                    idle "gui/button/switch_rotated.png"
                    action ToggleVariable("persistent.quick_menu_align", True, False)
                    tooltip _("Quick menu")

        ## Determine quick menu style to use
        if persistent.quick_menu_style and persistent.quick_menu_align:

            ## Create a container for the quick menu content
            frame:

                xfill True
                ## Align the quick menu to the top of the screen
                ypos 0
                has hbox
                style_prefix "touch_quick"

                xalign 0.5
                yalign 0.8
                spacing 35

                textbutton _("Back") action Rollback()
                textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
                textbutton _("Auto") action Preference("auto-forward", "toggle")
                textbutton _("Q.Save") action QuickSave()
                textbutton _("Menu") action ShowMenu('navigation')

        elif persistent.quick_menu_style and not persistent.quick_menu_align:

            ## Create a container for the quick menu content
            frame:

                xfill True
                ## Number not yet accurate
                ypos 1466
                has hbox
                style_prefix "touch_quick"

                xalign 0.5
                yalign 0.8
                spacing 35

                textbutton _("Back") action Rollback()
                textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
                textbutton _("Auto") action Preference("auto-forward", "toggle")
                textbutton _("Q.Save") action QuickSave()
                textbutton _("Menu") action ShowMenu('navigation')

        elif not persistent.quick_menu_style:
            use quick_menu_ham





screen quick_menu_2():

    zorder 100

    frame:
        style_prefix "quick_menu"
        xalign 0.5
        yalign 0

        grid 4 2:
            xalign 0.5
            yalign 0.5
            spacing 5

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu ("navigation")
            textbutton _("History") action ShowMenu("history")
            textbutton _("Q.save") action QuickSave()
            textbutton _("Q.load") action QuickLoad()
            textbutton _("Settings") action ShowMenu("preferences")
    use quick_menu_ham

style quick_menu_frame:
    xfill True
    ysize 150

    background Frame("gui/overlay/menu_top.png", gui.frame_borders, tile=gui.frame_tile)
    padding gui.frame_borders.padding
                      
default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")


style touch_quick_button is default
style touch_quick_button_text is button_text

style touch_quick_button:
    properties gui.button_properties("touch_quick_button")

style touch_quick_button_text:
    properties gui.button_text_properties("touch_quick_button")


screen quick_menu_ham():

    ## Ensure the quick menu button stays on top of the quick menu so it can be closed
    zorder 101

    vbox:
        xalign 1.0
        yalign 0.0
        imagebutton:
            alt "Open the quick menu"
            hover "gui/button/hamburger.png"
            idle "gui/button/hamburger.png"
            action ToggleScreen('quick_menu_2')
            tooltip _("Quick menu")


################################################################################
## Main and Game Menu Screens
################################################################################


## Navigation screen ############################################################
##
## Used as the pause/game menu


screen navigation():

    tag menu

    if persistent.navigation_menu_content_style:

        frame:
            style_prefix "main_menu"

            at menu_appear_side


            grid 1 8:
                xalign 0.5
                yalign 0.5

                textbutton _("History") action ShowMenu("history")
                textbutton _("Save") action ShowMenu("save")
                textbutton _("Load") action ShowMenu("load")
                textbutton _("Settings") action ShowMenu("preferences")
                textbutton _("Help") action ShowMenu("help")
                ## We use renpy.full_restart to avoid any potential issues with gestures.
                textbutton _("Main Menu") action renpy.full_restart
                if not renpy.variant("mobile"):
                    textbutton _("Quit") action Quit(confirm = True)
                else:
                    null
                null

            if persistent.navigation_return_button_style:
                textbutton _("Close") action Hide("navigation"), Return():
                    xalign 0.5
                    yalign 1.0

            else:
                fixed:
                    xmaximum 60
                    xalign 0.99
                    yalign 0.1
                    textbutton "≡" action Hide("navigation"), Return()


    else:

        frame:
            ypos 980
            style_prefix "navigation_menu"

            at menu_appear_bottom

            grid 2 4:
                xalign 0.5
                yalign 0.5
                spacing 5

                textbutton _("History") action ShowMenu("history")
                ## We use renpy.full_restart to avoid any potential issues with gestures.
                textbutton _("Main Menu") action renpy.full_restart
                textbutton _("Save") action ShowMenu("save")
                textbutton _("Load") action ShowMenu("load")
                textbutton _("Settings") action ShowMenu("preferences")
                textbutton _("Help") action ShowMenu("help")
                null
                if not renpy.variant("mobile"):
                    textbutton _("Quit") action Quit(confirm = True)
                else:
                    null


            if persistent.navigation_return_button_style:
                textbutton _("Close") action Hide("navigation"), Return():
                    xalign 0.99
                    yalign 1.0

            else:
                fixed:
                    xmaximum 60
                    xalign 0.99
                    yalign 0.1
                    textbutton "≡" action Hide("navigation"), Return()



    if config.developer:

        vbox:
            imagebutton:
                alt "Switch close button style"
                hover "gui/button/switch.png"
                idle "gui/button/switch.png"
                action ToggleVariable("persistent.navigation_return_button_style")
                tooltip _("Switch between available close button styles")
            imagebutton:
                alt "Switch menu style"
                hover "gui/button/switch.png"
                idle "gui/button/switch.png"
                action ToggleVariable("persistent.navigation_menu_content_style")
                tooltip _("Switch between available menu styles")


style navigation_menu_frame:
    xfill True
    ysize 300

    background Frame("gui/overlay/menu_bottom.png", gui.frame_borders, tile=gui.frame_tile)
    padding gui.frame_borders.padding
style navigation_menu_vbox is main_menu_vbox
style navigation_menu_text is main_menu_text


transform menu_appear_bottom:
    on show, replace:
        ypos 1920
        linear 0.36 ypos 1617
    on hide, replaced:
        linear 0.36 ypos 1920

transform menu_appear_side:
    on show, replace:
        xpos -432
        linear 0.36 xpos 0
    on hide, replaced:
        linear 0.36 xpos -432





## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    style_prefix "main_menu"

    add gui.main_menu_background

    use mm_content

    if config.developer:
        imagebutton:
            alt "Switch menu style"
            hover "gui/button/switch.png"
            idle "gui/button/switch.png"
            action ToggleVariable("persistent.men_style")
            tooltip _("Switch between available menu styles")

screen conf_button():

    if config.developer:
        vbox:
            xalign 0.98
            ypos 0.165

            imagebutton:
                alt "change configuration settings"
                auto "gui/button/settings_%s.png"
                hover_foreground Text(_("Configure GUI"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Configure GUI"), xalign=0.5, yalign=0.5)
                selected_idle "gui/button/settings_selected_idle.png"
                selected_hover "gui/button/settings_selected_hover.png"
                action ShowMenu("configs")
                tooltip _("Change Configuration settings")

screen mm_content():

    use conf_button

    if persistent.men_style:
        grid 3 2:

            xalign 0.5
            yalign 0.965
            spacing 20

            imagebutton:
                alt "new game"
                auto new_game_button_image
                hover_foreground Text(_("New Game"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("New Game"), xalign=0.5, yalign=0.5)
                selected_idle new_game_button_idle_image
                selected_hover new_game_button_hover_image
                action Start()
                tooltip _("Begin a new game")

            imagebutton:
                alt "load"
                auto load_button_image
                hover_foreground Text(_("Load"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Load"), xalign=0.5, yalign=0.5)
                selected_idle load_button_idle_image
                selected_hover load_button_hover_image
                action ShowMenu("load")
                tooltip _("Load a previously saved game")

            imagebutton:
                alt "Settings"
                auto settings_button_image
                hover_foreground Text(_("Settings"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Settings"), xalign=0.5, yalign=0.5)
                selected_idle settings_button_idle_image
                selected_hover settings_button_hover_image
                action ShowMenu("preferences")
                tooltip _("Adjust game settings")

            imagebutton:
                alt "extras"
                auto extras_button_image
                hover_foreground Text(_("Extras"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Extras"), xalign=0.5, yalign=0.5)
                selected_idle extras_button_idle_image
                selected_hover extras_button_hover_image
                action ShowMenu("extras")
                tooltip _("Extra content")

            imagebutton:
                alt "help"
                auto settings_button_image
                hover_foreground Text(_("Help"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Help"), xalign=0.5, yalign=0.5)
                selected_idle help_button_idle_image
                selected_hover help_button_hover_image
                action ShowMenu("help")
                tooltip _("How to play")

            if not renpy.variant("mobile"):

                imagebutton:
                    alt "quit"
                    auto quit_button_image
                    hover_foreground Text(_("Quit"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Quit"), xalign=0.5, yalign=0.5)
                    selected_idle quit_button_idle_image
                    selected_hover quit_button_hover_image
                    action Quit(confirm=not main_menu)
                    tooltip _("Close the game")
            else:
                null


        if gui.show_name:

            vbox:
                xalign 0.5
                ypos 0.5
                text "[config.name!t]":
                    style "main_menu_title"

                text "[config.version]":
                    style "main_menu_version"

## text alignment adjusted in line 289 or gui.rpy
# define gui.main_menu_text_xalign = 0.5


    elif not persistent.men_style:

        frame:
            grid 1 6:
                xalign 0.5
                yalign 0.5

                spacing 30

                imagebutton:
                    alt "new game"
                    auto new_game_button_image
                    hover_foreground Text(_("New Game"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("New Game"), xalign=0.5, yalign=0.5)
                    selected_idle new_game_button_idle_image
                    selected_hover new_game_button_hover_image
                    action Start()
                    tooltip _("Begin a new game")

                imagebutton:
                    alt "load"
                    auto load_button_image
                    hover_foreground Text(_("Load"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Load"), xalign=0.5, yalign=0.5)
                    selected_idle load_button_idle_image
                    selected_hover load_button_hover_image
                    action ShowMenu("load")
                    tooltip _("Load a previously saved game")

                imagebutton:
                    alt "Settings"
                    auto settings_button_image
                    hover_foreground Text(_("Settings"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Settings"), xalign=0.5, yalign=0.5)
                    selected_idle settings_button_idle_image
                    selected_hover settings_button_hover_image
                    action ShowMenu("preferences")
                    tooltip _("Adjust game settings")

                imagebutton:
                    alt "extras"
                    auto extras_button_image
                    hover_foreground Text(_("Extras"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Extras"), xalign=0.5, yalign=0.5)
                    selected_idle extras_button_idle_image
                    selected_hover extras_button_hover_image
                    action ShowMenu("extras")
                    tooltip _("Extra content")

                imagebutton:
                    alt "help"
                    auto help_button_image
                    hover_foreground Text(_("Help"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Help"), xalign=0.5, yalign=0.5)
                    selected_idle help_button_idle_image
                    selected_hover help_button_hover_image
                    action ShowMenu("help")
                    tooltip _("How to play")

                if not renpy.variant("mobile"):
                    imagebutton:
                        alt "quit"
                        auto quit_button_image
                        hover_foreground Text(_("Quit"), xalign=0.5, yalign=0.5)
                        idle_foreground Text(_("Quit"), xalign=0.5, yalign=0.5)
                        selected_idle quit_button_idle_image
                        selected_hover quit_button_hover_image
                        action Quit(confirm=not main_menu)
                        tooltip _("Close the game")
                else:
                    null

            if gui.show_name:

                vbox:
                    xalign 1.0
                    ypos 1.0
                    text "[config.name!t]":
                        style "main_menu_title"

                    text "[config.version]":
                        style "main_menu_version"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 416
    yfill True

    background Frame("gui/overlay/menu_side.png", gui.frame_borders, tile=gui.frame_tile)
    padding gui.frame_borders.padding

style main_menu_vbox:
    xalign 1.0
    xoffset -20
    xmaximum 800
    yalign 1.0
    yoffset -20

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


screen extras():

    $ tooltip = GetTooltip()

    tag menu

    use game_menu(_("Extras"), scroll="viewport"):

        vbox:
            ysize 120

            if tooltip:
                text "[tooltip]"
            else:

                vbox:
                    if renpy.mobile:
                        text _("Press and hold an option for a short description of its function")
                    else:
                        text _("Hover over an option for a short description of its function")

        ## Used as a content divider
        null height 10
        bar ysize 10 xsize 1000
        null height 10

        hbox:

            spacing 25
            ## Add 10 pixels padding
            null

            if persistent.gal_screen:
                imagebutton:
                    alt "image gallery"
                    auto gallery_button_image
                    hover_foreground Text(_("Image Gallery"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Image Gallery"), xalign=0.5, yalign=0.5)
                    selected_idle gallery_button_idle_image
                    selected_hover gallery_button_hover_image
                    action ShowMenu("gallery")
                    tooltip _("View unlocked images")
            else:
                imagebutton:
                    alt "image gallery"
                    auto gallery_button_image
                    hover_foreground Text(_("Image Gallery"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Image Gallery"), xalign=0.5, yalign=0.5)
                    selected_idle gallery_button_idle_image
                    selected_hover gallery_button_hover_image
                    action ShowMenu("underconstruction")
                    tooltip _("View unlocked images")

            imagebutton:
                alt "about"
                auto about_button_image
                hover_foreground Text(_("About"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("About"), xalign=0.5, yalign=0.5)
                selected_idle about_button_idle_image
                selected_hover about_button_hover_image
                action ShowMenu("about")
                tooltip _("About this game")

            imagebutton:
                alt "changelog"
                auto changelog_button_image
                hover_foreground Text(_("Changelog"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Changelog"), xalign=0.5, yalign=0.5)
                selected_idle changelog_button_idle_image
                selected_hover changelog_button_hover_image
                action ShowMenu("changelog")
                tooltip _("View the changelog")


        ## Used as a content divider
        null height 10
        bar ysize 10 xsize 1000
        null height 10




screen nav_content():

    grid 3 2:

        xalign 0.5
        yalign 0.965
        spacing 20

        if main_menu:
            imagebutton:
                alt "new game"
                auto new_game_button_image
                hover_foreground Text(_("New Game"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("New Game"), xalign=0.5, yalign=0.5)
                selected_idle new_game_button_idle_image
                selected_hover new_game_button_hover_image
                action Start()
                tooltip _("Begin a new game")

            imagebutton:
                alt "load"
                auto load_button_image
                hover_foreground Text(_("Load"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Load"), xalign=0.5, yalign=0.5)
                selected_idle load_button_idle_image
                selected_hover load_button_hover_image
                action ShowMenu("load")
                tooltip _("Load a previously saved game")

            imagebutton:
                alt "Settings"
                auto settings_button_image
                hover_foreground Text(_("Settings"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Settings"), xalign=0.5, yalign=0.5)
                selected_idle settings_button_idle_image
                selected_hover settings_button_hover_image
                action ShowMenu("preferences")
                tooltip _("Adjust game settings")

            imagebutton:
                alt "extras"
                auto extras_button_image
                hover_foreground Text(_("Extras"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Extras"), xalign=0.5, yalign=0.5)
                selected_idle extras_button_idle_image
                selected_hover extras_button_hover_image
                action ShowMenu("extras")
                tooltip _("Extra content")

            imagebutton:
                alt "help"
                auto help_button_image
                hover_foreground Text(_("Help"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Help"), xalign=0.5, yalign=0.5)
                selected_idle help_button_idle_image
                selected_hover help_button_hover_image
                action ShowMenu("help")
                tooltip _("How to play")

            imagebutton:
                alt "return"
                auto return_button_image
                hover_foreground Text(_("Return"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Return"), xalign=0.5, yalign=0.5)
                selected_idle return_button_idle_image
                selected_hover return_button_hover_image
                action Return()
                tooltip _("Return to the main menu")
        else:

            imagebutton:
                alt "history"
                auto new_game_button_image
                hover_foreground Text(_("History"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("History"), xalign=0.5, yalign=0.5)
                selected_idle history_button_idle_image
                selected_hover history_button_hover_image
                action ShowMenu("history")
                tooltip _("Show the text history")

            imagebutton:
                alt "save"
                auto save_button_image
                hover_foreground Text(_("Save"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Save"), xalign=0.5, yalign=0.5)
                selected_idle save_button_idle_image
                selected_hover save_button_hover_image
                action ShowMenu("save")
                tooltip _("Save your game")

            imagebutton:
                alt "load"
                auto load_button_image
                hover_foreground Text(_("Load"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Load"), xalign=0.5, yalign=0.5)
                selected_idle load_button_idle_image
                selected_hover load_button_hover_image
                action ShowMenu("load")
                tooltip _("Load a previously saved game")

            imagebutton:
                alt "Settings"
                auto settings_button_image
                hover_foreground Text(_("Settings"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Settings"), xalign=0.5, yalign=0.5)
                selected_idle settings_button_idle_image
                selected_hover settings_button_hover_image
                action ShowMenu("preferences")
                tooltip _("Adjust game settings")

            imagebutton:
                alt "help"
                auto help_button_image
                hover_foreground Text(_("Help"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Help"), xalign=0.5, yalign=0.5)
                selected_idle help_button_idle_image
                selected_hover help_button_hover_image
                action ShowMenu("help")
                tooltip _("How to play")

            imagebutton:
                alt "return"
                auto return_button_image
                hover_foreground Text(_("Return"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Return"), xalign=0.5, yalign=0.5)
                selected_idle return_button_idle_image
                selected_hover return_button_hover_image
                action Return()
                tooltip _("Return to the main menu")

## text alignment adjusted in line 289 or gui.rpy
# define gui.main_menu_text_xalign = 0.5





## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid". When
## this screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0):

    style_prefix "game_menu"

    add "gui/game_menu.png"

    frame:
        style "game_menu_outer_frame"

        hbox:

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        transclude

                else:

                    transclude
    use nav_content

    hbox:
        label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
#    bottom_padding 130
    bottom_padding 436
    top_padding 120

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 416
    yfill True

style game_menu_content_frame:
    left_margin 40
    right_margin 40
    top_margin 10

style game_menu_viewport:
    xsize 1080

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 10

style game_menu_label:
    xpos 50
    ysize 120

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]\n\n")

            text _("Edgy-tan used with permission. Copyright {a=http://studiomugenjohncel.wordpress.com/}mugenjohncel{/a}\n")

            text _("The Raven by {a=https://en.wikipedia.org/wiki/Edgar_Allan_Poe}Edgar Allen Poe{/a} is in the Public Domain.")

            text _("'Danse Macabre - Big Hit 1' Kevin MacLeod {a=incompetech.com}incompetech.com{/a}")

            text _("Licensed under Creative Commons: By Attribution 4.0 License {a=http://creativecommons.org/licenses/by/4.0/}http://creativecommons.org/licenses/by/4.0/{/a}")

            text _("'Danse Macabre - Big Change' Kevin MacLeod {a=incompetech.com}incompetech.com{/a}")

            text _("Licensed under Creative Commons: By Attribution 4.0 License {a=http://creativecommons.org/licenses/by/4.0/}http://creativecommons.org/licenses/by/4.0/{/a}")



## This is used to add text to the about screen.
define gui.about = ""


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size



## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu
    use file_slots(_("Save"))


screen load():

    tag menu
    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.1

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        ## Distance the text from the thumbnail
                        null height 10

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")

                ## range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 50
    ypadding 3

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

## This is necessary for the vibration toggle to function
default persistent.allow_vibration = True

## Variable to control which screen we show for settings the menu
default settings_menu_selector = "audio_settings"

screen preferences():

    $ tooltip = GetTooltip()

    tag menu


    use game_menu(_("Settings"), scroll="viewport"):


        vbox:
            ysize 120

            if tooltip:
                text "[tooltip]"
            else:

                vbox:
                    if renpy.mobile:
                        text _("Press and hold an option for a short description of its function")
                    else:
                        text _("Hover over an option for a short description of its function")

        ## Used as a content divider
        null height 10
        bar ysize 10 xsize 1000
        null height 10

        hbox:

            spacing 25
            ## Add 10 pixels padding
            null

            imagebutton:
                alt "adjust audio settings"
                auto audio_settings_button_image
                hover_foreground Text(_("Audio settings"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Audio settings"), xalign=0.5, yalign=0.5)
                action SetVariable("settings_menu_selector", "audio_settings")
                tooltip _("Adjust audio settings")

            imagebutton:
                alt "adjust text settings"
                auto text_settings_button_image
                hover_foreground Text(_("Text\nsettings"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Text\nsettings"), xalign=0.5, yalign=0.5)
                action SetVariable("settings_menu_selector", "text_settings")
                tooltip _("Adjust text settings")

            imagebutton:
                alt "adjust system settings"
                auto system_settings_button_image
                hover_foreground Text(_("System settings"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("System settings"), xalign=0.5, yalign=0.5)
                action SetVariable("settings_menu_selector", "system_settings")
                tooltip _("Adjust system settings")


        ## Used as a content divider
        null height 10
        bar ysize 10 xsize 1000
        null height 10


        if settings_menu_selector == "system_settings":
            use system_settings
        elif settings_menu_selector == "audio_settings":
            use audio_settings
        elif settings_menu_selector == "text_settings":
            use text_settings



screen system_settings():

    vbox:
        xalign 0.5

        if renpy.variant("pc"):
            vbox:
                style_prefix "radio"
                label _("Display")
                hbox:

                    imagebutton:
                        alt "window"
                        auto display_toggle_button_image
                        hover_foreground Text(_("{u}Window{/u}"), xalign=0.5, yalign=0.5)
                        idle_foreground Text(_("Window"), xalign=0.5, yalign=0.5)
                        selected_idle display_toggle_button_idle_image
                        selected_hover display_toggle_button_hover_image
                        action Preference("display", "any window")
                        tooltip _("Display the game in a window")

                    imagebutton:
                        alt "fullscreen"
                        auto display_toggle_button_image
                        hover_foreground Text(_("{u}Fullscreen{/u}"), xalign=0.5, yalign=0.5)
                        idle_foreground Text(_("Fullscreen"), xalign=0.5, yalign=0.5)
                        selected_idle display_toggle_button_idle_image
                        selected_hover display_toggle_button_hover_image
                        action Preference("display", "fullscreen")
                        tooltip _("Display the game in fullscreen")

        if renpy.variant("mobile"):
            vbox:
                style_prefix "radio"
                label _("Vibration")

                hbox:

                    imagebutton:
                        alt "on"
                        auto vibration_button_image
                        hover_foreground Text(_("{u}ON{/u}"), xalign=0.5, yalign=0.5)
                        idle_foreground Text(_("ON"), xalign=0.5, yalign=0.5)
                        selected_idle vibration_button_idle_image
                        selected_hover vibration_button_hover_image
                        action SetField(persistent, "allow_vibration", True)
                        tooltip _("Enable vibration")

                    imagebutton:
                        alt "off"
                        auto vibration_button_image
                        hover_foreground Text(_("{u}OFF{/u}"), xalign=0.5, yalign=0.5)
                        idle_foreground Text(_("OFF"), xalign=0.5, yalign=0.5)
                        selected_idle vibration_button_idle_image
                        selected_hover vibration_button_hover_image
                        action SetField(persistent, "allow_vibration", False)
                        tooltip _("disable vibration")

        vbox:
            style_prefix "radio"
            label _("Rollback Side")
            hbox:
                if renpy.variant("pc"):
                    imagebutton:
                        alt "disabled"
                        auto rollback_side_disabled_button_image
                        hover_foreground Text(_("{u}Disabled{/u}"), xalign=0.5, yalign=0.5)
                        idle_foreground Text(_("Disabled"), xalign=0.5, yalign=0.5)
                        selected_idle rollback_side_disabled_button_idle_image
                        selected_hover rollback_side_disabled_button_hover_image
                        action Preference("rollback side", "disable")
                        tooltip _("Rollback is only accessible through the scroll wheel and back button")
                else:
                    imagebutton:
                        alt "disabled"
                        auto rollback_side_disabled_button_image
                        hover_foreground Text(_("{u}Disabled{/u}"), xalign=0.5, yalign=0.5)
                        idle_foreground Text(_("Disabled"), xalign=0.5, yalign=0.5)
                        selected_idle rollback_side_disabled_button_idle_image
                        selected_hover rollback_side_disabled_button_hover_image
                        action Preference("rollback side", "disable")
                        tooltip _("Rollback is only accessible via the back button and gestures")

                imagebutton:
                    alt "left"
                    auto rollback_side_left_button_image
                    hover_foreground Text(_("{u}Left{/u}"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Left"), xalign=0.5, yalign=0.5)
                    selected_idle rollback_side_left_button_idle_image
                    selected_hover rollback_side_left_button_hover_image
                    action Preference("rollback side", "left")
                    tooltip _("Touch the left side of the screen to rollback")

                imagebutton:
                    alt "right"
                    auto rollback_side_right_button_image
                    hover_foreground Text(_("{u}Right{/u}"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Right"), xalign=0.5, yalign=0.5)
                    selected_idle rollback_side_right_button_idle_image
                    selected_hover rollback_side_right_button_hover_image
                    action Preference("rollback side", "right")
                    tooltip _("Touch the right side of the screen to rollback")

        vbox:
            style_prefix "check"
            label _("Skip")
            hbox:
                imagebutton:
                    alt "skip all text"
                    auto skip_all_button_image
                    hover_foreground Text(_("{u}All text{/u}"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("All text"), xalign=0.5, yalign=0.5)
                    selected_idle skip_all_button_idle_image
                    selected_hover skip_all_button_hover_image
                    action Preference("skip", "all")
                    tooltip _("Skip all text")

                imagebutton:
                    alt "skip only previously read text"
                    auto skip_read_button_image
                    hover_foreground Text(_("{u}Seen text{/u}"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Seen text"), xalign=0.5, yalign=0.5)
                    selected_idle skip_read_button_idle_image
                    selected_hover skip_read_button_hover_image
                    action Preference("skip", "seen")
                    tooltip _("Skip only previously read text")


            label _("After Choices")

            hbox:
                imagebutton:
                    alt "continue skipping after making choices"
                    auto after_choices_continue_button_image
                    hover_foreground Text(_("{u}Keep skipping{/u}"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Keep skipping"), xalign=0.5, yalign=0.5)
                    selected_idle after_choices_continue_button_idle_image
                    selected_hover after_choices_continue_button_hover_image
                    action Preference("after choices", "skip")
                    tooltip _("Continue skipping after making choices")

                imagebutton:
                    alt "stop skipping after making choices"
                    auto after_choices_stop_button_image
                    hover_foreground Text(_("{u}Stop skipping{/u}"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Stop skipping"), xalign=0.5, yalign=0.5)
                    selected_idle after_choices_stop_button_idle_image
                    selected_hover after_choices_stop_button_hover_image
                    action Preference("after choices", "stop")
                    tooltip _("Stop skipping after making choices")

                imagebutton:
                    alt "skip through scene transitions"
                    auto skip_transitions_button_image
                    hover_foreground Text(_("{u}Transitions{/u}"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Transitions"), xalign=0.5, yalign=0.5)
                    selected_idle skip_transitions_button_idle_image
                    selected_hover skip_transitions_button_hover_image
                    action InvertSelected(Preference("transitions", "toggle"))
                    tooltip _("Skip through scene transitions")


screen audio_settings():
    python:
        music_vol = _preferences.get_volume("music")
        sound_vol = _preferences.get_volume("sfx")
        voice_vol = _preferences.get_volume("voice")

    hbox:
        style_prefix "slider"
        box_wrap True

        vbox:

            if config.has_music:
                label _("Music Volume")

                vbox:
                    bar value Preference("music volume") tooltip _("Change the music volume")
                    text _( "{:.0f}%".format(music_vol * 100) )

            if config.has_sound:

                label _("Sound Volume")

                vbox:
                    bar value Preference("sound volume") tooltip _("Change the SFX volume")
                    text _( "{:.0f}%".format(sound_vol * 100) )

            if config.has_voice:
                label _("Voice Volume")

                vbox:
                    bar value Preference("voice volume") tooltip _("Change the volume of speech in the game")
                    text _( "{:.0f}%".format(voice_vol * 100) )

            if config.has_music or config.has_sound or config.has_voice:
                null height gui.pref_spacing

                vbox:

                    if config.sample_sound:
                        textbutton _("{size=30}Test Sound volume{/size}") action Play("sound", config.sample_sound) tooltip _("Test SFX volume")

                    if config.sample_voice:
                        textbutton _("{size=30}Test Voice Volume{/size}") action Play("voice", config.sample_voice) tooltip _("Test Voice volume")

                    textbutton _("Reset to default"):
                        action Preference("voice volume", config.default_music_volume), Preference("sound volume", config.default_music_volume), Preference("music volume", config.default_music_volume)
                        tooltip _("Reset audio settings to default")

                    textbutton _("Mute All"):
                        action Preference("all mute", "toggle")
                        style "mute_all_button"
                        tooltip _("Stop all audio")

screen text_settings():

    python:
        txtspd = _preferences.text_cps
        afmtm = _preferences.afm_time

    hbox:
        style_prefix "slider"
        box_wrap True

        vbox:

            label _("Text Speed")

            bar value Preference("text speed") tooltip _("Adjust the speed text appears on screen in characters per second")
            if txtspd > 0:
                text _("{:.0f}".format(txtspd) )
            elif txtspd == 0:
                text _("Instant")

            label _("Auto-Forward Time")

            bar value Preference("auto-forward time") tooltip _("Adjust wait time before automatically advancing the game")
            text _("{:.0f}".format(afmtm) )

            textbutton _("Reset to default"):
                action Preference("text speed", 60), Preference("auto-forward time", 15)
                tooltip _("Reset text settings to default")

style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 2

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 225

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")

style slider_slider:
    xsize 1000

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 10

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 450


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what

        if not _history_list:
            label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = set()


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign
    size gui.history_text_size + 5

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")
    size gui.history_text_size

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu

    if not renpy.variant("touch"):
        default device = "keyboard"
    elif renpy.variant("touch"):
        default device = "touch"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 15

            hbox:

                if renpy.variant("touch"):
                    textbutton _("Touch") action SetScreenVariable("device", "touch")
                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "touch":
                use touch_help
            elif device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help

screen touch_help():

    hbox:
        label _("Tap Screen")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Tap & Hold")
        text _("Alternate click. Primarily used with the skip button.")

    hbox:
        label _("Swipe Right")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Swipe Left")
        text _("Rolls forward to later dialogue.")

    hbox:
        label _("Vol Down + Power button")
        text _("Hold to take a screenshot.")


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    if renpy.variant("pc"):
        hbox:
            label "S"
            text _("Takes a screenshot.")

    if renpy.variant("pc"):
        hbox:
            label "V"
            text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up\nClick Rollback Side")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")


    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text

style help_text:
    size gui.text_size

style help_button:
    properties gui.button_properties("help_button")
    xmargin 8

style help_button_text:
    properties gui.button_text_properties("help_button")

style help_label:
    xsize 250
    right_padding 20

style help_label_text:
    size gui.text_size
    xalign 1.0
    text_align 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100

    if not renpy.get_screen("nvl"):
        style_prefix "skip"
    else:
        style_prefix "nvl_skip"

    frame:

        hbox:
            spacing 6

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"

style nvl_skip_frame is empty
style nvl_skip_text is gui_text
style nvl_skip_triangle is skip_text

style nvl_skip_frame:
    ypos gui.nvl_skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style nvl_skip_text:
    size gui.notify_text_size

## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):
    zorder 100

    if not renpy.get_screen("nvl"):
        style_prefix "notify"
    else:
        style_prefix "nvl_notify"

    frame at notify_appear:
        xpadding 130
        xalign 0.5
        ypos 105
        text "[message!tq]":
            size 40
            color "#000"


    timer 3.25 action Hide('notify')



transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")

style nvl_notify_frame is empty
style nvl_notify_text is gui_text

style nvl_notify_frame:
    ypos gui.nvl_notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style nvl_notify_text:
    properties gui.text_properties("notify")

init -2:
    screen _gamepad_select(joysticks):


        use game_menu(_("Settings"), scroll="viewport"):

            vbox:
                xfill True

                label _("Select Gamepad to Calibrate")

                if not joysticks:
                    text _("No Gamepads Available")
                else:
                    for i, name in joysticks:
                        textbutton "[i]: [name]" action Return(i) size_group "joysticks"

                null height 20

                textbutton _("Cancel") action Return("cancel")

    screen _gamepad_control(name, control, kind, mappings, back, i, total):


        use game_menu(_("Settings"), scroll="viewport"):

            vbox:
                xfill True

                label _("Calibrating [name] ([i]/[total])")

                null height 20

                text _("Press or move the [control] [kind].")
                #text _("Press or move the [control!r] [kind].")


                null height 20

                hbox:
                    textbutton _("Cancel") action Return("cancel")
                    if len(mappings) >= 2:
                        textbutton _("Skip (A)") action Return("skip")

                    if back and len(mappings) >= 3:
                        textbutton _("Back (B)") action Return(back)

            add _gamepad.EventWatcher(mappings)

screen underconstruction():

    $ tooltip = GetTooltip()

    tag menu
    use game_menu(_("Unavailable"), scroll="viewport"):

        vbox:
            null height 45
            style_prefix "about"
            xsize 660


            text _("This Feature is currently unavailable"):
                xalign 0.5


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    if nvl_mode == "phone":
        use messages(dialogue, items)
    else:
        window:
            style "nvl_window"

            has vbox:
                spacing gui.nvl_spacing

            ## Displays dialogue in either a vpgrid or the vbox.
            if gui.nvl_height:

                vpgrid:
                    cols 1
                    yinitial 1.0

                    use nvl_dialogue(dialogue)

            else:

                ypos 45

                use nvl_dialogue(dialogue)

            ## Displays the menu, if given. The menu may be displayed incorrectly if
            ## config.narrator_menu is set to True, as it is above.
            for i in items:

                textbutton i.caption:
                    action i.action
                    style "nvl_button"

#    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 450

style game_menu_navigation_frame:
    variant "small"
    xsize 340

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 400

style slider_pref_vbox:
    variant "small"
    xsize None

style slider_pref_slider:
    variant "small"
    xsize 600
