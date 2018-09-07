# coding=utf-8
HEALTH = {0: "Unharmed", 1: "Hurt", 2: "Injured", 3: "Maimed", 4: "Dead"}

EYES = {1: "blue", 2: "black", 3: "green", 4: "hazel", 5: "brown", 6: "yellow", 7: "white", 8: "red", 9: "purple"}

HAIR = {1: "bald", 2: "short brown", 3: "long brown", 4: "short blonde", 5: "long blonde", 6: "short auburn",
        7: "long auburn", 8: "short red", 9: "long red", 10: "short black", 11: "long black"}

SKIN = {1: "alabaster", 2: "peach", 3: "bronze", 4: "copper", 5: "coffee", 6: "mahogany", 7: "ebony"}

PERSONALITY = {"loyal": "disloyal", "brave": "cowardly", "honest" : "dishonest", "considerate": "selfish",
               "generous": "greedy", "loving": "hateful", "humble": "arrogant", "cautious": "rash", "kind": "mean",
               "calm": "nervous", "relaxed": "quick to anger"}

CLEARANCE = {1: "Infrared", 2: "Red", 3: "Orange", 4: "Yellow", 5: "Green", 6: "Blue", 7: "Indigo", 8: "Violet",
             9: "Ultraviolet"}

CLEARANCE_UPGRADES = {"Red": 500, "Orange": 1000, "Yellow": 2000, "Green": 4000, "Blue": 8000,
                      "Indigo": 16000, "Violet": 32000, "Ultraviolet": 64000}

MUTANT_POWERS = {"telepathy": {"action_order": 7, "description": "Spend 1 Moxie to read one dominant thought or "
                                                                 "implant a simple suggestion in another clone's "
                                                                 "mind.  It's difficult to read deeper memories, "
                                                                 "concoct elaborate lies or persuade them to do "
                                                                 "something they wouldn't normally but you can do it "
                                                                 "in a pinch."},
                 "anomoly": {"action_order": 5, "description": "Spend 1 Moxie to make things happen.  You can't "
                                                               "control what those things are - the GM does - but "
                                                               "they're generally beneficial to you.  In the past, "
                                                               "they've been: exploding heads, reversed gravity, time "
                                                               "dilation, gigantism and memory holes.  THe harder you "
                                                               "concentrate, the bigger the effect."},
                 "corrode": {"action_order": 3, "description": "Spend 1 Moxie to cause any small item you've touched "
                                                               "to rust, rot, corrode or break down in 30 seconds.  "
                                                               "It's difficult to damage large items or ones that are "
                                                               "further away but you can do it at a stretch."},
                 "cyrokinesis": {"action_order": 4, "description": "Spend 1 Moxie to significantly lower the "
                                                                   "temperature somewhere within your line of sight "
                                                                   "and create small patches of ice, slow down people "
                                                                   "or machiones and so on.  It's difficult to encase "
                                                                   "something in ice or lower the temperature enough "
                                                                   "to do serious harm to people but you can do it at "
                                                                   "a pinch."},
                 "electroshock": {"action_order": 8, "description": "Spend 1 Moxie to deliver a crackling burst of "
                                                                    "electricity from your palm that harms humans and "
                                                                    "stuns bots.  It's difficult to do it at anything "
                                                                    "longer than hand-to-hand range but you can do it "
                                                                    "at a stretch."},
                 "invisibility": {"action_order": 6, "description": "Spend 1 Moxie to turn yourself and your equipment "
                                                                    "invisible.  You can't turn others invisible.  "
                                                                    "It's difficult to stay unseen for more than a "
                                                                    "few seconds or if you stand in bright light but "
                                                                    "you can do it if you try harder."},
                 "levitation": {"action_order": 6, "description": "Spend 1 Moxie to hover up to a meter off the ground "
                                                                  "and move at a walking pace.  It's difficult to go "
                                                                  "higher, or faster, but you can do it with some "
                                                                  "effort.  Levitation can slow or stop falls."},
                 "machine empathy": {"action_order": 7, "description": "Spend 1 Moxie to cause any bot or AI (but not "
                                                                       "the Computer) to like and trust you for the "
                                                                       "remainder of the scene.  It's difficult to "
                                                                       "persuade a group of bots or to do it for "
                                                                       "longer than a scene, but you can do it if you "
                                                                       "try harder."},
                 "mental blast": {"action_order": 5, "description": "Spend 1 Moxie to let loose a mental blast on any "
                                                                    "clones within short range.  The blast can cause "
                                                                    "headaches and nosebleeds, maybe brief black-outs, "
                                                                    "up to - if you push it hard - permanent injury "
                                                                    "or death."},
                 "puppeteer": {"action_order": 5, "description": "Spend 1 Moxie to telepathically control a single "
                                                                 "limb from another clone within you line of sight.  "
                                                                 "It's dofficult to possess more than one limb (say, "
                                                                 "both legs, if you want them to walk somewhere) or "
                                                                 "to have them perform precise tasks buit you can do "
                                                                 "it at a stretch."},
                 "pyrokinesis": {"action_order": 4, "description": "Spend 1 Moxie to start a fire anywhere close to "
                                                                   "you.  It's difficult to start big fires, do it at "
                                                                   "a long distance or set a moving target on fire, "
                                                                   "but you can do it at a pinch."},
                 "strength": {"action_order": 9, "description": "Spend 1 Moxie to activate your super-strength and "
                                                                "lift heavy objects, run faster, jump further, hit "
                                                                "harder and so on.  It's difficult to lift really "
                                                                "heavy objects or jump really far but if you push "
                                                                "yourself you can do it."},
                 "telekinesis": {"action_order": 7, "description": "Spend 1 Moxie to push or pull small objects with "
                                                                   "the power of your mind.  It's difficult to move "
                                                                   "heavy objects (like people) or make precise "
                                                                   "movements (like pulling the trigger on a laser "
                                                                   "pistol) but you can do it at a stretch."},
                 "teleport": {"action_order": 5, "description": "Spend 1 Moxie to teleport yourself a short distance.  "
                                                                "It's difficult to teleport long distances or take "
                                                                "others with you but you can do it at a stretch.  "
                                                                "(You can't teleport something 'away' - you need to "
                                                                "go with it.)"},
                 "adhesive": {"action_order": 4, "description": "Spend 1 Moxie to secrete an adhesive substance from "
                                                                "your skin that you can use to attach things to other "
                                                                "things (or yourself to other things). The more you "
                                                                "concentrate, the more substance you exude and the "
                                                                "stronger the bond it can form."},
                 "charm": {"action_order": 5, "description": "Spend 1 Moxie to exude a pheromone that causes one "
                                                             "clone to like and trust you for the remainder of the "
                                                             "scene.  It's difficult to form bonds that last longer or "
                                                             "persuade while groups of people to trust you but you can "
                                                             "do it at a stretch."}}

