#!/usr/bin/env python3
"""
dolmenwood_chargen.py – Dolmenwood Character Generator
Based on: Dolmenwood Player's Book (Necrotic Gnome, 2023)

Usage:
    # Random character, no restrictions
    python dolmenwood_chargen.py

    # Allow only specific kindreds
    python dolmenwood_chargen.py --kindred human breggle

    # Exclude specific classes
    python dolmenwood_chargen.py --exclude-class magician enchanter

    # Combine filters
    python dolmenwood_chargen.py --kindred human breggle --exclude-class magician

    # Fix kindred or class
    python dolmenwood_chargen.py --kindred human --class fighter

    # Save to Obsidian vault
    python dolmenwood_chargen.py --kindred human breggle --exclude-class magician --save --campaign dolmenwood

    # Generate multiple characters (for player choice)
    python dolmenwood_chargen.py --count 3 --kindred human breggle
"""

import argparse
import random
import sys
import re
from pathlib import Path
from datetime import datetime

# ─── TRINKET TABLES (d100, 50 entries each) ───────────────────────────────────

TRINKETS = {
    "breggle": [
        "A bag of divination stones that always answer 'Panic' to any question.",
        "A bloodstained jester's hat.",
        "A bloody knife that cannot be cleaned.",
        "A blue velvet jacket with a hidden pocket which moves when you're not looking.",
        "A book of poetry that consists primarily of bleating.",
        "A bottle of noxious perfume. When sprayed, it can be smelt up to half a mile away.",
        "A brass owl statue with eerie black eyes.",
        "A broken fishing rod that still displays teeth marks from an enormous fish.",
        "A circular ceramic amulet which displays the current moon phase.",
        "A clay pot labelled 'Frog Paste,' containing what appears to be frog paste.",
        "A clump of writhing, black moss that you scraped off a looming monolith one lonely night.",
        "A collection of papers with scrawled notes detailing your life story, found on a drowned stranger.",
        "A curious mossling wind instrument carved out of a gourd.",
        "A diorama of two stuffed mice riding stuffed squirrels, jousting.",
        "A dried mushroom with a face.",
        "A folio of pressed sprite-wings.",
        "A gnarled root shaped like a mossling.",
        "A letter warning that several unnamed longhorns are secretly crookhorns in disguise.",
        "A locket with a portrait of a fluffy cat wearing a crown: 'For the love of King Pusskin.'",
        "A long-nosed masquerade mask.",
        "A moleskin wristband, anointed with exotic fairy perfume.",
        "A mossling pipe that blows rainbow-coloured smoke rings.",
        "A necklace of miscellaneous humanoid teeth.",
        "A petrified turnip.",
        "A pig heart that oozes ichor when squeezed.",
        "A pouch which feels heavy (as if full of pebbles) even when empty.",
        "A rusty scalpel that once belonged to Lord Malbleat.",
        "A sack of tasty fried chicken legs.",
        "A scale said to be from a breggle with a fishtail instead of legs.",
        "A scroll containing a prophetic warning from an esteemed ancestor—almost indecipherable.",
        "A sheet of parchment with a charcoal sketch of your long lost love.",
        "A short length of silver cord and a delicate hook, said to catch fairy fish in puddles.",
        "A shovel stained with the dirt of a thousand graves.",
        "A stuffed vole dressed in a charming waistcoat.",
        "A thigh-bone flute.",
        "A tin whistle whose tones drive cats wild.",
        "A tiny book of nonsense poetry, bound in purple leather.",
        "A tiny painting of a four-horned goat.",
        "A well-loved walking stick with a goat's head handle.",
        "A wooden Chapes (holy symbol of the Pluritine Church) studded with nails.",
        "An empty notebook. Anything written in it disappears at sunrise.",
        "An ornate pie pan, pilfered from a noble's kitchen.",
        "Black stone dice with white skulls for pips.",
        "Expensive-looking (but worthless) jewellery, designed for breggle horns.",
        "String from the bow of a legendary hunter.",
        "The board pieces for fairy chess. You have no idea what the rules are.",
        "The cured skin of a whole deer.",
        "The horn of an ancestor, hung from a necklace.",
        "The key to the prison cell you escaped from.",
        "Your grandmother's creepy glass eye. You sometimes feel her presence watching you.",
    ],
    "elf": [
        "A bag of caterpillars whose flesh has hallucinogenic properties.",
        "A bag of sticky sweets that never get any smaller when sucked on.",
        "A ball of silvery twine that is invisible in moonlight.",
        "A ball of yarn, gifted to you by a grateful grimalkin.",
        "A black rose that never wilts.",
        "A block of chocolate made with cocoa harvested from a mossling.",
        "A book of amateur poetry—you suspect the author to be a powerful Fairy noble.",
        "A crown woven from holly and poison ivy.",
        "A daisy that glows in moonlight.",
        "A fancy hat topped with elk antlers.",
        "A fragment of glowing crystal that you found in a dream.",
        "A fragment of horn from an evil unicorn.",
        "A glass bottle that annihilates any liquid poured into it.",
        "A glass jar containing the tiny, frozen form of your only sister.",
        "A glass slipper, stained with blood.",
        "A harp that, if left unattended, plays mood-inappropriate music with amateurish skill.",
        "A Chapes (holy symbol of the Pluritine Church), given to you by a dying friar decades ago.",
        "A key fashioned from ice. It melts in the warmth, and reforms in cold weather.",
        "A lantern that burns with a cold, blue flame when lit.",
        "A letter promising your imminent demise, written in High Elfish. Delivered over a century ago.",
        "A mortal's heart, freely given.",
        "A mote of sunlight, trapped in a scintillating crystal.",
        "A necklace composed of honeybees.",
        "A nightmare, sealed inside a bottle.",
        "A pan flute stolen from a woodgrue—a single pipe is missing.",
        "A peacock feather whose eye intermittently blinks.",
        "A pleasant dream, distilled into a liquor.",
        "A receipt for a loan of four rare tomes from a Fairy library. You no longer have the books.",
        "A scabbard taken from the fallen body of a great knight.",
        "A sealed scroll allegedly containing one of the Goblin King's myriad names.",
        "A seemingly ordinary acorn. Screams when its cap is removed.",
        "A set of horseshoes, designed for a centaur.",
        "A silver spoon that drips honey on command.",
        "A single crow feather, taken from the cloak of the Queen of Blackbirds.",
        "A skeletal finger that scrapes at dusk and writes macabre prophecies when given ink.",
        "A small bell shaped like a breggle's eye. Faint bleating accompanies its ringing.",
        "A spider that slowly weaves webs in the shape of clothing.",
        "A spyglass that always shows a view of a sea at night.",
        "A thimble that is always magically full of sweet liqueur.",
        "A white-and-gold parasol that creates darkness directly underneath it.",
        "A wolf pelt cloak. The wolf's head is still attached and occasionally salivates.",
        "An ancient bronze mask depicting a bearded face.",
        "An empty wine bottle that draws liquid inside until full when held over it.",
        "An hourglass which constantly flows in one direction and cannot be inverted.",
        "An icicle that never melts.",
        "Bronze chimes that tinkle in the presence of both ghosts and strong breezes.",
        "Sculpting tools, preternaturally cold to the touch.",
        "Six vials of blood, each drawn from a different Kindred.",
        "Star charts that match no sky seen from Dolmenwood.",
        "The severed tail of a fairy horse.",
    ],
    "grimalkin": [
        "A bicorne hat that is a foot deeper on the inside than it appears.",
        "A book of long-forgotten laws, written in Old Woldish.",
        "A brass thimble that turns water into milk.",
        "A breggle tongue, still moist.",
        "A cherry tart pilfered from the kitchen of a fairy noble.",
        "A cloak fashioned from a hundred voles.",
        "A copper coin that always lands on the same side when deliberately flipped.",
        "A crimson feather from an enormous bird.",
        "A dead crow that never rots.",
        "A deck of playing cards that shuffles itself when left unattended.",
        "A dried heart the size of an acorn.",
        "A hairball coughed up by a famous grimalkin.",
        "A handkerchief stained with the kiss of Queen Abyssinia.",
        "A heart-shaped locket—each time opened, it contains a portrait of a different cat.",
        "A human eye that dilates just before it rains.",
        "A hundred-year-old note offering a favour in return for services. Descendants may be obligated.",
        "A leaf from the tallest tree in Dolmenwood.",
        "A letter begging you to aid a miller's youngest child.",
        "A live cockroach tied to a thin gold string. A new one appears at sunrise if removed.",
        "A lucky tortoise shell.",
        "A lute that is always out of tune in the morning and in tune in the evening.",
        "A luxurious, gold-embroidered cushion.",
        "A mouse skull on a string (allegedly, a mouse from the moon).",
        "A mushroom stolen from the head of a mossling.",
        "A nightingale's song, trapped in a locket.",
        "A pair of boots that will never go out of fashion.",
        "A pair of dice that, when rolled together, always total to nine.",
        "A pink bow that cannot turn invisible under any circumstances.",
        "A pocket watch that always tells you the correct time an hour ago.",
        "A porcelain teacup with a painted salamander. Warm liquids held inside never cool down.",
        "A rabbit's foot that sporadically twitches.",
        "A rat king in a sack—each rat claims to be the 'King of All Rats.'",
        "A realistic mask of a human child.",
        "A scroll depicting your royal lineage. Of dubious authenticity.",
        "A set of keys on a golden ring, purloined from a noble.",
        "A severed head of a sprite, dried and preserved.",
        "A sewing needle, sized for a giant (treat as a dagger).",
        "A shard of cold iron, trapped in a glass sphere.",
        "A single cat whisker, given to you as a sign of commitment.",
        "A singular pipe, taken from a woodgrue's pan flute.",
        "A small vial containing a legendarily potent strain of catnip.",
        "A tiny bell that makes no sound.",
        "A trained, but not particularly smart, weasel.",
        "A whistle that only dogs can't hear.",
        "A wolf's paw that bleeds when the wolf is thinking of you.",
        "A wooden door the shape and size of a mouse.",
        "An eyepatch, stained with old blood.",
        "An ogre's toenail, tough as steel. Its owner still lives.",
        "Eyeglasses haunted by benign ghosts—wearing them lets you see the ghosts.",
        "One of a pair of bracelets made from braided mouse tails.",
    ],
    "human": [
        "A black stone which always points towards the sun.",
        "A blood sausage, allegedly made of wyrm's blood.",
        "A blood-stained handkerchief that won't wash clean.",
        "A bone statuette of a mermaid with prodigiously hairy armpits.",
        "A bright red egg that was given to you by a sprite.",
        "A clay effigy that whispers to you in your sleep.",
        "A cracked marble that falls in slow motion.",
        "A deck of cards illustrated with blindfolded kings, queens, and knaves.",
        "A drinking horn carved with cavorting nymphs.",
        "A dubious fake moustache made of rat fur.",
        "A fine set of silver cutlery and a floral china tea-set, packed in a wicker hamper.",
        "A foot-long, spicy sausage.",
        "A gauntlet of wyrm scales.",
        "A goatskin pouch full of giblets.",
        "A head-sized glass sphere with a neck opening.",
        "A hunk of ancient, mouldy cheese.",
        "A jar that breeds flies, even when tightly sealed.",
        "A jaunty cap (with a feather) which jumps up whenever anyone says your name.",
        "A lavender scented cushion embroidered with black roses and thorns.",
        "A lock of hair from the first person you killed.",
        "A long kilt of woven moss.",
        "A love letter you are penning in silver ink to your fairy betrothed.",
        "A miniature brass gnome (appears on your pillow looking at you each morning).",
        "A napkin and cutlery that you stole from a fancy inn.",
        "A note from your mother admonishing you to return home.",
        "A pair of stripy woollen socks that keep your feet as warm as fine boots.",
        "A pebble that glows faintly in the dark.",
        "A piece of the moon that fell to earth (or is it a hunk of desiccated cheese?).",
        "A porcelain teapot painted with a scene of owls devouring humans.",
        "A raven's feather quill that writes without ink.",
        "A silver belt woven from the mane of a kelpie.",
        "A silver mirror that always reflects the sky.",
        "A silver ring that shrinks or expands to fit whatever finger it is placed upon.",
        "A tiny fish in a jar of water—at night it surfaces and whispers names of those within 5'.",
        "A tiny wicker effigy that you stole from a witch's hut.",
        "A unicorn statuette carved out of mushroom-wood.",
        "A wanted poster for yourself.",
        "A well-thumbed and annotated book of psalms.",
        "An ash wand stained with the blood of a troll.",
        "An enormous Green Man brass belt buckle.",
        "An ornate lantern you found in a bog.",
        "Sixteen silver pieces, greased with slippery magical oil that cannot be washed off.",
        "The broken tip of a unicorn's horn.",
        "The fairy sword that slew your father.",
        "The mummified hand of a bog body.",
        "The scintillating, silvery feather of a witch owl.",
        "The skeleton of an especially large toad, in pieces.",
        "The skull of a Drune, stolen from a forbidden crypt.",
        "The wobbly, pink severed hand of a gelatinous ape, still fresh and sweet.",
        "Your grandfather's beard, rolled up in a hessian cloth.",
    ],
    "mossling": [
        "A bag of stone marbles. Each has a name and rolls towards whoever speaks it.",
        "A block of cheese infected with hallucinogenic fungus.",
        "A bloodstained hat that once belonged to a redcap.",
        "A book alleging crimes by each of the 100 saints of Dolmenwood—found on a murdered man.",
        "A bottle of yeast-froth shampoo, essential for maintaining the lustre of mossy manes.",
        "A bouquet of honeysuckle that drips real honey. The honey attracts wasps.",
        "A brass cowbell. When struck, nearby milk and cheese products jump half a foot towards it.",
        "A broad-brimmed hat covered in shimmering moss.",
        "A bronze idol to a two-headed mushroom god.",
        "A chunk of volcanic rock, warm to the touch. An Old Woldish rune has been carved into it.",
        "A clay figurine of a pot-bellied giant with a single eye.",
        "A cluster of fungus consisting of a dozen different kinds of mushrooms living in symbiosis.",
        "A collection of small rocks, all chipped from different gravestones.",
        "A cooking pot that adds mushrooms to every dish cooked inside it.",
        "A flower pressed inside a dead man's journal.",
        "A hunting horn fashioned from a great boar tusk.",
        "A jar of blue cheese massage oil.",
        "A jar of green jelly with the label 'Don't Eat Me.'",
        "A large egg, entrusted to you by a panicked woodgrue.",
        "A large gooseberry that appears to have a creature growing inside it.",
        "A large, pink sausage. Tries to crawl away if left unattended.",
        "A leaf that changes with the seasons, dying by winter only to rejuvenate in spring.",
        "A mossy rock that produces bugs when lifted after a minute on the ground.",
        "A mould-riddled tapestry depicting the hunt for a swine of mythic size.",
        "A puffball with dozens of tiny mouths which burp in unison at dawn.",
        "A puffball-skin pouch filled with jelly.",
        "A sack of half-empty ale bottles.",
        "A sealed bottle of spirits, brewed from the composted remains of one of your ancestors.",
        "A shepherd's crook that induces fear in farm animals when brandished.",
        "A single hair from the head of an elven lady, a token of her affection.",
        "A small beetle you found—you've since received a letter from a grimalkin charging you with its theft.",
        "A small effigy of a breggle made from dried mushroom flesh.",
        "A small pouch of magic nuts. When broken open, each nut emits a pearl of wisdom.",
        "A small snake with a 'Return to' note attached. The owner's name is smudged out.",
        "A small, hollow toadstool with a tiny wooden door.",
        "A snail shell that grows a new snail at dawn if the old one is removed or killed.",
        "A squirrel-sized collar and leash.",
        "A story book about the charming exploits of the rat-people of the moon.",
        "A unique pipeweed mix of your own invention. A bit too combustible.",
        "A watering can that constantly trickles water from its spout.",
        "A waterskin of yellow slime that drips upwards when unstoppered.",
        "A wheel of cheese that never loses momentum once it starts rolling.",
        "A wooden carving of yourself that ages as you do.",
        "A wooden peg leg that you found and converted into an incubator for rare fungi.",
        "A worm whose squirming slowly spells out threatening prophecies.",
        "An adorable red-and-white button mushroom. Whispers to you when no one else is listening.",
        "An incomplete, and possibly inaccurate, map of all the inns in Dolmenwood.",
        "An onion shaped like a baby.",
        "Blueprints for a marvellous mechanical mouse organ clock.",
        "Dozens of different kinds of bark, stitched together like a book.",
    ],
    "woodgrue": [
        "A bag of delicious boiled sweets.",
        "A basket of snakes, intended for juggling.",
        "A battered hat with a stuffed swan's head stitched proudly at the summit.",
        "A bone whistle. When blown at night, it sends nearby bats and night birds into a frenzy.",
        "A bottle containing dirty water from the Baths of Astralon.",
        "A bottle of ink that always seems to spill everywhere when opened.",
        "A bronze statuette of a chimera made up of a dozen different animals.",
        "A burial shroud imprinted with a face that becomes more distinguishable every day.",
        "A ceramic plate that emits a simple tune when scratched.",
        "A collection of fungi, loaned to you by a mossling.",
        "A dead crow in a bag—before you killed it, you were sure it was spying on you.",
        "A fake moustache. When worn, you appear to have a full beard.",
        "A forbidden treatise claiming grimalkins and woodgrues share the same ancestors.",
        "A glass case with a giant moth pinned inside.",
        "A harp shaped like a duck. Playing it attracts nearby waterfowl.",
        "A harp string, sharp and tinged with blood.",
        "A hooded cloak made from thousands of moth wings stitched together.",
        "A mead tankard that is perpetually sticky.",
        "A misshapen ocarina. Each note sounds eerily similar to a baby's cries.",
        "A mossling pipe you found in a pile of compost. Its smoke makes people nostalgic.",
        "A note promising that a 'Mr Fox' will come to your aid in your hour of greatest need.",
        "A pair of matching eyeballs. Whenever possible, they rotate to stare at you.",
        "A pair of small, bronze cymbals.",
        "A personalised invitation to 'THE FEAST.' No further details are provided.",
        "A pocketbook of bad jokes. Emits the occasional snicker.",
        "A poster for your parent's last, ill-fated circus performance.",
        "A quill made from a stirge-owl feather.",
        "A rope woven from a mix of human and breggle hair.",
        "A stack of angry letters, all accusing you of arson.",
        "A strange disk that produces the sound of flatulence whenever a weight is placed atop it.",
        "A tent that slowly raises itself when you loudly sing it a jaunty song.",
        "A vial of guano. Your last reminder of a deceased loved one.",
        "A wooden sceptre topped with a jester's head. When struck, tells an ill-considered joke.",
        "An advice book that ultimately suggests a liberal application of fire to every problem.",
        "An ancient coin, stolen from a grave. Far colder to the touch than it should be.",
        "An empty pan flute case, its contents stolen.",
        "An enormous firework with a tag that reads 'Untested.'",
        "An extravagant wig, stolen from the head of an elf noble.",
        "An ordinary-looking metal bucket. When filled with water, leeches appear inside.",
        "An ornate flute, said to be handed down by your ancestors since before they left Fairy.",
        "An unhatched egg that sweats blood.",
        "Faded parchment listing the names of everyone you've ever wronged. It updates itself.",
        "Light from a fireworks display, caught in a shard of glass.",
        "Lyrics to a half-written song about rodents visiting from the moon.",
        "Small vials of syrups, each labelled with the mood they're supposed to cure.",
        "The corpse of a mouse, dressed in tiny clothes.",
        "The crest of an unknown longhorn noble house, found on a dead breggle.",
        "The squirming pieces for maggot chess.",
        "Woollen ear warmers, knitted by your grandmother.",
        "Your uncle's famed recipe for moth cakes.",
    ],
}

