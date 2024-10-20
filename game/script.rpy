init python:
    player = ""
    currentCharacter = "Mom"
    mom_enabled = True
    luci_enabled = False
    elysia_enabled = False

    histories = {
        "Luci": [],
        "Elysia": [],
        "Mom": [],
    }
    chapters = {
        "Luci": 1,
        "Elysia": 1,
        "Mom": 1
    }

    luci_statuses = [
        "This user is unreachable",
        "Anyone wanna hangout later? ♡",
        "Wish I was outside rn",
    ]

    elysia_statuses = [
        "This user is unreachable",
        "zzzz"
    ]

    mom_statuses = [
        "Do the universe a favour, don't hide your magic!"
    ]

    luci_status = luci_statuses[0]
    elysia_status = elysia_statuses[0]
    mom_status = mom_statuses[0]

define config.developer = True

# NVL characters are used for the phone texting
define mc = Character("MC")
define sys = Character("System", kind=nvl)
define mc_nvl = Character("MC", kind=nvl, callback=Phone_SendSound)
define w_nvl = Character("Elysia", kind=nvl, callback=Phone_ReceiveSound)
define l_nvl = Character("Luci", kind=nvl, callback=Phone_ReceiveSound)
define mom_nvl = Character("Mom", kind=nvl, callback=Phone_ReceiveSound)
define stop_text = Character(kind=nvl, advance=False)

define config.adv_nvl_transition = None
define config.nvl_adv_transition = Dissolve(0.3)

label history_save(character):
    $ histories[character] = list(nvl_list)
    return

label character_history_load(character):
    nvl clear
    $ nvl_list = list(histories[character])

    if (character != currentCharacter):
        $ currentCharacter = character
        $ nvl_list = histories[character]
        $ label_to_jump = character + "_" + str(chapters[character])
        jump expression label_to_jump
    return

# The game starts here.
label main_menu:
    return

label start:
    window hide
    call showPhone

# Introductory conversation with Mom
label Mom_1:
    $ renpy.pause(0.000001, hard=False)
    nvl clear

    mom_nvl "Hi, sweetheart!{image=emoji/heart.png}"
    mc_nvl "Hey Mom!"
    $ renpy.notify("Hello! This is a test message to test notifications.")
    mom_nvl "Looks like your brother's phone still turns on."
    mom_nvl "Did you get everything set up properly?"
    mc_nvl "Yeah, I did. All set."
    mom_nvl "Did you remember to add your contact details?"
    mom_nvl "It's important to have them on the lockscreen, in case you lose it."

    call history_save("Mom")
    $ chapters["Mom"] = 2

    $ quick_menu = False
    show screen enterName
    $ ui.interact()

label Mom_2:
    $ renpy.pause(0.000001, hard=False)

    mc_nvl "Yep, All done."
    mom_nvl "Ok, good."
    mom_nvl "I'm so used to helping your brother with these things, I forget you're all grown up."
    mom_nvl "I trust you can handle setting up your own devices, honey {image=emoji/heart.png}"
    mom_nvl "Just hang onto this phone until he gets back from basic training, okay?"
    mom_nvl "Your dad and I can get you a newer model later."
    mc_nvl "Mom, I appreciate it, but I can buy my own stuff. {image=emoji/sweat.png}"
    mom_nvl "I know you can, but I don't want work to get in the way of your studies."
    mom_nvl "Let us take care of it. {image=emoji/thumbs up.png}"
    mom_nvl "And please, try not to break any more phones, okay?"

    mom_nvl "Oh, and is spaghetti okay for dinner? If not, we've got meatloaf too!"

    nvl_narrator "Oh god, anything but the meatloaf again."

    menu (nvl=True):
        "Spaghetti sounds great!":
            mc_nvl "Sounds good to me."
            mom_nvl "Good, because I already bought the mince {image=emoji/heart.png}"
            pass
        "Maybe we just get takeout?":
            mc_nvl "Actually, I have a coupon for a pizza deal..."
            mom_nvl "Oh sweetie, we've had takeout all week. Spaghetti it is."
            pass
    mom_nvl "Oops, your dad's calling me. We'll chat later. Love you! xxxxxx {image=emoji/heart.png}"

    $ luci_enabled = True
    #$ elysia_enabled = True
    $ luci_status = luci_statuses[1]
    #$ elysia_status = elysia_statuses[1]

    call history_save("Mom")
    nvl_narrator "Mom is offline"
    $ mom_enabled = False
    stop_text ""

label Luci_1:
    $ renpy.pause(0.000001, hard=False)
    nvl clear

    l_nvl "This conversation is locked for now..."
    nvl_narrator "Luci is offline"

    call history_save("Luci")
    $ luci_enabled = False
    stop_text ""

label Elysia_1:
    $ renpy.pause(0.000001, hard=False)
    nvl clear

    w_nvl "This conversation is locked for now..."
    nvl_narrator "Elysia is offline"

    call history_save("Elysia")


label Elysia_2:
    $ renpy.pause(0.000001, hard=False)

    w_nvl "Sorry, still offline."
    mc_nvl "Oh, okay..."


    call history_save("Elysia")
    $ elysia_enabled = False
    stop_text ""
    
