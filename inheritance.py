from typing import List
from random import randint

class Character:

    def __init__(self, family_tree: object, given_name: str, type: object, weapon_skill: str,
        attribute: str, ability: str) -> None:
        """
        :param type: class of character (warrior)
        :param weapon_skill: type of weapon specialty (axes, swords, lances, bows, tomes, staves)
        :param attribute: personal attribute bonus chosen (strength, agility, intellect)
        :param ability: personal ability chosen (dual weilding, blocking, avoiding, tome reading)
        """

        self.name = given_name
        self.type = type.name
        self.weapon_skill = weapon_skill
        self.attribute = attribute
        self.ability = ability

        # set stats equal to basic character (3,3,3) + innate class bonuses
        self.innate_stats = self.set_innate_stats(type.strength_bonus, type.agility_bonus, type.intellect_bonus)
        self.innate_stats[attribute] += 1

        # past reincarnations and their stat benefits to you
        bonus_skills = family_tree.inherited_base_stats()

        if len(bonus_skills) > 2:
            self.innate_stats['strength'] += bonus_skills[0]
            self.innate_stats['agility'] += bonus_skills[1]
            self.innate_stats['intellect'] += bonus_skills[2]

        print('My name is {}! I am a mighty {} with proficient skill in {} and a special attribute in {}. '
              'Additionally, I\'ve always been reaaaally good at {}.\n'.format(self.name, self.type, self.weapon_skill,
                                                                            self.attribute, self.ability))

        print('Your total skill points gained from ancestors is {}'.format(str(bonus_skills)))
        print('Here are my stats: {}\n'.format(str(self.innate_stats)))

    def set_innate_stats(self, strength_bonus:int, agility_bonus:int, intellect_bonus:int) -> dict:
        return {'strength': 3 + strength_bonus, 'agility': 3 + agility_bonus, 'intellect': 3 + intellect_bonus}

    def __str__(self) -> str:
        return self.name

class Type:
    pass

class Warrior(Type):

    def __init__(self) -> None:
        self.strength_bonus = 3
        self.agility_bonus = 1
        self.intellect_bonus = 0
        self.name = 'warrior'


class Mage(Type):

    def __init__(self) -> None:
        self.strength_bonus = 0
        self.agility_bonus = 1
        self.intellect_bonus = 3
        self.name = 'mage'

class Rogue(Type):

    def __init__(self) -> None:
        self.strength_bonus = 1
        self.agility_bonus = 2
        self.intellect_bonus = 1
        self.name = 'rogue'


class Inheritance:

    def __init__(self) -> None:
        self.family_tree = []

        # classes found in the inheritance of the family
        self.warriors = 0
        self.rogues = 0
        self.mages = 0

        # type of 'super inheritances' obtained randomly
        self.normal = 0 # normal birth
        self.awakened = 0 # special birth 20%
        self.empowered = 0 # kekkei touta 2%
        self.unleashed = 0 # godlike 0.1%
        # self.ascended = 0 # final tier, something like 0.01%

    def add_new_relative(self, character: Character) -> None:
        """
        Add a new relative to the overall Inheritance scheme
        :param character: user to add to family tree
        :return: Nothing
        """
        self.family_tree.append(character)
        if (character.type == 'warrior'):
            self.warriors += 1
        elif (character.type == 'rogue'):
            self.rogues += 1
        elif (character.type == 'mage'):
            self.mages += 1

    def inherited_base_stats(self) -> List[int]:
        bonus_stats = [0, 0, 0]

        if len(self.family_tree) < 1:
            return bonus_stats

        count = self.count_bonus()

        for char in list(reversed(self.family_tree)): # main loop where all previous characters in the lineage all
            # give a small part
            # of their power to the current character
            # this loop should traverse backwards because the very first ancestor should have the least effect
            # compared to the actual 'father' of the child
            bonus_stats[0] += self.inherited_skill(char, 'strength') * count
            bonus_stats[1] += self.inherited_skill(char, 'agility') * count
            bonus_stats[2] += self.inherited_skill(char, 'intellect') * count

            count = count / 2 # constant divisor to minimize effect of old generations on child (1, 0.5, 0.25, 0.125...)

        # round up to nearest?
        for stat in range(0,len(bonus_stats)):
            if bonus_stats[stat] - int(bonus_stats[stat]) >= 0.5:
                bonus_stats[stat] += 1
            bonus_stats[stat] = int(bonus_stats[stat])

        return bonus_stats

    def count_bonus(self) -> float:
        """
        function which returns the 'count' variable, which determines how powerful of an influence your ancestors
        have over your bonus stats (a count of 1 means your father passes on his ENTIRE stats, 0.5 of your
        grandfather, 0.25 great grandfather, etc.
        :return: influence 'count' to be passed back to the main ancestor stat bonuses method
        """
        count = 0.25

        if randint(0, 100) < 20: # chance of a reincarnation - meaning you inherit much more (ashura) 20%
            print('Woah! Your birth was special... you have inhereted much stronger bonds than usual! Check if you '
                  'obtained the Sharingan.')
            count = 0.5
            if randint(0, 100) < 10: # 10% of the 20% takers (2%)
                print('This is unbelievable. You are a prodegy. Think Kekkei Touta in Naruto.')
                count = 1
                if randint(0, 100) < 5: # 5% of the previous 2% (0.1%) total
                    print('There could be nothing stronger. You are blessed with the power of many different bloodlines '
                          'intertwining to create a near omnipotent being - yourself.')
                    count = 2
                    #print('Ok. You might not realize how rare this is. If you don\'t beat the game this time, you suck.')


        if (count == 0.25):
            self.normal += 1
        elif (count == 0.5):
            self.awakened += 1
        elif (count == 1):
            self.empowered += 1
        elif (count == 2):
            self.unleashed += 1


        return count

    def inherited_skill(self, character: Character, attribute: str) -> float:
        bonus = character.innate_stats[attribute]
        if character.attribute == attribute:
            bonus += 1
        return bonus

    def family_tree_types(self) -> str:
        return 'Your family tree contains: {} warriors, {} rogues, {} mages.'.format(str(self.warriors), \
               str(self.rogues), str(self.mages))
    def family_tree_super_inheritences(self) -> str:
        return 'Your family tree contains: {} normal members, {} awakened members (sharingan users), {} empowered ' \
               'members (kekkei touta), {} unleashed members (post war narutos).'.format(str(self.normal),
               str(self.awakened), str(self.empowered), str(self.unleashed))

    def __str__(self) -> str:
        return str(self.family_tree)

your_family = Inheritance()

writing = ''

for i in range(0,21):
    num = randint(0,2)
    some = None
    if num == 0:
        some = Warrior()
    elif num == 1:
        some = Rogue()
    else:
        some = Mage()
    character = Character(your_family, 'Test', some, 'daggers', 'strength', 'stealth')
    your_family.add_new_relative(character)
print(your_family.family_tree_types())
print(your_family.family_tree_super_inheritences())


writing = 'quit'
while (writing != 'quit'):
    your_name = input("Your character's name? ")
    your_type = input("Your character's class? ")
    if (your_type == 'warrior'):
        your_type = Warrior()
    elif (your_type == 'rogue'):
        your_type = Rogue()
    else:
        your_type = Mage()

    your_weapon = input("Your character's weapon? ")
    your_attribute = input("Your character's special attribute? str/agl/int ")
    your_ability = input("Your character's ability? ")
    character = Character(your_family, your_name, your_type, your_weapon, your_attribute, your_ability)
    your_family.add_new_relative(character)

    writing = input("Create a new character? 'quit' to exit")

print("see ya!")