# ─── APPEARANCE TABLES (d12 each) ─────────────────────────────────────────────

APPEARANCE = {
    "breggle": {
        "Head": [
            "Dented helm with coat of arms", "Ears pierced with nails or rings",
            "Long, curly locks", "Long, floppy ears", "Narrow, pointed ears",
            "One bent horn, one straight", "One horn broken off", "Silver stripe in hair",
            "Slick, oiled hair", "Spiky ginger hair", "Thin neck, hefty head",
            "Third nub horn on forehead",
        ],
        "Face": [
            "Black eyes, silver pupils", "Buck teeth", "Bushy brows", "Golden eyes",
            "Lank forelock droops over eyes", "Long, wispy chin-beard",
            "Milky white eyes, blue flecks", "Missing teeth", "Prominent scar",
            "Shaggy chin-beard", "Small eyes, close set", "Wide, drooling mouth",
        ],
        "Fur": [
            "Black, flecked with silver", "Black, glossy", "Ginger, curly", "Ginger, rough",
            "Grey, greasy", "Grey, lustrous", "Russet, spiky", "Russet, wavy",
            "Tan, coarse", "Tan, shaggy", "White, dirty", "White, fluffy",
        ],
        "Dress": [
            "Doublet and frilly shirt", "Greasy woollens", "Grimy apron",
            "Huge, hairy overcoat", "Long skirts and cloak", "Patched leather, many pockets",
            "Rabbit and squirrel fur", "Servant's livery", "Thigh boots and waistcoat",
            "Thong and dashing cape", "Tweed and deerstalker", "Wide, armless frock",
        ],
        "Demeanour": [
            "Ale-addled", "Cool-headed pragmatist", "Cultivated aristocratic air",
            "Dour, pessimistic", "Earnest, loyal", "Endlessly scheming",
            "Flighty, mercurial", "Jocular with violent outbursts", "Mellow, unflappable",
            "Single-minded, stubborn", "Wild hedonist", "Wryly philosophical",
        ],
        "Desires": [
            "Eradicate the Drune", "Escape justice for past crime", "Found a crime syndicate",
            "Free the common folk", "Imprison all crookhorns", "Marry into nobility",
            "Outrageous wealth and luxury", "Popularise turnip ale", "Recover ancient breggle lore",
            "Restore High Wold to Ramius", "Swindle Lord Murkin's wealth", "Travel and discovery",
        ],
        "Beliefs": [
            "Ancestors demand sacrifices", "Breggles made standing stones",
            "Breggles originate in Fairy", "Church hides breggle saints",
            "Daily garlic wards fairy hexes", "Descendant of a mighty wizard",
            "Duke is thrall of the Drune", "Fairy is purely mythical",
            "Malbleat serves the Nag-Lord", "Malbleat will rule High Wold",
            "Nag-Lord is breggle messiah", "The end is nigh",
        ],
        "Speech": [
            "Cackling", "Circuitous", "Coarse", "Gurgling", "High-pitched",
            "Lackadaisical", "Mumbling", "Rumbling", "Staccato", "Throaty",
            "Warbling", "Whining",
        ],
    },
    "elf": {
        "Head": [
            "Delicate, pointed ears", "Floppy, ass-like ears", "Flowing, silver hair",
            "Foppish wig", "Glossy, iridescent hair", "Gold hair at day, grey at night",
            "Hair as white as snow", "Hair like cobwebs", "Lustrous, waist-length hair",
            "Ragged, cropped hair", "Shadowy locks", "Small, ivory horn nubs",
        ],
        "Face": [
            "Androgynous", "Eye colour shifts with season", "Feline eyes",
            "Frosted blue lips", "Glow of candlelight on skin", "Long, distinguished nose",
            "Pale and mask-like", "Spotted with soot", "Star-shaped pupils",
            "Violet eyes", "Wide-eyed, childlike", "Wide-set almond eyes",
        ],
        "Body": [
            "Aroma of mead or honey", "Aura of dancing glimmers", "Bluish skin",
            "Faintly insubstantial", "Golden blood, silver tears", "Lithe frame, sex unclear",
            "Odour of fresh spring dew", "Pale skin, black in mirrors", "Skin appears moonlit",
            "Skin of a newborn", "Skin rimed with frost", "Sparkling skin",
        ],
        "Dress": [
            "Chequered harlequin", "Cloak of black feathers", "Cloak of frost",
            "Cobwebs and soot", "Decaying regal finery", "Elaborately embroidered",
            "Extravagant, frilly lace", "Lace and flowers", "Mother of pearl gown",
            "Sheer black", "Silvery gossamer", "Woven leaves",
        ],
        "Demeanour": [
            "Affected nobility", "Aloof and amoral", "Childlike and mischievous",
            "Decadent", "Gleeful enthusiasm", "Keenly naive", "Loquacious",
            "Melancholic aesthete", "Obsessive", "Sardonic observer", "Wilful and whimsical",
            "World-weary",
        ],
        "Desires": [
            "Break mortal hearts", "Collect exotic stuffed beasts", "Depose fairy lord or lady",
            "Distil wines from emotions", "Forbidden arcane lore", "Library of dreams",
            "Odd magical trinkets", "Return of the Cold Prince", "Savour finest of mortal life",
            "To grow old and die", "Understand mortal religion", "Usurp noble house",
        ],
        "Beliefs": [
            "All plants are sentient", "Cats are disguised fairies", "Daylight is to be shunned",
            "Drink only fine wine", "Magic is the true language", "Mortal world is but a dream",
            "Mortals evolved from fungi", "Reality is a fabulous song", "The world is dying",
            "Time is seeping into Fairy", "Understand speech of stars", "Witches led by fairy queen",
        ],
        "Speech": [
            "Condescending", "Distant and slightly echoing", "Flat and toneless",
            "Flirtatious", "Like the cracking of ice", "Lilting", "Mirthful",
            "Pitch changes: deep/high", "Poetic and obscure", "Song and rhyme",
            "Subtly threatening", "Whispering",
        ],
    },
    "grimalkin": {
        "Head": [
            "Carefully sculpted quiff", "Dapper top hat", "Extravagant ear fur",
            "Floppy beret", "Floppy ear", "Jaunty tricorn hat", "Plumed hat",
            "Pointy ear tufts", "Shaggy mane", "Spotted headscarf", "Torn ear",
            "Unrealistically large",
        ],
        "Face": [
            "Bug-eyed", "Constantly looks surprised", "Copper, saucer-like eyes",
            "Extra fluffy cheeks", "Extravagantly long whiskers", "Flabby jowls",
            "Flashing silver eyes", "Long, pointy snout", "Mostly mouth",
            "Snaggle-toothed", "Snub nose", "Tongue pokes out",
        ],
        "Fur": [
            "Black", "Black and white", "Blue", "Brown tabby", "Chocolate",
            "Ginger tabby", "Iridescent", "Silver, fluffy", "Tortoiseshell",
            "Violet", "White, spiky", "White, fluffy",
        ],
        "Dress": [
            "Cape and spurs", "Dandyish lace and silks", "Festooned with rat bones",
            "Jet black woollens", "Long gloves and chaps", "Long, colourful knitted scarf",
            "Pied doublet and breeches", "Ratskin vest and breeches", "Regal ermine cloak",
            "Shiny red boots", "Smart tweed", "Tassels and fringes",
        ],
        "Demeanour": [
            "Boastful", "Fastidious and precise", "Irreverently jocund", "Jittery and on edge",
            "Loose with money", "Mercurial", "Reckless swashbuckler", "Self-indulgent preening",
            "Slumbersome", "Sneaky and larcenous", "Snobbish gourmet", "Tipsy and frolicsome",
        ],
        "Desires": [
            "Become a crime lord", "Become fat eating rodents", "Build a secret palace",
            "Build a sky ship to the moon", "Commune with lost cat gods",
            "Fame as a slayer of monsters", "Found a catnip distillery",
            "Infamy as a supreme gambler", "Inhabit Hoarblight Keep",
            "Live in exorbitant luxury", "Marry into human nobility", "Steal the duke's jewels",
        ],
        "Beliefs": [
            "Catnip is poison to humans", "Consume mouse-flesh daily",
            "Dreams are the true reality", "Evil rat realm underground",
            "Human nobles serve Catland", "Magic is fading", "Only eat raw meat",
            "The Cold Prince is long dead", "The moon is ruled by mice",
            "The Nag-Lord adores cats", "Vegetables harm the health", "War is brewing in Fairy",
        ],
        "Speech": [
            "Adorable mewling", "Conspiratorial whispering", "Decadently fashionable",
            "Eloquent and poetic", "Impertinent", "Languid", "Manic", "Meandering",
            "Mirthful and mocking", "Purring", "Sycophantic", "Wilfully abstruse",
        ],
    },
    "human": {
        "Head": [
            "Cropped or shaven hair", "Embroidered skull cap", "Fur hat with animal tail",
            "Jaunty cap with feather", "Jug ears", "Long braids",
            "Meticulously oiled hair", "Misshapen skull", "Patchy, straggly hair",
            "Poised atop an elegant neck", "Thick, lustrous hair", "Wild, curly hair",
        ],
        "Face": [
            "Bent nose", "Button nose", "Darting eyes", "Droll, lupine mouth",
            "Gap-toothed", "Hirsute", "Large, regal nose", "Narrow, pinched",
            "Pimples", "Prominent scar", "Rosy", "Wide, spaced out features",
        ],
        "Body": [
            "Barrel chest", "Big hands", "Blotchy skin", "Excessively hairy",
            "Freckles", "Long legs", "Long, elegant fingers", "Oily skin",
            "Pocked with plague-scars", "Pot belly", "Smooth, supple skin", "Warts",
        ],
        "Dress": [
            "Colourful patchwork", "Dashing doublet and hose", "Enigmatic cloak and hood",
            "Filthy woollens", "Hessian rags", "Lace, posies, and frills",
            "Noisome furs", "Padded vest and breeches", "Sheepskin coat",
            "Smoking jacket and slacks", "Sturdy boots and raincoat", "Way-worn leathers",
        ],
        "Demeanour": [
            "Brooding, quick-tempered", "Curious, broad-minded", "Dour, single-minded",
            "Enthusiastic, gullible", "Gregarious", "Impatient and rash", "Kindly",
            "Miserly", "Scheming", "Self-aggrandising", "Slovenly", "Suave",
        ],
        "Desires": [
            "Build castle and new village", "Clear family name", "Collect saintly relics",
            "Domestic bliss", "Explore Fairy", "Found business empire", "Infamy",
            "Map stones of Dolmenwood", "Marry into nobility", "Redeem past misdeeds",
            "Secret underground lair", "Squander fortune on luxury",
        ],
        "Beliefs": [
            "Bishop is a werewolf", "Drune will enslave the duke", "Fairies steal human souls",
            "Nag-Lord brings final doom", "One parent was an elf", "Prayers redeem evil deeds",
            "Shroom of immortality", "Sunken village in Longmere", "Talking beasts plot uprising",
            "The dead are rising", "Visions from the Cold Prince", "Witches serve the Nag-Lord",
        ],
        "Speech": [
            "Agitated", "Bellowing", "Cackling", "Coarse", "Conspiratorial",
            "Gravelly", "Inane banter", "Mellow", "Mumbling", "Nasal whine",
            "Rapid", "Sighing",
        ],
    },
    "mossling": {
        "Head": [
            "Bald like a polished nut", "Buzzing with flies", "Floppy hat droops over eyes",
            "Fuzzy green hair", "Huge floppy ears", "Long greasy hair",
            "Much too big", "No neck", "Patchy orange hair", "Pointy felt hat",
            "Wobbly", "Wrinkled like a walnut",
        ],
        "Face": [
            "Beard of frothy yeast", "Darting tongue", "Eyes as big as fists",
            "Eyes like pools of deep space", "Eyes like tiny black marbles",
            "Long, floppy nose", "Looks like a carved potato", "Massive flared nostrils",
            "Mouth foaming with yeast", "Nostrils ooze purple slime", "Pointy root nose",
            "Wobbly lips",
        ],
        "Body": [
            "Blubbery", "Covered in downy fur", "Flabby rolls", "Lumpy",
            "Rampant belly button fur", "Spherical", "Stubby legs", "Stumpy arms",
            "Whorled like knotted wood", "Wider than tall", "Wobbly paunch",
            "Wrinkled folds of skin",
        ],
        "Dress": [
            "Brushed felt", "Cosy knitwear", "Dapper tweed", "Greasy leathers",
            "Grubby rags", "Knitted ivy", "Loincloth", "Naturist", "Pelts",
            "Pig suede", "Scratchy wool", "Woven fungus stems",
        ],
        "Demeanour": [
            "Blustery", "Brooding", "Cowardly", "Dozy", "Flustered", "Grumpy",
            "Impertinent", "Lethargic", "Miserly", "Overbearingly affable", "Shrewd",
            "Tells terrible jokes",
        ],
        "Desires": [
            "A dozen spouses", "Acquire moon cheese", "Become a fungus giant",
            "Breed a sentient swine", "Brew the universal elixir", "Consume sentient fungi",
            "Found a moss brewery", "Found underground realm", "Grow clones of self",
            "Meld with the fungal mind", "Own a sprawling inn", "Sample all known ales",
        ],
        "Beliefs": [
            "Ale is essential for life", "Bathing is inimical to health",
            "Daily sacrifice to the elders", "Gets visions from the moon",
            "Humans are naked monkeys", "Pursued by vengeful ghosts",
            "Stone circles hide buried gold", "Talking owls are plotting",
            "The Drune will conquer all", "The duke is secretly a fairy",
            "The fungal mind is supreme", "The trees have eyes",
        ],
        "Speech": [
            "Baritone", "Filthy", "Grumbling", "Meandering", "Mumbling", "Muttering",
            "Obtuse", "Phlegmy", "Squeaking", "Squelchy", "Stammering", "Wheezy",
        ],
    },
    "woodgrue": {
        "Head": [
            "Bald, veiny ears", "Blotchy bald pate", "Cap of shiny beetle shells",
            "Ears ooze orange wax", "Elongated, teetering neck", "Felt hat with long liripipe",
            "Floppy hat, way too big", "Long, bristling hair tufts", "Pink mohawk (natural)",
            "Round, droopy ears", "Stripe of silver hair", "Twitching, pointy ears",
        ],
        "Face": [
            "Droopy nose", "Lavishly preened moustache", "Lustrous black beard",
            "Nose flesh changes colour", "Nostrils flap when excited",
            "Nostrils dripping yellow snot", "Oiled moustache", "One large eye, one small",
            "Protruding fangs", "Sagging, bloated throat", "Shifty eyes constantly blink",
            "Straggly beard",
        ],
        "Body": [
            "Flaps of skin between fingers", "Hunchback", "Knock-kneed",
            "Pink skin with white fuzz", "Prehensile feet", "Rotund", "Scrawny",
            "Skin flaps under arms", "Spindly, 4-knuckled fingers",
            "Thick, matted, auburn fur", "Utterly hairless", "Vestigial wings (flightless)",
        ],
        "Dress": [
            "Dangling bells and baubles", "Enigmatic black cloak", "Heavily patched",
            "Hessian loin cloth", "Knotted cords", "Long, ragged cape",
            "Mismatched, stolen clothes", "Paint-daubed rags", "Pied jester's outfit",
            "Soft brushed suede", "Stockings and baggy jumper", "Stripy hose and bodice",
        ],
        "Demeanour": [
            "Bends the truth", "Capers and japes", "Childlike and curious",
            "Cunning, scheming", "Dour, gallows humour", "Feigned mysticism",
            "Frivolous and petty", "Penchant for pilfery", "Practical joker",
            "Shady and unscrupulous", "Trickster (but loyal friend)", "Wide-eyed innocence",
        ],
        "Desires": [
            "Be accepted as a saint (as a joke)", "Build manor half in Fairy",
            "Burn down a castle", "Found a secret society", "Giant bee mead brewery",
            "Live in a castle of bats", "Marry a goblin merchant",
            "Organise largest moot ever", "Perform for the Nag-Lord",
            "Popularise moth sausages", "Rule a human town in secret",
            "Steal secrets of the Drune",
        ],
        "Beliefs": [
            "Crows are spies from Fairy", "Fairies are illusory", "Fungi are souls of the dead",
            "Get all agreements in writing", "Gold buried in graveyards",
            "Humans can't dance", "Immune to fire", "Live on cake alone",
            "Nearly perfected deadly song", "Never reveal your name",
            "Penal system must be a joke", "The Nag-Lord really is a wag",
        ],
        "Speech": [
            "Childish giggling", "Excited screeching", "Guffawing",
            "Hesitant warbling", "Hissing and slurping", "Intermittent gibbering",
            "Languid rumbling", "Melodious", "Punctuated with hoots",
            "Shrill", "Sinister whispering", "Staccato",
        ],
    },
}

