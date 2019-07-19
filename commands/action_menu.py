from commands.library import _wrapper, titlecase
from world.static_data import ACTIONS, MUTANT_POWERS


def menu_start_node(caller):
    text = "There comes a time in every clone's life when they wanna do that thing that only comes natural.  Murder.  " \
           "Or whatever it is you kids call it these days.  Anyway, there are several types of actions you can take.  " \
           "Choose a category below to get started."
    options = ({"desc": "Equipment", "goto": "equipment_actions"},
               {"desc": "Actions", "goto": "action_card_actions"},
               {"desc": "Mutant Powers", "goto": "mutant_power_actions"})
    return text, options


def equipment_actions(caller):
    if hasattr(caller.ndb._menutree, "selected_item"):
        eq = caller.ndb._menutree.selected_item

        if eq.db.uses > 0:
            eq.db.uses = eq.db.uses - 1
            caller.location.msg_contents(eq)
        else:
            caller.msg('That item is our of uses.  Please visit the +catalog to recharge/reload it.')
        if eq.db.uses == 0 and eq.db.consumable:
            eq.delete()
        return "", ()
    text = "You are only as effective as how well you maintain your equipment.  These items are reusable and " \
           "persistent, but have to be refilled or recharged from time to time.  Any items that are out of uses will " \
           "not be shown here, even if they are in your inventory."
    options = ()

    for e in caller.contents:
        options += ({"desc": "{} - {} uses".format(e.key, e.db.uses) if e.db.uses > 0 else "{}".format(e.key),
                     "exec": _wrapper(caller, "selected_item", e), "goto": "equipment_actions"},)

    options += ({"key": ["back", "b"], "desc": "Go Back", "goto": "menu_start_node"},)
    return text, options


def action_card_actions(caller):
    if hasattr(caller.ndb._menutree, "selected_action"):
        selected_action = caller.ndb._menutree.selected_action
        action = ACTIONS.get(selected_action)
        caller.location.msg_contents(
            "|gSYSTEM:|n {}'s action: |w{}|n Order: |w{}|n {}".format(caller.key,
                selected_action, action.get("action_order"), "(reaction)" if action.get("reaction") == 1 else ""))
        caller.db.action_cards.remove(selected_action)
        return "", ()
    text = "The journey of a thousand miles begins with two in the bush.  Wise words.  Very wise words.  Actions are " \
           "things that you can do.  Once they are used, they are lose and you must purchase more.  Use them wisely." \
           "\n\nType |w+sheet/actions|n for more details."
    options = ()

    for act in caller.db.action_cards:
        options += ({"desc": act, "exec": _wrapper(caller, "selected_action", act), "goto": "action_card_actions"},)

    options += ({"key": ["back", "b"], "desc": "Go Back", "goto": "menu_start_node"},)
    return text, options


def mutant_power_actions(caller):
    power_name = caller.db.mutant_power
    power = MUTANT_POWERS.get(power_name)
    if hasattr(caller.ndb._menutree, "activate_power"):
        caller.location.msg_contents(
            "|gSYSTEM:|n {} activate their mutant power: {} Order: {}".
                format(caller.key, titlecase(power_name), power.get("action_order")))
        caller.db.moxie = caller.db.moxie - 1
        if caller.db.moxie == 1:
            caller.location.msg_contents("|gSYSTEM:|n {} completely LOSES IT! "
                                         "Consult the GM to determine the results.".format(caller.key))
        return "", ()
    text = "Treason huh?  Hey we've all done it.  You can't help how you were incubated.  It's just part of who you " \
           "are.  And who you are is a mutant.  A dirty, filthy mutant.  Well, might as well have some fun with it.  " \
           "Using your mutant powers costs 1 Moxie.  Remember, if your Moxie drops to 1, you will absolutely LOSE IT." \
           "\n\n|wPower:|n {}\n|wAction Order:|n {}\n|wDescription:|n {}".\
        format(power_name, power.get("action_order"), power.get("description"))
    options = ({"desc": "Activate", "exec": _wrapper(caller, "activate_power", 1), "goto": "mutant_power_actions"},
               {"key": ["back", "b"], "desc": "Go Back", "goto": "menu_start_node"})
    return text, options