SECRET_SOCIETIES = {"anti-mutant group":
                        {"keywords": ["order", "pro-human"],
                         "beliefs": "All Alpha Complex's troubles are down to mutants.  They're everywhere.  They're "
                                    "plotting and they must be eliminated.",
                         "goals": "To destroy all mutants.  The only good mutants are an oxymoron.  Look for evidence "
                                  "of a mutant conspiracy and destroy it.  Make people understand how dangerous "
                                  "mutants are.  Recruit new members."},
                    "communists":
                        {"keywords": ["isolate", "pro-human"],
                         "beliefs": "A fair and just system of government for all and for the end of the Computer's "
                                    "reign of terror.",
                         "goals": "Liberate the means of production and lift the yoke of toil from the shoulders of "
                                  "ordinary citizens.  Destroy the forces that stand in your way.  Give our pamphlets.  "
                                  "Recruit new members."},
                    "death leopards":
                        {"keywords": ["disorder", "explore"],
                         "beliefs": "Why worry when we can rock?  Party on.  Rebel.  Smash the system if your sober "
                                    "enough to find it.",
                         "goals": "To rock and roll all nightcycle, and party every daycycle!  Loud music, explosions, "
                                  "leather and booze are your secret passions.  Indulge your urges.  Freak the squares.  "
                                  "Recruit new members."},
                    "alpha complex local history research group":
                        {"keywords": ["explore", "pro-human"],
                         "beliefs": "History is interesting.  History tells us of Outside, where human destiny like, "
                                    "along with more cool stuff from the Time Before.",
                         "goals": "Discover and explore off-limits areas of Alpha Complex.  Find and analyse items and "
                                  "artifacts from the Time Before.  Recruit new members."},
                    "first church of christ computer programmer":
                        {"keywords": ["pro-tech", "isolate"],
                         "beliefs": "The Computer is God, literally.  Alpha Complex and its holy trinity of hardware, "
                                    "software and wetware, is perfect and must be protected from anyone who would "
                                    "change it.",
                         "goals": "Protect Alpha Complex.  Spread the message of peace, understanding and property "
                                  "commented code.  Find and hurt members of heretic schisms of FCCCP.  Recruit "
                                  "new members."},
                    "frankenstein destroyers":
                        {"keywords": ["pro-human", "disorder"],
                         "beliefs": "Humans are just as capable as machines.  Humans should run Alpha Complex.  "
                                    "Machines should be servants to humans or piles of smoking scrap, and smoking "
                                    "scrap is more fun.",
                         "goals": "Destroy all bots and usher in a human-only Alpha Complex.  Make sure that bots "
                                  "don't manage to get their oily claws into this mission.  Recruit new members."},
                    "free enterprise":
                        {"keywords": ["diversify", "progress"],
                         "beliefs": "Capitalism is good.  Raw, naked, bloody, hungry capitalism is better.  Trust the "
                                    "Market, the Market is your friend.",
                         "goals": "Sniff out good deals and new business opportunities.  Get one over on the other "
                                  "guy.  Ensure your superiors' business interests re represented during the mission.  "
                                  "Recruit new members."},
                    "illuminati":
                        {"keywords": ["much too secret to tell you"],
                         "beliefs": "Power and control.  The agenda doesn't matter as long as the Illuminati are "
                                    "controlling it.",
                         "goals": "Further the aims of the Illuminati.  Get ahead at any cost.  Infiltrate another "
                                  "secret society and subvert their agenda.  Recruit new members is they're suitable "
                                  "elite."},
                    "intsec":
                        {"keywords": ["order", "pro-tech"],
                         "beliefs": "You work for the Computer as an undercover agent, rooting out subversion and "
                                    "corruption among Troubleshooters.",
                         "goals": "Root out terrorists and the causes of terrorists wherever they rear their ugly "
                                  "heads.  be ruthless.  Don't get found out."},
                    "mystics":
                        {"keywords": ["explore", "diversify"],
                         "beliefs": "The Outside is inside us all and if you want to get into it you've got to get out "
                                    "of it.",
                         "goals": "To ingest, create and distribute mind-bending chemicals.  You've been chosen to "
                                  "spread the truth through Alpha Complex.  Develop new markets.  Recruit new members."},
                    "phreaks":
                        {"keywords": ["pro-tech"],
                         "beliefs": "Technology is cool, fun and easier to understand than human beings.  Used "
                                    "correctly, technology will save us all.",
                         "goals": "To wring the most out of technology and stop people using it incorrectly.  Hack, "
                                  "experiment with and steal wierd, expensive and rare technology.  Recruit new "
                                  "members."},
                    "psion":
                        {"keywords": ["progress"],
                         "beliefs": "Mutants are the future.  Homo Sapiens is as obsolete as the DX-503N laser-razor.",
                         "goals": "Further the pro-mutant agenda with propaganda, graffiti and cunning acts of "
                                  "subversion.  (If you don't have a mutant power yourself, you'll just have to hope "
                                  "that your origin story comes soon.)  Recruit new members, particularly other "
                                  "mutants."}
                    }