# ─── MOSSLING SPECIAL TABLES ──────────────────────────────────────────────────

MOSSLING_SYMBIOTIC_FLESH = [
    "Outer parts of ears replaced by jelly fungus.",
    "Patches of lichen.",
    "Dainty flowers bloom in the beard in springtime.",
    "Yeast infections in moist places.",
    "Toadstools growing from joints.",
    "Covered in slimy, green jelly.",
    "Miniature tree growing from ear.",
    "Skin riddled with mycelia.",
    "Eyes fur over with transparent, yellow mould.",
    "Edible toe cheese.",
    "Growths of woody, bracket fungus in the armpits.",
    "Mossy feet.",
    "Climbing vines wrapped around limbs and torso.",
    "Radical fern growth around groin.",
    "Mossy biceps.",
    "Puffball growths around the buttocks and knees.",
    "Parsley chest hair.",
    "Blackberry brambles tangled in the hair.",
    "Edible mushrooms growing in hair.",
    "Semi-sentient mushroom growing from top of head.",
]

MOSSLING_KNACKS = [
    ("Bird Friend", "Converses with birds; charm bird companion (Lvl 3); twittering message 12 mph (Lvl 5); summon flock 1d4 Turns (Lvl 7)."),
    ("Lock Singer", "Open simple locks 2-in-6/Turn; locate key (Lvl 3); snap locks shut 30' (Lvl 5); open any lock (Lvl 7)."),
    ("Root Friend", "Question a root 1d6 words 1/day; summon edible roots 1d4 rations (Lvl 3); shelter in roots up to 1 hour (Lvl 5); summon root thing 1/day (Lvl 7)."),
    ("Thread Whistling", "Tie/untie/unravel threads; animate threads up to 20 coin weight (Lvl 3); rope mastery (Lvl 5); animate rope to attack (Lvl 7)."),
    ("Wood Kenning", "Touch wood 1 Turn: sense creator/last toucher; sense recent emotion (Lvl 3); see through wooden barrier (Lvl 5); learn tree's true name (Lvl 7)."),
    ("Yeast Master", "Touch ferments sweet liquids (1 pint/Turn); commune with yeast to learn drinker's name (Lvl 3); yeasty belch stuns 1d6 Rounds (Lvl 5); conjure yeasty feast 1d6 rations (Lvl 7)."),
]

