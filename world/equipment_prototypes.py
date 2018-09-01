from random import randint
EQUIPMENT = {
"GRENADES": {
    "key": "Grenades x3",
    "desc": "Blows up in a pretty wide radius fove seconds after you press the arming button.  You could probably "
            "modify it to explode on a timer, or a trigger, but you should be very careful with that sort of thing.",
    "action_order": ("violence", 3),
    "size": "small",
    "cost": 50,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 2,
    "uses": 3
},
"MINIGUN": {
    "key": "The Minigun",
    "desc": "That's a midleading name; this thing is bloody huge.  Fires d6 times before it runs out of ammo; get the "
            "GM to roll.  You can't tell how many shots you've got left unless you take it apart.",
    "action_order": ("violence", 1),
    "size": "large",
    "cost": 400,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 3,
    "uses": lambda:randint(1, 6)
},
"SNIPER": {
    "key": "Sniper Rifle",
    "desc": "If you try to use it when you've not had time to prepare and calibrate the thing, those bonus dice "
            "become negative dice",
    "action_order": ("violence", 4),
    "size": "medium",
    "cost": 300,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 2
},
"MULTI_ADAPTER": {
    "key": "Multi-Adapter",
    "desc": "If there's a lot of things that need to be recharged and only one power outlet, you're the most popular "
            "Troubleshooter on the team.",
    "action_order": ("mechanics", 0),
    "size": "small",
    "cost": 25,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 1,
    "uses": -1
},
"GAUSS_ROCKET_LAUNCHER": {
    "key": "Gauss Rocket Launcher",
    "desc": "Either this weapon uses electromagnets to launch explosive projectiles up to 300 meters (3 charges) or "
            "it fires gauss rockets.  Information on gauss rockets is classified at your security level.",
    "action_order": ("violence", 0),
    "size": "large",
    "cost": 650,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 3,
    "uses": 3
},
"GRAPPLE_GUN": {
    "key": "Grapple Gun",
    "desc": "Uses compressed gas to shoot a grapnel attached to a steel cable; very useful for climbing, swinging or "
            "rapidly descending.  Could be used as a Level 1 weapon, with the additional benefit (or problem) that on "
            "a successful hit, you are now attached to your target.",
    "action_order": ("mechanics", 2),
    "size": "medium",
    "cost": 100,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 2,
    "uses": -1
},
"BODY_ARMOR": {
    "key": "Body Armor",
    "desc": "Increases the wearer's defense rating by 2.  Makes hydrolic noises.  Has a habit of coming off, breaking "
            "or running out of power at inopportune moments (or critical failures).",
    "action_order": ("athletics", -2),
    "size": "large",
    "cost": 750,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 2,
    "uses": -1
},
"MEDKIT": {
    "key": "Medkit x3",
    "desc": "Whack one on a wound and watch it insta-heal!  Isn't nanotechnology and morphine great?  Some medkits "
            "will even regrow a missing limb.  You weren't missing a limb?  Now you have a spare!  Make a Brains + "
            "Science check to use it properly.",
    "action_order": ("brains", 2),
    "size": "small",
    "cost": 50,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 1,
    "uses": 3
},
"ELECTRO_KNUCLES": {
    "key": "Electro-Knuckles",
    "desc": "Add a die when you punch someone or intimidate them and add another die if you want to electrocute them "
            "at the same time.  (4 charges)",
    "action_order": ("violence", 3),
    "size": "small",
    "cost": 250,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 1,
    "uses": 4
},
"SEDATIVES": {
    "key": "Sedatives x3",
    "desc": "Used to calm down unstable clones, whether they're innocent bystanders, dangerous terrorists or misguided "
            "members of the Troubleshooter team.  Make a Brains + Science check to inflict calm.",
    "action_order": ("brains", 1),
    "size": "small",
    "cost": 100,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 1,
    "uses": 3
},
"DATA_BOMB": {
    "key": "Data Bomb",
    "desc": "Renders the immediate area free of all electronic activity for 1-3 minutes and makes it easier to mess "
            "with machines and computers.  Usable only once.  If your mission briefing did not mention DAVs then you "
            "have been issued this item in error and not returning it immediately is treason.",
    "action_order": ("mechanics", 2),
    "size": "medium",
    "cost": 1250,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 3,
    "uses": 1
},
"TAXI_POD": {
    "key": "Taxi-Pod",
    "desc": "A small electric four-wheeled vehicle suitable for carrying up to four small Troubleshooters with no "
            "equipment or intimacy issues or one large Troubleshooter with a lot of equipment.  Range depends on load.",
    "action_order": ("mechanics", 2),
    "size": "oversize",
    "cost": 2000,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 2,
    "uses": -1
},
"MEGAPHONE": {
    "key": "Megaphone",
    "desc": "Make yourself heard in noisy situation and at long distances.",
    "action_order": ("chutzpah", 3),
    "size": "medium",
    "cost": 35,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 1,
    "uses": -1
},
"NEEDLER": {
    "key": "Needler",
    "desc": "Fires small hypodermic darts up to 15 meters.  Standard darts contain a strong knockout drug (takes "
            "effect in 1-2 rounds) but other darts are available.",
    "action_order": ("violence", 4),
    "size": "medium",
    "cost": 125,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 1,
    "uses": 5
},
"FRICTION_ENHANCER": {
    "key": "Friction Enhancer",
    "desc": "This experimental device increases or reduces friction by up to 500%.  Requires a Science roll to "
            "operate correctly.  Increasing friction causes solids to move less freely and machinery to seize up; "
            "reducing it makes everything slippery and difficult to hold, while machines run faster.  Only works while "
            "trigger is pressed.  Power pack weighs 65kgs and discharges in 20 seconds; can be recharged (8 hours) or "
            "replaced.  Range: a 30-degree beam, up to 15 meters.",
    "action_order": ("brains", 4),
    "size": "large",
    "cost": 1000,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 4,
    "uses": -1
},
"LASER_TRIPWIRE": {
    "key": "Laser Tripwire",
    "desc": "A brick-sized box that attaches to any flat surface.  When armed it projects an invisible laser beam up "
            "to 10 meters that detects and slices through anyone passing through it like cheesewire.  Has settings "
            "for security clearance and bots/no bots.  Box will explode if disturbed.  'On/Off' switch is on the side "
            "that fixes to the wall, to strop traitors disarming it.",
    "action_order": ("mechanics", 1),
    "size": "medium",
    "cost": 200,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 3,
    "uses": 1
},
"FOAM_GRENADE": {
    "key": "Foam Grenades x3",
    "desc": "This grenade creates 30 cubic meters of grey sticky foam that solidifies in 2 combat rounds, "
            "immobilizing anyone caught in it.  Make a Violence + Melee roll to get free before it sets; no chance "
            "after that.  Anyone completely covered will suffocate in 1-3 minutes.  Foam does not burn, cannot be "
            "lasered and R&D is developing a solution that will dissolve it without dissolving the clones trapped in it.",
    "action_order": ("violence", 2),
    "size": "small",
    "cost": 75,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 2,
    "uses": 3
},
"KAT_COMPANION_BOT": {
    "key": "K@ Companion Bot",
    "desc": "A feline surveillance bot, K@ can climb walls, explore confined spaces, or lie on watch, all while "
            "streaming live audio/video to the Troubleshooter's Cerebral Coretech.  Uses titanium teeth and claws to "
            "attack or sabotage.  Had night-vision and a 12-hour battery.  It its cats-whisker wifi antennae are "
            "damaged, make a Mechanics + Operate roll or the bot enters 'feral' mode and must be recaptured.  K@ bot "
            "sees other K@s as hostil and are distracted by lasers.",
    "action_order": ("mechanics", 5),
    "size": "medium",
    "cost": 500,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 3,
    "uses": -1
},
"HYGIENE_O_MATIC_9000": {
    "key": "Hygiene-o-matic 9000",
    "desc": "Clean corridors!  Clean you friends! Wash propaganda out of a traitor's mouth!  Comes with five "
            "solutions for all your hygiene needs.  To use, make a Mechanics + Science roll (Violence + Science in "
            "combat) to choose a setting.  On a fail the GM chooses but that setting is then empty.  Settings are: "
            "Combination Soap, Shampoo and Mouth Wash; Industrial Solvent and Paint Stripper; Pure Bleach; No-Mess "
            "Sanitation Gel (flammable)l and Quick-Dry Superglue for Fast Repairs",
    "action_order": ("mechanics", 2),
    "size": "large",
    "cost": 250,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 3,
    "uses": -1
},
"UBT_HYPERSENSE_DEVICE": {
    "key": "U.B.T. Hypersense Device",
    "desc": "The UBT Hypersense Device digitally enhances one of the Troubleshooter's sense by a factor of 12 bu "
            "repurposing the bandwidth of the other senses and reducing their input.  Make a Brains + Operate roll to "
            "use successfully.  Synaesthesia and disorientation can result, as well as a spackle of grey itching "
            "bitter with the eleven of hair.",
    "action_order": ("brains", 4),
    "size": "small",
    "cost": 450,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 2,
    "uses": -1
},
"CASEY_BS_BOMBABOOTS": {
    "key": "Casey-B's Bombaboots",
    "desc": "The ultimate in personal maneuverability!  Operated via a Cerebral Coretech pligin, the Bombaboots "
            "launch the wearer up to 7 meters vertically or 10 meters horizontally with pulsed blasts of superheated "
            "mercury vapor.  Roll Violence + Demolitions to use; failure only rarely results in knees being blown "
            "off.  Boots hold four charges, which leave unhygienic scortch marks or divots.  Do not stand within two "
            "meters or user.",
    "action_order": ("violence", 5),
    "size": "medium",
    "cost": 300,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 3,
    "uses": -1
},
"FAKE_MUSTACHE": {
    "key": "Fake Moustache",
    "desc": "Working undercover? Worried that terrorists know your face?  Worry no more!  Fake Moustache lets you "
            "reclaim your anonymity.  No one's looking for a clone with a moustache!  Place it under your nose, let "
            "the pneumatic pinchers expand within your nostrils and feel like a new clone.  Fake Moustache identifies "
            "the wearer as John-R-DOE-1 (default Setting) to Cerebral COretech users and bots.  Only the Computer "
            "knows your secret.",
    "action_order": ("chutzpah", 4),
    "size": "small",
    "cost": 150,
    "typeclass": "typeclasses.equipment.Equipment",
    "level": 1,
    "uses": -1
},
    "LASER_PISTOL": {
        "key": "Laser pistol",
        "desc": "Standard equipment for a Troubleshooter.  I mean, it's the 'shoot' part, right?  RIGHT?  Anyway, "
                "point the noisy end away from you.",
        "action_order": ("violence", 1),
        "size": "medium",
        "cost": 0,
        "typeclass": "typeclasses.equipment.Equipment",
        "level": 1,
        "uses": 20
    }
}
