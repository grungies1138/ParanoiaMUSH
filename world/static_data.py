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

MUTANT_POWERS = {"telepathy": {"action order": 7, "description": "Spend 1 Moxie to read one dominant thought or "
                                                                 "implant a simple suggestion in another clone's "
                                                                 "mind.  It's difficult to read deeper memories, "
                                                                 "concoct elaborate lies or persuade them to do "
                                                                 "something they wouldn't normally but you can do it "
                                                                 "in a pinch."},
                 "anomoly": {"action order": 5, "description": "Spend 1 Moxie to make things happen.  You can't "
                                                               "control what those things are - the GM does - but "
                                                               "they're generally beneficial to you.  In the past, "
                                                               "they've been: exploding heads, reversed gravity, time "
                                                               "dilation, gigantism and memory holes.  THe harder you "
                                                               "concentrate, the bigger the effect."},
                 "corrode": {"action order": 3, "description": "Spend 1 Moxie to cause any small item you've touched "
                                                               "to rust, rot, corrode or break down in 30 seconds.  "
                                                               "It's difficult to damage large items or ones that are "
                                                               "further away but you can do it at a stretch."},
                 "cyrokinesis": {"action order": 4, "description": "Spend 1 Moxie to significantly lower the "
                                                                   "temperature somewhere within your line of sight "
                                                                   "and create small patches of ice, slow down people "
                                                                   "or machiones and so on.  It's difficult to encase "
                                                                   "something in oce or lower the temperature enough "
                                                                   "to do serious harm to people but you can do it at "
                                                                   "a pinch."},
                 "electroshock": {"action order": 8, "description": "Spend 1 Moxie to deliver a crackling burst of "
                                                                    "electricity from your palm that harms humans and "
                                                                    "stuns bots.  It's difficult to do it at anything "
                                                                    "longer than hand-to-hand range but you can do it "
                                                                    "at a stretch."},
                 "invisibility": {"action order": 6, "description": "Spend 1 Moxie to turn yourself and your equipment "
                                                                    "invisible.  You can't turn others invisible.  "
                                                                    "It's difficult to stay unseen for more than a "
                                                                    "few seconds or if you stand in bright light but "
                                                                    "you can do it if you try harder."},
                 "levitation": {"action order": 6, "description": "Spend 1 Moxie to hover up to a meter off the ground "
                                                                  "and move at a walking pace.  It's difficult to go "
                                                                  "higher, or faster, but you can do it with some "
                                                                  "effort.  Levitation can slow or stop falls."},
                 "machine empathy": {"action order": 7, "description": "Spend 1 Moxie to cause any bot or AI (but not "
                                                                       "the Computer) to like and trust you for the "
                                                                       "remainder of the scene.  It's difficult to "
                                                                       "persuade a group of bots or to do it for "
                                                                       "longer than a scene, but you can do it if you "
                                                                       "try harder."},
                 "mental blast": {"action order": 5, "description": "Spend 1 Moxie to let loose a mental blast on any "
                                                                    "clones within short range.  The blast can cause "
                                                                    "headaches and nosebleeds, maybe brief black-outs, "
                                                                    "up to - if you push it hard - permanent injury "
                                                                    "or death."},
                 "puppeteer": {"action order": 5, "description": "Spend 1 Moxie to telepathically control a single "
                                                                 "limb from another clone within you line of sight.  "
                                                                 "It's dofficult to possess more than one limb (say, "
                                                                 "both legs, if you want them to walk somewhere) or "
                                                                 "to have them perform precise tasks buit you can do "
                                                                 "it at a stretch."},
                 "pyrokinesis": {"action order": 4, "description": "Spend 1 Moxie to start a fire anywhere close to "
                                                                   "you.  It's difficult to start big fires, do it at "
                                                                   "a long distance or set a moving target on fire, "
                                                                   "but you can do it at a pinch."},
                 "strength": {"action order": 9, "description": "Spend 1 Moxie to activate your super-strength and "
                                                                "lift heavy objects, run faster, jump further, hit "
                                                                "harder and so on.  It's difficult to lift really "
                                                                "heavy objects or jump really far but if you push "
                                                                "yourself you can do it."},
                 "telekinesis": {"action order": 7, "description": "Spend 1 Moxie to push or pull small objects with "
                                                                   "the power of your mind.  It's difficult to move "
                                                                   "heavy objects (like people) or make precise "
                                                                   "movements (like pulling the trigger on a laser "
                                                                   "pistol) but you can do it at a stretch."},
                 "teleport": {"action order": 5, "description": "Spend 1 Moxie to teleport yourself a short distance.  "
                                                                "It's difficult to teleport long distances or take "
                                                                "others with you but you can do it at a stretch.  "
                                                                "(You can't teleport something 'away' - you need to "
                                                                "go with it.)"},
                 "adhesive": {"action order": 4, "description": "Spend 1 Moxie to secrete an adhesive substance from "
                                                                "your skin that you can use to attach things to other "
                                                                "things (or yourself to other things). The more you "
                                                                "concentrate, the more substance you exude and the "
                                                                "stronger the bond it can form."},
                 "charm": {"action order": 5, "description": "Spend 1 Moxie to exude a pheromone that causes one "
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