# ─── KINDRED DATA ─────────────────────────────────────────────────────────────

KINDREDS = {
    "human": {
        "type": "mortal",
        "size": "Medium",
        "languages": ["Woldish"],
        "allowed_classes": ["bard", "cleric", "enchanter", "fighter", "friar", "hunter", "knight", "magician", "thief"],
        "common_classes": ["bard", "cleric", "fighter", "friar", "hunter", "knight", "magician", "thief"],
        "restricted_classes": [],
        "special_traits": [
            "Decisiveness: When Initiative is tied, humans act first.",
            "Leadership: Retainer Loyalty +1.",
            "Spirited: +10% bonus to all XP earned.",
        ],
        "age_base": 15,
        "age_roll": "2d10",
        "height_base_m": "5'4\"",
        "height_base_f": "5'",
        "height_roll": "2d6\"",
        "ac_bonus": 0,
        "names_male": ["Arfred","Brom","Bunk","Chydewick","Crump","Dimothy","Guillem","Henrick","Hogrid",
                       "Jappser","Joremey","Josprey","Jymes","Mollequip","Rodger","Rogbert","Samwise",
                       "Shadwell","Shank","Sidley"],
        "names_female": ["Agnel","Amonie","Celenia","Emelda","Gertwinne","Gilly","Gretchen","Gwendolyne",
                         "Hilda","Illabell","Katerynne","Lillibeth","Lillith","Lisabeth","Mabel","Maydrid",
                         "Melysse","Molly","Pansy","Roese","Winifred"],
        "names_unisex": ["Andred","Arda","Aubrey","Clement","Clewyd","Dayle","Gemrand","Hank","Lyren",
                         "Maude","Megynne","Moss","Robyn","Rowan","Sage","Tamrin","Ursequine","Waldra",
                         "Waydred","Wendlow"],
        "surnames": ["Addercapper","Burl","Candleswick","Crumwaller","Dogoode","Dregger","Dunwallow",
                     "Fraggleton","Gruewater","Harper","Lank","Logueweave","Loomer","Malksmilk","Smith",
                     "Sunderman","Swinney","Tolmen","Weavilman","Woodwick"],
        # d100 backgrounds (weighted; stored as flat list for simplicity, weights approximate)
        "backgrounds": [
            "Actor","Angler","Angler","Angler","Angler","Animal trainer","Apothecary",
            "Baker","Baker","Baker","Barber","Beekeeper","Beggar","Beggar","Beggar",
            "Blacksmith","Blacksmith","Blacksmith","Bookbinder","Brewer","Brewer",
            "Butcher","Butcher","Butcher","Carpenter","Carpenter","Carpenter","Carpenter",
            "Cartographer","Cattle farmer","Cattle farmer","Cattle farmer","Chandler",
            "Cheesemaker","Cobbler","Cooper","Dockhand","Fortune-teller","Fur trapper",
            "Gambler","Gambler","Glassblower","Grave digger","Hog farmer","Hog farmer",
            "Hunter","Hunter","Hunter","Hunter","Jester","Jeweller","Leather worker",
            "Locksmith","Merchant","Miner","Miner","Outlaw","Outlaw","Pedlar","Pedlar",
            "Pilgrim","Poacher","Poacher","Potter","Roper","Sailor","Scribe",
            "Servant","Servant","Servant","Servant","Sheep farmer","Sheep farmer",
            "Shipwright","Smuggler","Stable hand","Stonemason","Swindler","Tailor",
            "Tax collector","Thatcher","Turnip farmer","Turnip farmer","Turnip farmer",
            "Unicorn hunter","Vagrant","Vagrant","Wainwright","Wayfarer","Wayfarer",
            "Weaver","Weaver","Wheat farmer","Wheat farmer","Wheat farmer",
            "Wizard's assistant","Woodcutter","Woodcutter","Woodcutter","Woodcutter",
        ],
    },
    "breggle": {
        "type": "mortal",
        "size": "Medium",
        "languages": ["Woldish", "Gaffe", "Caprice"],
        "allowed_classes": ["bard", "cleric", "enchanter", "fighter", "friar", "hunter", "knight", "magician", "thief"],
        "common_classes": ["fighter", "knight", "magician", "bard", "thief", "hunter"],
        "restricted_classes": ["cleric", "friar"],  # rare, not forbidden
        "special_traits": [
            "Horns: Natural melee attack (1d4 dmg at Lvl 1–3; 1d6 at Lvl 4–6; 1d8 at Lvl 7+).",
            "Fur: +1 AC when unarmoured or wearing Light armour.",
            "Gaze (from Lvl 4, Longhorn status only): Charm a human or shorthorn; Save vs Spell or charmed until sunrise. 1/day.",
        ],
        "ac_bonus": 1,  # +1 when unarmoured/light armour
        "age_base": 15,
        "age_roll": "2d10",
        "names_male": ["Aele","Braembel","Broob","Crump","Drerdl","Frennig","Grerg","Gripe","Llerg",
                       "Llrod","Lope","Mashker","Olledg","Rheg","Shadgore","Shadwell","Shadwicke",
                       "Shandor","Shank","Snerd"],
        "names_female": ["Aedel","Berrild","Bredhr","Draed","Fannigrew","Frandorup","Grendilore","Grendl",
                         "Grewigg","Hildrup","Hraigl","Hwendl","Maybel","Myrkle","Nannigrew","Pettigrew",
                         "Rrhimbr","Shord","Smethra","Wheld"],
        "names_unisex": ["Addle","Andred","Blocke","Clover","Crewwin","Curlip","Eleye","Ellip","Frannidore",
                         "Ghrend","Grennigore","Gwendl","Hrannick","Grennick"],
        "surnames": ["Blathergripe","Bluegouge","Bockbrugh","Bockstump","Elbowgen","Forlocke","Hwodlow",
                     "Lankshorn","Lockehorn","Longbeard","Longshanks","Shankwold","Smallbuck","Snicklebock",
                     "Snidebleat","Snoode","Underbleat","Underbuck","Wolder","Woldleap"],
        "backgrounds": ["Alchemist's assistant","Angler","Beekeeper","Blacksmith","Brewer","Chandler",
                        "Devil goat handler","Gambler","Grave digger","Merchant","Onion farmer","Page",
                        "Pig farmer","Servant","Smuggler","Sorcerer's assistant","Standard-bearer",
                        "Thatcher","Turnip farmer","Vagrant"],
    },
    "elf": {
        "type": "fairy",
        "size": "Medium",
        "languages": ["Woldish", "Sylvan", "High Elfish"],
        "allowed_classes": ["bard", "enchanter", "fighter", "hunter", "knight", "magician", "thief"],
        "common_classes": ["enchanter", "fighter", "hunter", "magician"],
        "restricted_classes": ["cleric", "friar"],  # forbidden - no spiritual connection
        "special_traits": [
            "Glamours: Knows 1 random glamour.",
            "Immortality: Cannot die of old age or natural disease.",
            "Unearthly Beauty: +2 Charisma (max 18) when interacting with mortals.",
            "Magic Resistance: +2 to saves vs magic.",
            "Vulnerable to Cold Iron: Cold iron weapons deal +1 damage.",
            "Elf Skills: Skill Target 5 for Listen and Search.",
        ],
        "ac_bonus": 0,
        "age_base": 100,
        "age_roll": "1d100x10",
        "names": {
            "rustic": ["Bucket-and-Broth","Candle-Bent-Sidewise","Glance-Askew-Guillem","Jack-of-Many-Colours",
                       "Lace-and-Polkadot","Lament-of-Bones-Broken","Lightly-Come-Softly","Lillies-o'er-Heartsight",
                       "Prick-of-the-Nail","Silver-and-Quicksilver","Spring-to-the-Queen","Sprue-Upon-Gallows",
                       "Sun's-Turning-Tide","Supper-Before-Noon","Too-Soon-Begotten","Trick-of-the-Light",
                       "Tryst-about-Town","Tumble-and-Thimble","Wine-By-The-Goblet","Wry-Passing-Noon"],
            "courtly": ["Begets-Only-Dreams","Breath-Upon-Candlelight","Chalice-of-Duskviolet",
                        "Dream-of-Remembrance","Gleanings-of-Lost-Days","Hands-Bound-By-Crows",
                        "Impudence-Hath-Victory","Indigo-and-Patchwork","Marry-No-Man",
                        "Morning's-Last-Mists","Murder-of-Ravens","Quavering-of-Night",
                        "Revenge's-Sweet-Scent","Seven-Steps-At-Dawn","Shade-of-Winter-Betrayal",
                        "Shallow-Pained-Plight","Shallow-Spirit's-Lament","Slips-Behind-Shadows",
                        "Spring-Noon's-Arrogance","Dusk-Upon-Silver-Water"],
        },
        "backgrounds": ["Chronicler","Coiffeur","Confectioner","Courtier","Dream thief","Elk hunter",
                        "Explorer","Frost sculptor","Harpist","Highway robber","Librarian","Mountebank",
                        "Nut forager","Peacock trainer","Poet","Swordsmith","Tailor","Thespian",
                        "Unicorn handler","Vintner"],
    },
    "grimalkin": {
        "type": "fairy",
        "size": "Small",
        "languages": ["Woldish", "Mewl"],
        "allowed_classes": ["bard", "enchanter", "fighter", "hunter", "magician", "thief"],
        "common_classes": ["enchanter", "thief", "bard", "hunter"],
        "restricted_classes": ["cleric", "friar"],
        "special_traits": [
            "Three Forms: Estray (humanoid cat, normal form), Chester (fat moggy, unlimited shifts, AC 12, bite+2 claws 1 dmg each), Wilder (fey predator, 1/day when in melee at <half HP, heals 2d6 HP, AC 13, bite+2 claws 1d4, +2 Attack, lasts 2d4 Rounds).",
            "Defensive Bonus: +2 AC when in melee with Large creatures.",
            "Eating Giant Rodents: After 1 Turn devouring a freshly killed giant rodent, heals 1 HP.",
            "Glamours: Knows 1 random glamour.",
            "Immortality: Cannot die of old age or natural disease.",
            "Magic Resistance: +2 to saves vs magic.",
            "Vulnerable to Cold Iron: Cold iron weapons deal +1 damage.",
            "Repulsion to Silver: Touch of silver causes nausea.",
        ],
        "ac_bonus": 0,
        "age_base": 100,
        "age_roll": "1d100x10",
        "names_first": ["Boots","Fripple","Ginger","Jack","Jill","Jaspy","Jasqueline","Kitty","Little",
                        "Lord","Lady","Mogget","Moggle","Monsieur","Madame","Nibbles","Penny","Poppet",
                        "Prince","Princess","Prissy","Tippsy","Tomkin","Toppsy"],
        "surnames": ["Bobblewhisk","Cottonsocks","Flip-a-tail","Flippancy","Fluff-a-kin","Grimalgrime",
                     "Grinser","Lickling","Milktongue","Mogglin","Poppletail","Pouncemouse","Pusskin",
                     "Ratbane","Snuffle","Tailwhisk","Tippler","Whippletongue","Whipsy","Whiskers"],
        "backgrounds": ["Alchemist's aide","Angler","Barber","Card-sharp","Catnip brewer","Clothier",
                        "Duellist","Highway robber","Knifemaker","Libertine","Mariner","Pheasant poacher",
                        "Rat hunter","Spy","Stage magician","Swindler","Thespian","Trapper/furrier",
                        "Vole farmer","Weasel tamer"],
    },
    "mossling": {
        "type": "mortal",
        "size": "Small",
        "languages": ["Woldish", "Mulch"],
        "allowed_classes": ["bard", "cleric", "fighter", "friar", "hunter", "magician", "thief"],
        "common_classes": ["fighter", "hunter", "magician", "thief"],
        "restricted_classes": [],
        "special_traits": [
            "Knacks: Roll 1d6 for a knack (special skill tree with powers at Levels 1/3/5/7).",
            "Symbiotic Flesh: Roll 1d20 at Level 1 (and each new Level) for a fungal/plant growth.",
            "Resilience: +4 to saves vs fungal spores and poisons; +2 to all other saves.",
            "Mossling Skills: Skill Target 5 for Survival (foraging only).",
            "Note: Chainmail = bark armour; plate mail = pinecone armour for mosslings.",
        ],
        "ac_bonus": 0,
        "age_base": 50,
        "age_roll": "3d6",
        "names_male": ["Dombo","Gobd","Gobulom","Golobd","Gremo","Gwomotom","Hollogowl","Kabob",
                       "Kollobom","Limbly","Loblow","Mobdemold","Nyoma","Obolm","Oglom","Omb",
                       "Shmold","Slumbred","Umbertop","Wobobold"],
        "names_female": ["Bilibom","Brimbul","Ebbli","Ghibli","Gobbli","Gwedim","Higwold","Ibulold",
                         "Imbwi","Klibli","Klimbim","Libib","Limimb","Marib","Milik","Shlirimi",
                         "Shobd","Skimbim","Slimpk","Smodri"],
        "names_unisex": ["Bendiom","Blobul","Ebdwol","Glob","Gombly","Greblim","Gwoodwom",
                         "Hollb","Klolb","Kwolotomb","Lambop","Morromb","Mwoomb","Olob","Shlurbel",
                         "Smodron","Tomdown","Tomumbolo","Worrib"],
        "surnames": ["Barkhop","Conker","Danklow","Fernhead","Frother","Grimehump","Hogscap","Mossbeard",
                     "Mossfurrow","Mould","Mouldfinger","Mudfoot","Mugfoam","Mulchwump","Mushrump",
                     "Oddpolyp","Puffhelm","Smallcheese","Sodwallow","Twiggler"],
        "backgrounds": ["Bark tailor","Boar hunter","Beekeeper","Cheesemaker","Compost raker",
                        "Fungologist","Fungus farmer","Gambler","Horn blower","Moss brewer",
                        "Moss farmer","Night forager","Oracle's apprentice","Pipe maker",
                        "Sausage maker","Squirrel trainer","Swineherd","Tavernkeep","Vagrant",
                        "Worm farmer","Yeast farmer"],
    },
    "woodgrue": {
        "type": "demi-fey",
        "size": "Small",
        "languages": ["Woldish", "Sylvan"],
        "allowed_classes": ["bard", "enchanter", "fighter", "hunter", "magician", "thief"],
        "common_classes": ["bard", "enchanter", "thief", "hunter"],
        "restricted_classes": ["cleric", "friar"],
        "special_traits": [
            "Mad Revelry: 1/day, play one of 6 melodies in 30' radius—Confide, Dance, Imbibe, Jape, Jubilate, Mount. Targets Save vs Spell or are compelled.",
            "Moon Sight: Darkvision 60'.",
            "Compulsive Jubilation: Must partake in any party or feast encountered (Save vs Spell to resist).",
            "Defensive Bonus: +2 AC vs Large creatures (when in melee).",
            "Remnant Glamours: Knows 1 random glamour (diminished fairy magic).",
            "Vulnerable to Cold Iron: Cold iron weapons deal +1 damage.",
            "Long-lived: Lifespan 300+ years but not immortal.",
            "Musical Instrument: Can use wind instrument as melee weapon (1d4 dmg). Always starts with one.",
        ],
        "ac_bonus": 0,
        "age_base": 50,
        "age_roll": "3d6",
        "names_male": ["Bagnack","Barmcudgel","Bloomfext","Bunglebone","Capratt","Chimm","Delgodand",
                       "Drunker","Eortban","Grunkle","Gubber","Gumroot","Gunkuss","Kungus","Longtittle",
                       "Lubbal","Olpipes","Runkelgate","Weepooze","Wumpus"],
        "names_female": ["Bishga","Canaghoop","Cheruffue","Doola","Frogfyrr","Gruecalle","Hoolbootes",
                         "Maulspoorer","Mogsmote","Molemoch","Moonmilk","Munmun","Nettaclare","Oorcha",
                         "Palliepalm","Pimplepook","Puggump","Rolliepolk","Sasserpipe","Whipsee"],
        "names_unisex": ["Bogfrink","Bongwretch","Chunder","Danklob","Frondbong","Gobblebag","Hootbra",
                         "Longsnipe","Lumpfrisk","Mabmungle","Mungus","Obblehob","Oddler","Oodler",
                         "Pipplepoke","Slovend","Umple","Unclord","Undermap","Whoopla"],
        "surnames": ["Bobbleslime","Bogbabble","Bootswap","Chumley","Cobwallop","Drooglight","Dungobble",
                     "Eggmumble","Hogslapper","Hortleswoop","Hungerslip","Lankwobble","Moorsnob",
                     "Mundersnog","Pencecrump","Persnickle","Shunderbog","Snodgrass","Wallerbog","Woodfuffle"],
        "backgrounds": ["Circus performer","Convicted arsonist","Court jester","Crow hunter",
                        "Dung collector","Egg thief","Errant piper","Firework maker","Fungus trader",
                        "Juggler","Maggot farmer","Mead brewer","Moth trapper","Mushroom forager",
                        "Pedlar","Pipe carver","Ragpicker","Tent maker","Tomb robber","Wizard's servant"],
    }
}