ACTIONS = {
    "A gun in the right place": {
        "desc": "You spot a ranged weapon useful to the action. Describe it; GM has veto over your description. The "
            "weapon adds +1 dice so long as it’s useful and intact. If the GM is particularly pleased by your "
            "description, it adds +2 dice this round and +1 dice thereafter.",
        "action_order": 5,
        "reaction": 0
    },
    "Adaptive Resources": {
        "desc": "You improvise a melee weapon out of something mundane. Describe what you find; GM has veto over your "
                "description. The weapon adds +1 dice so long as it’s useful and intact. If the GM is particularly "
                "pleased by your description, it adds +2 dice this round and +1 dice thereafter.",
        "action_order": 4,
        "reaction": 1
    },
    "An unexpected Boon": {
        "desc": "Play after a target has rolled but before the GM describes the outcome. Add 1 to the target’s score. "
                "Describe something that helps them out. GM has veto over your description.",
        "action_order": 0,
        "reaction": 1
    },
    "Called shot to the groin": {
        "desc": "The attack strikes your target in a very painful area but the effects aren’t permanent. Roll a die; "
                "if the target is an NPC, they’re out of action for that many rounds. If they’re a PC, they’re out "
                "of action for half that many rounds (rounding up).",
        "action_order": 3,
        "reaction": 1
    },
    "Collateral damage": {
        "desc": "An object is damaged as a side-effect of the action. Try to persuade your GM what was damaged and "
                "see if they listen to you. Good luck.",
        "action_order": 0,
        "reaction": 1
    },
    "Colossal Snafu": {
        "desc": "EVERYTHING HAS GONE WRONG! GM, pull out the thumbscrews.",
        "action_order": 0,
        "reaction": 1
    },
    "Combines assault": {
        "desc": "Pick another Troubleshooter. They can attack the same target as you immediately (and it doesnt "
                "count as taking their turn) at +1 or they can attack YOU immediately at +1. Their choice.",
        "action_order": 5,
        "reaction": 0
    },
    "Critical failure": {
        "desc": "SOMETHING GOES VERY WRONG! GM, you determine how.",
        "action_order": 0,
        "reaction": 1
    },
    "Critical success": {
        "desc": "SOMETHING GOES WAY BETTER THAN EXPECTED! GM, time to shine.",
        "action_order": 0,
        "reaction": 1
    },
    "Drop it": {
        "desc": "Play after a target has rolled but before the GM describes the outcome. The target fumbles and drops "
                "one piece of equipment they were holding in their hands. Try to persuade your GM what you want it "
                "to be and see if they listen to you.",
        "action_order": 0,
        "reaction": 1
    },
    "Easy come, easy go": {
        "desc": "Play on any face-up card on the table. That card is placed at the bottom of its respective deck; "
                "whatever its in-game effects were, they no longer apply. Describe what happened to cause this turn "
                "of events.",
        "action_order": 3,
        "reaction": 1
    },
    "Everything looks like a nail": {
        "desc": "You spot a tool that’s useful to the action. Describe it; GM has veto over your description. The "
                "tool adds +1 dice so long as it’s useful and intact. If the GM is particularly pleased by your "
                "description, it adds +2 dice this round and +1 dice thereafter.",
        "action_order": 4,
        "reaction": 1
    },
    "Feint": {
        "desc": "You spot a situation that you can exploit to confuse an enemy. Describe what it is, then roll "
                "Chutzpah + Bluff to take advantage. If you succeed, describe the actions of that enemy. The GM has "
                "veto over your description, so don’t go crazy.",
        "action_order": 2,
        "reaction": 1
    },
    "Flesh wound": {
        "desc": "Play on a target just as you or another PC is about to roll to attack them. If the roll is "
                "successful then the wound causes the target to lose a limb.",
        "action_order": 0,
        "reaction": 1
    },
    "Four's a crowd": {
        "desc": "Describe a group of NPCs who are useful to the action OR detrimental to the action, your choice; GM "
                "has veto over your description and controls the NPCs after this round ends.",
        "action_order": 1,
        "reaction": 1
    },
    "Function over form": {
        "desc": "Invent a decorative terrain feature (a screen, banner, statue and so on) that’s useful to the "
                "action; GM has veto over your creation. The feature adds +1 dice so long as the target uses it. If "
                "the GM is particularly pleased by your description, it adds +2 dice this round and +1 dice thereafter.",
        "action_order": 1,
        "reaction": 1
    },
    "Great victory": {
        "desc": "Everything goes right, above and beyond even the greatest expectations, for a few seconds at least. "
                "GM describes how.",
        "action_order": 0,
        "reaction": 1
    },
    "I'm going first": {
        "desc": "You act immediately, interrupting the target’s action. If they survive then they can resolve their "
                "action after you’re finished.",
        "action_order": 0,
        "reaction": 1
    },
    "Improvised defenses": {
        "desc": "You find a piece of armour or clothing that’s helpful to your current situation. Describe what you "
                "find; GM has veto over your description. The item adds +1 dice so long as it’s useful and intact. "
                "If the GM is particularly pleased by your description, it adds +2 dice this round and +1 dice "
                "thereafter.",
        "action_order": 3,
        "reaction": 0
    },
    "Jam": {
        "desc": "The target’s weapon jams. OR: The scene somehow now involves jam but the target’s weapon is "
                "perfectly functional. Your choice.",
        "action_order": 0,
        "reaction": 1
    },
    "Ka-boom!": {
        "desc": "Instead of hitting its target, a ranged attack (or another appropriate action if you think you can "
                "get away with it) hits something nearby that blows up with a 3-metre blast radius. Describe what it "
                "is. GM has veto over your description.",
        "action_order": 3,
        "reaction": 1
    },
    "Keep your head down": {
        "desc": "You find a hiding spot; describe it. You can Dodge any attacks until the start of the next round "
                "but you cannot do anything else till then.",
        "action_order": 6,
        "reaction": 0
    },
    "Lucky manual": {
        "desc": "Play after an attack that causes damage; it now causes no damage and instead destroys a piece of "
                "equipment carried by the target. The GM picks which.",
        "action_order": 0,
        "reaction": 1
    },
    "Man, am I pleased to see you": {
        "desc": "Describe a male-identifying NPC who’s useful to the action OR detrimental to the action, your "
                "choice; GM has veto over your description and controls the NPC after the end of the round. The NPC "
                "gives +1/-1 dice so long as they’re useful/impeding. If the GM is particularly pleased by your "
                "description, they give +2/2 dice this round and +1/-1 dice thereafter.",
        "action_order": 3,
        "reaction": 1
    },
    "Miss identified": {
        "desc": "Describe a female-identifying NPC who’s useful to the action OR detrimental to the action, your "
                "choice. GM has veto over your description and controls the NPC after the end of the round. The NPC "
                "gives +1/-1 dice so long as they’re useful/impeding. If the GM is particularly pleased by your "
                "description, they give +2/2 dice this round and +1/-1 dice thereafter.",
        "action_order": 4,
        "reaction": 1
    },
    "Mistaken identity": {
        "desc": "As far as everyone (including the Computer) is concerned, the target didn’t perform that action; "
                "someone else did. Try to persuade your GM who you want it to be and see if they listen to you.",
        "action_order": 0,
        "reaction": 1
    },
    "My lucky vent": {
        "desc": "Describe a convenient terrain feature (a crane, vent, steam pipe and so on) that’s useful to the "
                "action. GM has veto over your description. The feature adds +1 dice so long as the target uses it. "
                "If the GM is particularly pleased by your description, it adds +2 dice this round and +1 dice "
                "thereafter.",
        "action_order": 3,
        "reaction": 1
    },
    "Not so hot": {
        "desc": "Play after a target has rolled but before the GM describes the outcome. Delete 1 success roll from "
                "the target’s total. Describe something unexpected that hindered them. GM has veto over your "
                "description.",
        "action_order": 0,
        "reaction": 1
    },
    "Opposite Day": {
        "desc": "It’s not that everything goes wrong with the action, more that the exact opposite of what the "
                "target wanted to happen happens instead. GM, get creative.",
        "action_order": 4,
        "reaction": 1
    },
    "Party trick": {
        "desc": "You realise that this dangerous situation calls for an unusual application of your skills. Make an "
                "attack but pick a non-standard Stat and Skill combination then persuade the GM why they’re "
                "applicable in this particular situation (GM, be lenient). If they buy it, you get +2 successes. If "
                "they don’t, -1 success.",
        "action_order": 0,
        "reaction": 1
    },
    "Risky trick": {
        "desc": "Describe how the action becomes dangerous. You get +2 dice to any action but for every 1 rolled on a "
                "non-Computer dice, take 1 severity of wound. So on 1, you’re Hurt. On 2, you’re Injured and so on.",
        "action_order": 4,
        "reaction": 1
    },
    "Safety first": {
        "desc": "You notice a piece of safety equipment that’s useful to the action; GM has veto over your "
                "description. The item adds +1 dice so long as it’s useful and intact. If the GM is particularly "
                "pleased by your description, it adds +2 dice this round and +1 dice thereafter.",
        "action_order": 3,
        "reaction": 1
    },
    "Should have killed you": {
        "desc": "Play on an attack that causes damage. Now it causes no damage and instead the attacker loses a "
                "point of Moxie because they were convinced they’d hit and now they didn’t and they’re a bit freaked "
                "out.",
        "action_order": 0,
        "reaction": 1
    },
    "Slightly worse than expected": {
        "desc": "Play after someone has rolled but before the GM describes the outcome. Subtract 1 success from the "
                "roll. Describe something that hindered them. GM has veto over your description.",
        "action_order": 0,
        "reaction": 1
    },
    "Snap decision": {
        "desc": "Play this card at the start of the round to go first but deduct one dice from any roll you make this "
                "round. If another player also plays ‘Snap Decision’ they cancel each other out and neither PC gets "
                "an action this round.",
        "action_order": 10,
        "reaction": 0
    },
    "Sneak attack": {
        "desc": "You spot an enemy who is unaware of your presence. Make an attack at +2 to your NODE but swap "
                "Violence for Chutzpah, Stealth for Melee or both.",
        "action_order": 3,
        "reaction": 0
    },
    "Sudden death": {
        "desc": "If the action you’re playing this card on causes damage to a living thing or a bot, it "
                "automatically kills whatever got hit. Describe the death. GM has veto over your description.",
        "action_order": 0,
        "reaction": 1
    },
    "Suddenly, knives!": {
        "desc": "You spot a hand-to-hand weapon useful to the action. Describe it; GM has veto over your description. "
                "The weapon adds +1 dice so long as it’s useful and intact. If the GM is particularly pleased by your "
                "description, it adds +2 dice this round and +1 dice thereafter.",
        "action_order": 6,
        "reaction": 1
    },
    "Surprise bot": {
        "desc": "Describe a bot or AI who’s useful to the action OR detrimental to the action, your choice. GM has "
                "veto over your description. The NPC gives +1/-1 dice so long as they’re useful/impeding. If the GM "
                "is particularly pleased by your description, they give +2/-2 dice this round and +1/-1 dice "
                "thereafter.",
        "action_order": 4,
        "reaction": 1
    },
    "Tactical assessment": {
        "desc": "You realise something of vital importance. Say what it is, then make an appropriate Brains + a "
                "relevant skill check. If you succeed, everyone you choose (including yourself) is at +1 dice next "
                "turn so long as they heed your advice. If you fail, everyone (including yourself) is at -1 dice.",
        "action_order": 2,
        "reaction": 0
    },
    "Take your time": {
        "desc": "Describe what you’re planning to do – you’ll take the rest of the round to prepare your action. It "
                "happens last in the round but you get +2 dice to roll. If both Take Your Time cards are played in "
                "the same round, they resolve simultaneously.",
        "action_order": 10,
        "reaction": 0
    },
    "Taxi!": {
        "desc": "A vehicle appears that’s useful to the action. Describe it; GM has veto over your description. The "
                "vehicle adds +1 dice to rolls so long as it’s useful and intact. If the GM is particularly pleased "
                "by your description, it adds +2 dice this round and +1 dice thereafter.",
        "action_order": 2,
        "reaction": 1
    },
    "Up high": {
        "desc": "Describe an elevated terrain feature (a lift, gantry, some stairs and so on) that’s useful to the "
                "action. GM has veto over your description. The feature adds +1 dice so long as the target uses it. "
                "If the GM is particularly pleased by your description, it adds +2 dice this round and +1 dice "
                "thereafter.",
        "action_order": 2,
        "reaction": 1
    },
    "The wetter the better": {
        "desc": "Describe a liquid that’s useful to the action OR detrimental to the action, your choice. GM has "
                "veto over your description. The liquid gives +1/-1 dice if appropriate. If the GM is particularly "
                "pleased by your description, it gives +2/-2 dice this round and +1/-1 dice thereafter.",
        "action_order": 6,
        "reaction": 1
    },
    "Wrong target": {
        "desc": "The attack hits a different target from the one intended. Try to persuade your GM who you want it to "
                "be and see if they listen to you.",
        "action_order": 0,
        "reaction": 1
    }
}