# ─── CLASS DATA ────────────────────────────────────────────────────────────────

CLASSES = {
    "bard": {
        "prime": ["Charisma", "Dexterity"],
        "hd": "1d6",
        "hd_after_10": "+1",
        "combat": "Semi-martial",
        "armour": "Light and Medium, no shields",
        "weapons": "Small and Medium",
        "saves_lvl1": {"Doom": 13, "Ray": 14, "Hold": 13, "Blast": 15, "Spell": 15},
        "attack_lvl1": 0,
        "skills": {
            "Decipher Doc.": 6,
            "Legerdemain": 5,
            "Listen": 6,
            "Monster Lore": 5,
        },
        "special": [
            "Counter Charm: While playing, allies within 30' are immune to magic based on music/song and gain +2 saves vs fairy magic. 1/Turn.",
            "Enchantment: 1/day per Level. By performing music, fascinate creatures in 30' radius. Cannot use in combat. Affects creatures whose total Levels ≤ 2× bard's Level. At Lvl 1: mortals only; Lvl 4+: animals/demi-fey; Lvl 7+: fairies/monstrosities. Charmed after performance (Save +2) for 1 Turn/Level.",
            "Bard Skills: Decipher Document, Legerdemain, Listen, Monster Lore.",
            "Customisable Skills: 2 expertise points at Lvl 1; +1 per Level gained (each point lowers a skill target by 1).",
        ],
        "starting_equipment": [
            ("Armour", ["None", "None", "Leather armour", "Leather armour", "Chainmail", "Chainmail"]),
            ("Weapon 1", ["Club", "3 daggers", "Longsword", "Sling + 20 stones", "Shortbow + 20 arrows", "Shortsword"]),
            ("Weapon 2", ["Club", "3 daggers", "Longsword", "Sling + 20 stones", "Shortbow + 20 arrows", "Shortsword"]),
            ("Class item", ["Musical instrument (stringed or wind)"]),
        ],
        "kindred_restrictions": [],
    },
    "cleric": {
        "prime": ["Wisdom"],
        "hd": "1d6",
        "hd_after_10": "+1",
        "combat": "Semi-martial",
        "armour": "Any, including shields (no arcane/fairy magic armour)",
        "weapons": "Any (no arcane/fairy magic weapons)",
        "saves_lvl1": {"Doom": 11, "Ray": 12, "Hold": 13, "Blast": 16, "Spell": 14},
        "attack_lvl1": 0,
        "skills": {
            "Listen": 6,
            "Search": 6,
            "Survival": 6,
        },
        "special": [
            "Holy Magic: From Level 2, pray for holy spells. Level 1: 0 spells.",
            "Turning the Undead: Present holy symbol to drive off undead. Roll 2d6 (4 or lower: unaffected; 5–6: 2d4 stunned 1 Round; 7–12: 2d4 flee 1 Turn; 13+: 2d4 destroyed).",
            "Detect Holy Magic Items: By touching an object and concentrating for 1 Turn, the cleric can detect if it is a holy magic item.",
            "Holy Order (from Lvl 2): Choose one — Order of St Faxis (+2 saves vs arcane magic; arcane casters –2 saves vs cleric spells; holy symbol: three crossed swords), Order of St Sedge (lay on hands: heal 1 HP/Level/day; holy symbol: hand with two fingers raised), Order of St Signis (+1 Attack vs undead; attacks harm undead as magic/silver; holy symbol: skull crowned with ivy).",
            "Alignment: Must be Lawful or Neutral.",
            "Kindred: Mortals only (no elves, grimalkins, woodgrues).",
        ],
        "starting_equipment": [
            ("Armour", ["Leather armour", "Leather armour + shield", "Chainmail", "Chainmail + shield", "Plate mail", "Plate mail + shield"]),
            ("Weapon 1", ["Dagger", "Longsword", "Mace", "Shortbow + 20 arrows", "Shortsword", "Warhammer"]),
            ("Weapon 2", ["Dagger", "Longsword", "Mace", "Shortbow + 20 arrows", "Shortsword", "Warhammer"]),
            ("Class item", ["Holy symbol"]),
        ],
        "kindred_restrictions": ["elf", "grimalkin", "woodgrue"],
        "holy_orders": [
            "Order of St Faxis – Seekers; root out dark magic practitioners. +2 saves vs arcane magic; arcane casters –2 saves vs your spells.",
            "Order of St Sedge – Defenders of the Church. Lay on hands: heal 1 HP/Level/day.",
            "Order of St Signis – Lichwards; hunt the undead. +1 Attack vs undead; your attacks harm undead as magic/silver weapons.",
        ],
    },
    "enchanter": {
        "prime": ["Charisma", "Intelligence"],
        "hd": "1d6",
        "hd_after_10": "+1",
        "combat": "Semi-martial",
        "armour": "Light and Medium, no shields",
        "weapons": "Small and Medium",
        "saves_lvl1": {"Doom": 11, "Ray": 12, "Hold": 13, "Blast": 16, "Spell": 14},
        "attack_lvl1": 0,
        "skills": {
            "Detect Magic": 5,
        },
        "special": [
            "Fairy Runes: Knows 1 random rune of lesser magnitude at Lvl 1.",
            "Glamours: Knows 1 glamour at Lvl 1 (plus kindred glamours if any).",
            "Detect Magic Skill: Touch object/place/creature to detect magic.",
            "Resistance to Divine Aid: 2-in-6 chance beneficial holy spells have no effect.",
            "Kindred: Typically fairies and demi-fey. Rare mortals with Fairy connection also qualify.",
        ],
        "starting_equipment": [
            ("Armour", ["None", "None", "Leather armour", "Leather armour", "Chainmail", "Chainmail"]),
            ("Weapon 1", ["Club", "Dagger", "Longsword", "Shortbow + 20 arrows", "Spear", "Staff"]),
            ("Weapon 2", ["Club", "Dagger", "Longsword", "Shortbow + 20 arrows", "Spear", "Staff"]),
        ],
        "kindred_restrictions": [],
    },
    "fighter": {
        "prime": ["Strength"],
        "hd": "1d8",
        "hd_after_10": "+2",
        "combat": "Martial",
        "armour": "Any, including shields",
        "weapons": "Any",
        "saves_lvl1": {"Doom": 12, "Ray": 13, "Hold": 14, "Blast": 15, "Spell": 16},
        "attack_lvl1": 1,
        "skills": {
            "Listen": 6,
            "Search": 6,
            "Survival": 6,
        },
        "special": [
            "Combat Talents: Gains 1 talent at Levels 2, 6, 10, 14 (roll or choose).",
            "  1. Battle Rage: +2 Attack/Damage while raging; –4 AC; cannot flee. Lasts until end of combat.",
            "  2. Cleave: On a killing blow in melee, immediately attack a second foe at –2 Attack.",
            "  3. Defender: While in melee, foe's attacks against other characters suffer –2.",
            "  4. Last Stand: If reduced to 0 HP, act for up to 5 more Rounds; Save vs Doom each time damaged.",
            "  5. Leader: Retainers/mercenaries within 60' gain +1 Morale/Loyalty; allies +2 saves vs fear.",
            "  6. Main Gauche: Off-hand Small melee weapon—each Round choose +1 AC or +1 Attack.",
            "  7. Slayer: +1 Attack/Damage vs a chosen enemy type (may be taken multiple times).",
            "  8. Weapon Specialist: +1 Attack/Damage with a chosen weapon type (may be taken multiple times).",
        ],
        "starting_equipment": [
            ("Armour", ["Leather armour", "Leather armour + shield", "Chainmail", "Chainmail + shield", "Plate mail", "Plate mail + shield"]),
            ("Weapon 1", ["Crossbow + 20 quarrels", "Dagger", "Longsword", "Mace", "Shortsword", "Spear"]),
            ("Weapon 2", ["Crossbow + 20 quarrels", "Dagger", "Longsword", "Mace", "Shortsword", "Spear"]),
        ],
        "kindred_restrictions": [],
    },
    "friar": {
        "prime": ["Intelligence", "Wisdom"],
        "hd": "1d4",
        "hd_after_10": "+1",
        "combat": "Non-martial",
        "armour": "None",
        "weapons": "Club, dagger, holy water, oil, sling, staff, torch",
        "saves_lvl1": {"Doom": 11, "Ray": 12, "Hold": 13, "Blast": 16, "Spell": 14},
        "attack_lvl1": 0,
        "skills": {
            "Survival (foraging)": 5,
        },
        "special": [
            "Armour of Faith: AC bonus from divine blessing — +2 AC at Lvl 1, increasing with level (max +5 at Lvl 11+). No armour worn.",
            "Holy Magic: May pray for holy spells. Level 1: 1 Rank 1 spell.",
            "Turning the Undead: Drive off undead with holy symbol (same mechanics as cleric).",
            "Herbalism: A single dose of medicinal herb is sufficient for 2 subjects.",
            "Culinary Implements: Can use a frying pan, sausage, or ham shank as melee weapon (1d4 dmg).",
            "Languages: Speaks Liturgic in addition to native languages.",
            "Poverty: Worldly possessions limited to what can be carried; excess wealth must be donated; must wear habit and tonsure.",
            "Alignment: Must be Lawful or Neutral.",
            "Kindred: Mortals only (no elves, grimalkins, woodgrues).",
        ],
        "starting_equipment": [
            ("Weapon", ["Club", "Dagger", "Sling + 20 stones", "Sling + 20 stones", "Staff", "Staff"]),
            ("Class item", ["Friar's habit, wooden holy symbol"]),
        ],
        "kindred_restrictions": ["elf", "grimalkin", "woodgrue"],
    },
    "hunter": {
        "prime": ["Constitution", "Dexterity"],
        "hd": "1d8",
        "hd_after_10": "+2",
        "combat": "Martial",
        "armour": "Light, shields",
        "weapons": "Any",
        "saves_lvl1": {"Doom": 12, "Ray": 13, "Hold": 14, "Blast": 15, "Spell": 16},
        "attack_lvl1": 1,
        "skills": {
            "Alertness": 6,
            "Stalking": 6,
            "Survival": 5,
            "Tracking": 5,
        },
        "special": [
            "Animal Companion: May bond with an animal. Companion follows hunter, fights to the death.",
            "Hunter Skills: Alertness, Stalking, Survival, Tracking.",
            "Missile Attack Bonus: +1 Attack with all missile weapons.",
            "Trophies: After slaying a creature (min 50 coins weight), take a trophy. Grants +1 Attack vs same creature type and +1 saves vs their special attacks.",
            "Wayfinding: If the party becomes lost, 3-in-6 chance the hunter can find the path again.",
        ],
        "starting_equipment": [
            ("Armour", ["Leather armour", "Leather armour", "Leather armour", "Leather armour + shield", "Leather armour + shield", "Leather armour + shield"]),
            ("Weapon 1", ["Dagger", "Longbow + 20 arrows", "Longbow + 20 arrows", "Longbow + 20 arrows", "Shortsword", "Sling + 20 stones"]),
            ("Weapon 2", ["Dagger", "Longbow + 20 arrows", "Longbow + 20 arrows", "Longbow + 20 arrows", "Shortsword", "Sling + 20 stones"]),
        ],
        "kindred_restrictions": [],
    },
    "knight": {
        "prime": ["Charisma", "Strength"],
        "hd": "1d8",
        "hd_after_10": "+2",
        "combat": "Martial",
        "armour": "Medium and Heavy, shields",
        "weapons": "Any melee weapons (no missile weapons — dishonourable)",
        "saves_lvl1": {"Doom": 12, "Ray": 13, "Hold": 12, "Blast": 15, "Spell": 15},
        "attack_lvl1": 1,
        "skills": {
            "Listen": 6,
            "Search": 6,
            "Survival": 6,
        },
        "special": [
            "Strength of Will: +2 bonus to Saving Throws against fairy magic and effects that cause fear.",
            "Mounted Combat: +1 Attack bonus when mounted.",
            "Monster Slayer (from Lvl 5): +2 to Attack and Damage Rolls against Large creatures.",
            "Horseman: Expert rider. From Lvl 5, urge steed to +10 Speed for 6 Turns, 1/day. Can assess steed's Hit Point range.",
            "Knighthood: Lvls 1–2 are squires. Fully knighted at Lvl 3 (coat of arms, hospitality rights from same-Alignment nobles).",
            "Liege: Serves one of the lower noble houses. Alignment must match liege.",
            "Code of Chivalry: Honour, Service, Glory in battle, Protecting the Weak, Hierarchy.",
            "Note: Rarely, non-humans and non-breggles are accepted as knights.",
        ],
        "liege_options": [
            "House Guillefer (Neutral) – Lord Edwin Guillefer",
            "House Harrowmoor (Lawful) – Lady Theatrice Harrowmoor",
            "House Hogwarsh (Neutral) – Baron Sagewine Hogwarsh",
            "House Malbleat (Chaotic) – Lord Gryphius Malbleat",
            "House Mulbreck (Lawful) – Lady Pulsephine Mulbreck",
            "House Murkin (Chaotic) – Lord Simeone Murkin",
            "House Nodlock (Neutral) – Lord Harald Nodlock",
            "House Ramius (Neutral) – Lord Shadgore Ramius",
        ],
        "starting_equipment": [
            ("Armour", ["Chainmail", "Chainmail + shield", "Chainmail + shield", "Plate mail", "Plate mail + shield", "Plate mail + shield"]),
            ("Weapon 1", ["Dagger", "Lance (spear for Small)", "Lance (spear for Small)", "Lance (spear for Small)", "Longsword", "Mace"]),
            ("Weapon 2", ["Dagger", "Lance (spear for Small)", "Lance (spear for Small)", "Lance (spear for Small)", "Longsword", "Mace"]),
        ],
        "kindred_restrictions": [],
    },
    "magician": {
        "prime": ["Intelligence"],
        "hd": "1d4",
        "hd_after_10": "+1",
        "combat": "Non-martial",
        "armour": "None",
        "weapons": "Dagger, holy water, oil, staff, torch",
        "saves_lvl1": {"Doom": 14, "Ray": 14, "Hold": 13, "Blast": 16, "Spell": 14},
        "attack_lvl1": 0,
        "skills": {
            "Detect Magic": 6,
        },
        "special": [
            "Arcane Magic: 1 Rank 1 spell per day at Level 1.",
            "Detect Magic Skill: Touch object/creature to detect magic.",
            "Magic Items: Can use arcane magic items (wands, scrolls).",
            "Starting Spell Book (roll 1d6):",
            "  1. Charms of the Fey Court: Fairy Servant, Ingratiate, Ventriloquism",
            "  2. Hogbrand's Incandescence: Firelight, Ignite/Extinguish, Shield of Force",
            "  3. Lord Oberon's Seals: Decipher, Glyph of Sealing, Vapours of Dream",
            "  4. Oliphan's Folio: Crystal Resonance, Ioun Shard, Shield of Force",
            "  5. Smythe's Illuminations: Decipher, Ignite/Extinguish, Ioun Shard",
            "  6. Treatise on Force and Dissolution: Crystal Resonance, Floating Disc, Vapours of Dream",
        ],
        "starting_equipment": [
            ("Weapon", ["Dagger", "Dagger", "Dagger", "Staff", "Staff", "Staff"]),
            ("Class item", ["Ritual robes, Spell Book (roll 1d6 above)"]),
        ],
        "kindred_restrictions": [],
    },
    "thief": {
        "prime": ["Dexterity"],
        "hd": "1d4",
        "hd_after_10": "+1",
        "combat": "Semi-martial",
        "armour": "Light, no shields",
        "weapons": "Small and Medium",
        "saves_lvl1": {"Doom": 13, "Ray": 14, "Hold": 13, "Blast": 15, "Spell": 15},
        "attack_lvl1": 0,
        "skills": {
            "Climb Wall": 4,
            "Decipher Doc.": 6,
            "Disarm Mech.": 6,
            "Legerdemain": 5,
            "Listen": 6,
            "Pick Lock": 5,
            "Search": 6,
            "Stealth": 6,
        },
        "special": [
            "Back-Stab: When attacking from behind with dagger vs unaware target: +4 Attack, 3d4 damage.",
            "Thief Skills: Climb Wall, Decipher Document, Disarm Mechanism, Legerdemain, Listen, Pick Lock, Search, Stealth.",
            "Thieves' Cant: Secret language of gestures and code words. Can hide messages in normal conversation.",
            "Customisable Skills: At Lvl 1 allocate 4 expertise points; +2 per Level gained (each lowers a skill target by 1).",
        ],
        "starting_equipment": [
            ("Armour", ["None", "None", "None", "Leather", "Leather", "Leather"]),
            ("Weapon 1", ["Club", "3 daggers", "Longsword", "Shortbow + 20 arrows", "Shortsword", "Sling + 20 stones"]),
            ("Weapon 2", ["Club", "3 daggers", "Longsword", "Shortbow + 20 arrows", "Shortsword", "Sling + 20 stones"]),
            ("Class item", ["Thieves' tools"]),
        ],
        "kindred_restrictions": [],
    },
}

# ─── ABILITY SCORE SYSTEM ─────────────────────────────────────────────────────

ABILITY_MODIFIER_TABLE = {
    3: -3, 4: -2, 5: -2, 6: -1, 7: -1, 8: -1,
    9: 0, 10: 0, 11: 0, 12: 0,
    13: 1, 14: 1, 15: 1, 16: 2, 17: 2, 18: 3
}

XP_MODIFIER_TABLE = {
    range(3, 6): -20,
    range(6, 9): -10,
    range(9, 13): 0,
    range(13, 16): 5,
    range(16, 19): 10,
}

def ability_modifier(score: int) -> int:
    return ABILITY_MODIFIER_TABLE.get(score, 0)

def fmt_mod(mod: int) -> str:
    return f"+{mod}" if mod >= 0 else str(mod)

def xp_modifier(score: int) -> int:
    for r, mod in XP_MODIFIER_TABLE.items():
        if score in r:
            return mod
    return 0

def roll_dice(expression: str) -> int:
    match = re.match(r'^(\d*)d(\d+)([+-]\d+)?$', expression.lower().strip())
    if not match:
        return int(expression)
    n = int(match.group(1)) if match.group(1) else 1
    sides = int(match.group(2))
    mod = int(match.group(3)) if match.group(3) else 0
    return sum(random.randint(1, sides) for _ in range(n)) + mod

def roll_3d6():
    return sum(random.randint(1, 6) for _ in range(3))

def roll_ability_scores() -> dict:
    return {
        "Strength": roll_3d6(),
        "Intelligence": roll_3d6(),
        "Wisdom": roll_3d6(),
        "Dexterity": roll_3d6(),
        "Constitution": roll_3d6(),
        "Charisma": roll_3d6(),
    }

# ─── NAME GENERATION ──────────────────────────────────────────────────────────

def generate_name(kindred_key: str) -> str:
    k = KINDREDS[kindred_key]
    gender = random.choice(["male", "female", "unisex"])

    if kindred_key == "elf":
        style = random.choice(["rustic", "courtly"])
        return random.choice(k["names"][style])

    if kindred_key == "grimalkin":
        first = random.choice(k["names_first"])
        surname = random.choice(k["surnames"])
        return f"{first} {surname}"

    # For others, pick by gender
    if gender == "male" and "names_male" in k:
        first = random.choice(k["names_male"])
    elif gender == "female" and "names_female" in k:
        first = random.choice(k["names_female"])
    elif "names_unisex" in k:
        first = random.choice(k["names_unisex"])
    else:
        first = random.choice(k.get("names_male", ["Unknown"]))

    surname = random.choice(k["surnames"]) if "surnames" in k else ""
    return f"{first} {surname}".strip()

# ─── EQUIPMENT ROLLING ────────────────────────────────────────────────────────

def roll_equipment(class_key: str, kindred_key: str) -> list:
    cls = CLASSES[class_key]
    equipment = []
    for item_name, options in cls["starting_equipment"]:
        if len(options) == 1:
            item = options[0]
            # Woodgrue always has a wind instrument (already listed as class item for bard, but ensure for woodgrue)
            equipment.append(f"{item_name}: {item}")
        elif len(options) == 6:
            roll = random.randint(1, 6) - 1
            result = options[roll]
            if result != "None":
                # Mossling armour renaming
                if kindred_key == "mossling":
                    result = result.replace("Chainmail", "Bark armour").replace("Plate mail", "Pinecone armour")
                equipment.append(f"{item_name}: {result}")
        else:
            equipment.append(f"{item_name}: {random.choice(options)}")
    # Woodgrue always starts with a wind instrument (even if not bard)
    if kindred_key == "woodgrue" and class_key != "bard":
        if not any("instrument" in e.lower() or "pipe" in e.lower() or "flute" in e.lower() for e in equipment):
            equipment.append("Class item: Wind instrument (can be used as melee weapon 1d4)")
    return equipment

# ─── HP CALCULATION ───────────────────────────────────────────────────────────

def roll_hp(class_key: str, con_modifier: int) -> tuple:
    hd = CLASSES[class_key]["hd"]
    max_die = int(hd[2:])
    raw = random.randint(1, max_die)
    total = max(1, raw + con_modifier)
    return raw, total

# ─── APPEARANCE ROLLING ───────────────────────────────────────────────────────

def roll_appearance(kindred_key: str) -> dict:
    tables = APPEARANCE[kindred_key]
    result = {}
    for category, entries in tables.items():
        result[category] = random.choice(entries)
    return result

# ─── CHARACTER GENERATION ─────────────────────────────────────────────────────

def generate_character(kindred_key: str = None, class_key: str = None,
                        allowed_kindreds: list = None, allowed_classes: list = None,
                        excluded_classes: list = None) -> dict:
    """Generate a complete Dolmenwood character with optional constraints."""

    all_kindreds = list(KINDREDS.keys())
    all_classes = list(CLASSES.keys())

    # ── Select kindred ──
    if kindred_key:
        if kindred_key not in KINDREDS:
            print(f"ERROR: Unknown kindred '{kindred_key}'. Valid: {', '.join(all_kindreds)}")
            sys.exit(1)
    else:
        pool = allowed_kindreds if allowed_kindreds else all_kindreds
        pool = [k for k in pool if k in KINDREDS]
        if not pool:
            print(f"ERROR: No valid kindreds in pool: {allowed_kindreds}")
            sys.exit(1)
        kindred_key = random.choice(pool)

    kindred = KINDREDS[kindred_key]

    # ── Select class ──
    if class_key:
        if class_key not in CLASSES:
            print(f"ERROR: Unknown class '{class_key}'. Valid: {', '.join(all_classes)}")
            sys.exit(1)
        if class_key in CLASSES[class_key].get("kindred_restrictions", []):
            print(f"WARNING: {kindred_key} cannot be {class_key}. Proceeding anyway (GM override).")
    else:
        pool = allowed_classes if allowed_classes else kindred["allowed_classes"]
        if excluded_classes:
            pool = [c for c in pool if c not in excluded_classes]
        pool = [c for c in pool if kindred_key not in CLASSES[c].get("kindred_restrictions", [])]
        if not pool:
            print(f"ERROR: No valid classes for {kindred_key} with given constraints.")
            sys.exit(1)
        weights = [3 if c in kindred.get("common_classes", []) else 1 for c in pool]
        class_key = random.choices(pool, weights=weights)[0]

    cls = CLASSES[class_key]

    # ── Roll ability scores ──
    abilities = roll_ability_scores()

    # ── HP ──
    con_mod = ability_modifier(abilities["Constitution"])
    hp_raw, hp_total = roll_hp(class_key, con_mod)

    # ── XP modifier (lowest prime ability score) ──
    prime_scores = [abilities[a] for a in cls["prime"]]
    lowest_prime = min(prime_scores)
    xp_mod = xp_modifier(lowest_prime)
    if kindred_key == "human":
        xp_mod += 10  # Human Spirited trait

    # ── Equipment ──
    equipment = roll_equipment(class_key, kindred_key)

    # ── Alignment ──
    if class_key in ["cleric", "friar"]:
        alignment = random.choice(["Lawful", "Neutral"])
    elif kindred_key in ["elf", "grimalkin", "woodgrue"]:
        alignment = random.choices(["Lawful", "Neutral", "Chaotic"], weights=[2, 4, 3])[0]
    else:
        alignment = random.choices(["Lawful", "Neutral", "Chaotic"], weights=[3, 5, 2])[0]

    # ── Name ──
    name = generate_name(kindred_key)

    # ── Background ──
    background = random.choice(kindred["backgrounds"])

    # ── Appearance ──
    appearance = roll_appearance(kindred_key)

    # ── Trinket ──
    trinket = random.choice(TRINKETS[kindred_key])

    # ── Special class data ──
    extra = {}
    if class_key == "knight":
        extra["liege"] = random.choice(cls["liege_options"])
    if class_key == "magician":
        spellbook_roll = random.randint(1, 6)
        spellbooks = [
            "Charms of the Fey Court: Fairy Servant, Ingratiate, Ventriloquism",
            "Hogbrand's Incandescence: Firelight, Ignite / Extinguish, Shield of Force",
            "Lord Oberon's Seals: Decipher, Glyph of Sealing, Vapours of Dream",
            "Oliphan's Folio: Crystal Resonance, Ioun Shard, Shield of Force",
            "Smythe's Illuminations: Decipher, Ignite / Extinguish, Ioun Shard",
            "Treatise on Force and Dissolution: Crystal Resonance, Floating Disc, Vapours of Dream",
        ]
        extra["spellbook"] = spellbooks[spellbook_roll - 1]
        extra["spellbook_roll"] = spellbook_roll
    if class_key == "cleric":
        extra["holy_order"] = random.choice(cls["holy_orders"])
    if kindred_key == "mossling":
        knack = random.choice(MOSSLING_KNACKS)
        extra["knack_name"] = knack[0]
        extra["knack_desc"] = knack[1]
        extra["symbiotic_flesh"] = random.choice(MOSSLING_SYMBIOTIC_FLESH)

    # ── Starting gold ──
    gold = roll_dice("3d6") * 10

    return {
        "name": name,
        "kindred": kindred_key,
        "class": class_key,
        "level": 1,
        "alignment": alignment,
        "background": background,
        "abilities": abilities,
        "hp_raw": hp_raw,
        "hp": hp_total,
        "xp_modifier": xp_mod,
        "saves": cls["saves_lvl1"],
        "attack": cls["attack_lvl1"],
        "equipment": equipment,
        "gold": gold,
        "appearance": appearance,
        "trinket": trinket,
        "kindred_data": kindred,
        "class_data": cls,
        "extra": extra,
    }

# ─── FORMATTING ───────────────────────────────────────────────────────────────

def format_character_sheet(char: dict, include_gm_notes: bool = True) -> str:
    k = char["kindred_data"]
    cls = char["class_data"]
    ab = char["abilities"]
    saves = char["saves"]
    name = char["name"]
    kindred = char["kindred"].capitalize()
    class_name = char["class"].capitalize()
    date = datetime.now().strftime("%Y-%m-%d")

    # AC calculation
    if char["kindred"] == "breggle":
        base_ac_asc = 11  # unarmoured + breggle fur (+1)
        base_ac_desc = 8
    else:
        base_ac_asc = 10
        base_ac_desc = 9

    armour_ac = 0
    for item in char["equipment"]:
        item_lower = item.lower()
        if "plate mail" in item_lower or "pinecone armour" in item_lower:
            armour_ac = 6
        elif "chainmail" in item_lower or "bark armour" in item_lower:
            armour_ac = 4
        elif "leather" in item_lower:
            armour_ac = 2

    # Friar Armour of Faith (+2 at level 1)
    if char["class"] == "friar":
        armour_ac = 2  # Armour of Faith +2 at Lvl 1

    final_ac_asc = base_ac_asc + armour_ac
    final_ac_desc = 19 - final_ac_asc

    prime_str = " and ".join(cls["prime"])
    prime_scores = [ab[a] for a in cls["prime"]]

    # Skills
    skills_section = ""
    if cls.get("skills"):
        skills_section = "\n### Skills\n\n"
        skills_section += "| Skill | Target | Roll |\n|-------|--------|------|\n"
        for skill, target in cls["skills"].items():
            skills_section += f"| {skill} | {target} | d6, equal or beat target |\n"

    # Class special traits
    class_traits = "\n".join(f"- {t}" for t in cls["special"])

    # Kindred special traits
    kindred_traits = "\n".join(f"- {t}" for t in k["special_traits"])

    # Equipment
    equip_list = "\n".join(f"- {e}" for e in char["equipment"])
    equip_list += f"\n- Gold: {char['gold']} gp"

    # Extra class data
    extra_section = ""
    if char["extra"].get("spellbook"):
        extra_section = f"\n### Starting Spell Book (Rolled {char['extra']['spellbook_roll']})\n**{char['extra']['spellbook']}**\n"
    if char["extra"].get("liege"):
        extra_section += f"\n### Liege\n**{char['extra']['liege']}**\n"
    if char["extra"].get("holy_order"):
        extra_section += f"\n### Holy Order (from Level 2)\n**{char['extra']['holy_order']}**\n"
    if char["extra"].get("knack_name"):
        extra_section += f"\n### Mossling Knack: {char['extra']['knack_name']}\n{char['extra']['knack_desc']}\n"
    if char["extra"].get("symbiotic_flesh"):
        extra_section += f"\n### Symbiotic Flesh\n{char['extra']['symbiotic_flesh']}\n"

    # Languages
    languages = ", ".join(k["languages"])
    if class_name.lower() in ["cleric", "friar"]:
        languages += ", Liturgic"
    if class_name.lower() == "thief":
        languages += ", Thieves' Cant"

    # XP mod display
    xp_display = f"+{char['xp_modifier']}%" if char["xp_modifier"] >= 0 else f"{char['xp_modifier']}%"

    # Appearance section
    app = char["appearance"]
    appearance_lines = []
    for category, value in app.items():
        appearance_lines.append(f"- **{category}:** {value}")
    appearance_section = "\n".join(appearance_lines)

    sheet = f"""---
tags: [character, pc, {char['kindred']}, {char['class']}, level-1]
name: {name}
kindred: {kindred}
class: {class_name}
level: 1
alignment: {char['alignment']}
status: alive
created: {date}
---

# {name} — {kindred} {class_name}
**Kindred:** {kindred} ({k['type'].capitalize()}, {k['size']})
**Class:** {class_name} · Level 1
**Alignment:** {char['alignment']}
**Background:** {char['background']}
**Languages:** {languages}

---

## Ability Scores

| STR | INT | WIS | DEX | CON | CHA |
|-----|-----|-----|-----|-----|-----|
| {ab['Strength']} ({fmt_mod(ability_modifier(ab['Strength']))}) | {ab['Intelligence']} ({fmt_mod(ability_modifier(ab['Intelligence']))}) | {ab['Wisdom']} ({fmt_mod(ability_modifier(ab['Wisdom']))}) | {ab['Dexterity']} ({fmt_mod(ability_modifier(ab['Dexterity']))}) | {ab['Constitution']} ({fmt_mod(ability_modifier(ab['Constitution']))}) | {ab['Charisma']} ({fmt_mod(ability_modifier(ab['Charisma']))}) |

**Prime Ability:** {prime_str} ({", ".join(str(s) for s in prime_scores)}) → **XP Modifier: {xp_display}**

---

## Combat

| Stat | Value |
|------|-------|
| **HP** | {char['hp']} / {char['hp']} |
| **AC (Ascending)** | {final_ac_asc} |
| **AC (Descending)** | {final_ac_desc} |
| **Attack Bonus** | {fmt_mod(char['attack'])} |
| **Speed** | 40' (120' per Turn) |

**Saving Throws**

| Doom | Ray | Hold | Blast | Spell |
|------|-----|------|-------|-------|
| {saves['Doom']} | {saves['Ray']} | {saves['Hold']} | {saves['Blast']} | {saves['Spell']} |

> Roll d20 equal or above target to succeed. Wisdom modifier applies as Magic Resistance bonus to Spell saves.

---

## Armour & Weapons

| Item | Details |
|------|---------|
{"".join(f"| {e.split(': ')[0]} | {': '.join(e.split(': ')[1:])} |" + chr(10) for e in char['equipment'])}
**Gold:** {char['gold']} gp

---

## Class Abilities

**Combat Aptitude:** {cls['combat']}
**Armour:** {cls['armour']}
**Weapons:** {cls['weapons']}

{class_traits}
{extra_section}
{skills_section}
---

## Kindred Traits ({kindred})

{kindred_traits}

---

## Appearance & Personality

{appearance_section}

---

## Trinket

> {char['trinket']}

---

## Personality Notes

**Wants:** {app.get('Desires', '*(fill in)*')}

**Believes:** {app.get('Beliefs', '*(fill in)*')}

**Fears:** *(fill in)*
"""

    if include_gm_notes:
        sheet += f"""
---

## GM Notes *(remove for player handout)*

> **Secret:**
>
> **Personal hook:**
>
> **Loyalty – what would they betray the party for:**
"""

    return sheet

# ─── SAVE TO VAULT ────────────────────────────────────────────────────────────

def save_character(char: dict, campaign: str):
    campaign_dir = Path(__file__).parent.parent / "campaign" / campaign
    players_dir = campaign_dir / "players"
    players_dir.mkdir(parents=True, exist_ok=True)

    # Include class and kindred in filename
    slug = char["name"].lower().replace(" ", "_").replace("'", "").replace("-", "_")[:30]
    kindred_slug = char["kindred"]
    class_slug = char["class"]
    filename_base = f"{slug}_{kindred_slug}_{class_slug}"

    # GM version (full)
    gm_path = players_dir / f"{filename_base}_gm.md"
    gm_path.write_text(format_character_sheet(char, include_gm_notes=True), encoding="utf-8")

    # Player handout (no GM notes)
    player_path = players_dir / f"{filename_base}_player.md"
    player_path.write_text(format_character_sheet(char, include_gm_notes=False), encoding="utf-8")

    return gm_path, player_path

# ─── QUICK DISPLAY ────────────────────────────────────────────────────────────

def format_quick_summary(char: dict) -> str:
    ab = char["abilities"]
    cls = char["class_data"]
    saves = char["saves"]
    prime_str = "/".join(cls["prime"])
    prime_scores = [ab[a] for a in cls["prime"]]
    xp_display = f"+{char['xp_modifier']}%" if char["xp_modifier"] >= 0 else f"{char['xp_modifier']}%"

    lines = [
        f"  {char['name']} | {char['kindred'].capitalize()} {char['class'].capitalize()} | {char['alignment']}",
        f"  STR {ab['Strength']} INT {ab['Intelligence']} WIS {ab['Wisdom']} DEX {ab['Dexterity']} CON {ab['Constitution']} CHA {ab['Charisma']}",
        f"  HP: {char['hp']}  Prime ({prime_str}): {', '.join(str(s) for s in prime_scores)}  XP mod: {xp_display}",
        f"  Background: {char['background']}",
        f"  Trinket: {char['trinket'][:70]}{'...' if len(char['trinket']) > 70 else ''}",
    ]
    if char["extra"].get("spellbook"):
        lines.append(f"  Spellbook: {char['extra']['spellbook']}")
    if char["extra"].get("liege"):
        lines.append(f"  Liege: {char['extra']['liege']}")
    if char["extra"].get("knack_name"):
        lines.append(f"  Knack: {char['extra']['knack_name']}")
    return "\n".join(lines)

# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Dolmenwood Character Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dolmenwood_chargen.py
  python dolmenwood_chargen.py --kindred human breggle
  python dolmenwood_chargen.py --kindred human breggle --exclude-class magician enchanter
  python dolmenwood_chargen.py --kindred elf --class enchanter
  python dolmenwood_chargen.py --count 3 --kindred human breggle --exclude-class magician
  python dolmenwood_chargen.py --kindred human --save --campaign dolmenwood

Valid kindreds:  human, breggle, elf, grimalkin, mossling, woodgrue
Valid classes:   bard, cleric, enchanter, fighter, friar, hunter, knight, magician, thief
        """
    )
    parser.add_argument("--kindred", nargs="+",
                        help="Allow only these kindreds (e.g. --kindred human breggle)")
    parser.add_argument("--class", dest="classname",
                        help="Fix the class (e.g. --class fighter)")
    parser.add_argument("--exclude-class", nargs="+", dest="exclude_class",
                        help="Exclude these classes (e.g. --exclude-class magician enchanter)")
    parser.add_argument("--count", "-n", type=int, default=1,
                        help="Generate N characters (default: 1)")
    parser.add_argument("--save", "-s", action="store_true",
                        help="Save to campaign vault (Obsidian)")
    parser.add_argument("--campaign", default="dolmenwood",
                        help="Campaign name for vault save (default: dolmenwood)")
    parser.add_argument("--quick", "-q", action="store_true",
                        help="Show quick summary only (good for choosing from multiple)")
    parser.add_argument("--list", action="store_true",
                        help="List all valid kindreds and classes")

    args = parser.parse_args()

    if args.list:
        print("\nKindreds:")
        for k, v in KINDREDS.items():
            restricted = [c for c in CLASSES if k in CLASSES[c].get("kindred_restrictions", [])]
            print(f"  {k:12} ({v['type']}, {v['size']}) — cannot be: {', '.join(restricted) if restricted else 'none'}")
        print("\nClasses:")
        for c, v in CLASSES.items():
            prime = ", ".join(v["prime"])
            restricted_for = [k for k in KINDREDS if k in v.get("kindred_restrictions", [])]
            note = f" — not available to: {', '.join(restricted_for)}" if restricted_for else ""
            print(f"  {c:12} Prime: {prime}{note}")
        sys.exit(0)

    characters = []
    for i in range(args.count):
        char = generate_character(
            kindred_key=None if not args.kindred or len(args.kindred) != 1 else args.kindred[0],
            class_key=args.classname,
            allowed_kindreds=args.kindred if args.kindred and len(args.kindred) > 1 else (args.kindred if args.kindred else None),
            allowed_classes=None,
            excluded_classes=args.exclude_class,
        )
        characters.append(char)

    if args.count > 1 and args.quick:
        print(f"\n{'='*60}")
        print(f"  Generated {args.count} characters")
        print(f"  Filters: kindred={args.kindred}, exclude={args.exclude_class}")
        print(f"{'='*60}")
        for i, char in enumerate(characters, 1):
            print(f"\n  ── Option {i} ──")
            print(format_quick_summary(char))
        print()

    elif args.count > 1:
        print(f"\nGenerating {args.count} characters...\n")
        for i, char in enumerate(characters, 1):
            print(f"{'='*60}")
            print(f"  OPTION {i}")
            print(f"{'='*60}")
            print(format_quick_summary(char))
            print()

    else:
        char = characters[0]
        if args.quick:
            print(format_quick_summary(char))
        else:
            print(format_character_sheet(char, include_gm_notes=True))

    if args.save:
        for char in characters:
            gm_path, player_path = save_character(char, args.campaign)
            print(f"\nSaved (GM):     {gm_path}")
            print(f"Saved (player): {player_path}")


if __name__ == "__main__":
    main()
