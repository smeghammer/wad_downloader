from dataclasses import dataclass
from mongoengine import connect
from mongoengine import Document
from mongoengine import StringField
from mongoengine import EnumField
from mongoengine import IntField
from mongoengine import FloatField
from mongoengine import EmbeddedDocument
from mongoengine import EmbeddedDocumentField

from enum import Enum

# https://docs.mongoengine.org/guide/connecting.html

# connected = connect(host="mongodb://192.168.1.115:27017/DoomWadDownloader")
connect("DoomWadDownloader", host="192.168.1.115", port=27017)

# https://docs.mongoengine.org/apireference.html#mongoengine.fields.EnumField
class DownloadState(Enum):
    NOTFETCHED = "NOTFETCHED"
    FETCHED = "FETCHED"
    LOCKED = "LOCKED"
    ERROR = "ERROR"
    FAILED = "FAILED"

# special cases for R667:
'''
    "metadata" : {
        "dir" : "Armory/Doom/",
        "filename" : "40mmGrenadeLauncher.zip",
        "state" : "NOTFETCHED",
        "info" : {
            "title" : "Info",
            "entries" : {
                "Name" : "40mm Grenade Launcher",
                "Class" : "5",
                "Type" : "Projectile",
                "Palette" : "Doom",
                "Summon" : "40mmGrenadeLauncher",
                "Ammotype" : "40mmGrenades",
                "AltFire" : "Yes",
                "PoweredMode" : "No",
                "Brightmaps" : "No",
                "AddedStates" : "No",
                "ACS" : "No"
            }
        },
        "credits" : {
            "title" : "Credits",
            "entries" : {
                "Submitted" : "ProjectAngel",
                "Updated" : "Ozymandias81, BadMojo",
                "Decorate" : "ProjectAngel",
                "GLDefs" : "BadMojo",
                "Sounds" : "Raven Software, id Software",
                "Sprites" : "Marty Kirra, 3d Realms, id Software, Midway Entertainment",
                "SpriteEdit" : "Marty Kirra",
                "IdeaBase" : "Shadow Warrior Grenade Launcher, Militek MGL from 007: NightFire"
            }
        },
        "topic" : "Doom",
        "section" : "Armory"
    }
'''
# R667 INFO
# Note that the entries for Info and Credits are not a controlled list,
# so there are some very odd fieldnames, as well as typos...
class R667InfoEntries(EmbeddedDocument):
    acs = StringField(max_length=40)
    acsno = StringField(max_length=40)
    activatable = StringField(max_length=40)
    actormodification = StringField(max_length=40)
    actormodificationno = StringField(max_length=40)
    actormodifications = StringField(max_length=40)
    addedstates = StringField(max_length=40)
    akimbo = StringField(max_length=40)
    altfire = StringField(max_length=40)
    ambientsound = StringField(max_length=200)
    ambientsounds = StringField(max_length=200)
    ammo = StringField(max_length=40)
    ammotype = StringField(max_length=40)
    anims_switches = StringField(max_length=200)
    base = StringField(max_length=200)
    brightmaps = StringField(max_length=40)
    brighmaps = StringField(max_length=40)
    class5 = StringField(max_length=40)
    connection = StringField(max_length=200)
    connections = StringField(max_length=200)
    count = StringField(max_length=200)
    de_activatable = StringField(max_length=200)
    decaldef = StringField(max_length=40)
    delay = StringField(max_length=40)
    description = StringField(max_length=200)
    destroyable = StringField(max_length=200)
    destructible = StringField(max_length=200)
    difficulty = StringField(max_length=200)
    distance = StringField(max_length=200)
    documentation = StringField(max_length=200)
    duration = StringField(max_length=200)
    edifficulty = StringField(max_length=200)
    format = StringField(max_length=200)
    gldefs = StringField(max_length=40)
    heal = StringField(max_length=40)
    individualglyphs = StringField(max_length=200)
    individualglyphs_charactermapsincluded = StringField(max_length=200)
    looping = StringField(max_length=40)
    lowercases = StringField(max_length=200)
    melee = StringField(max_length=200)
    name = StringField(max_length=40)
    note = StringField(max_length=200)
    palette = StringField(max_length=40)
    paletted = StringField(max_length=200)
    pallette = StringField(max_length=40)
    poweredmode = StringField(max_length=40)
    poweredupmode = StringField(max_length=40)
    random = StringField(max_length=40)
    reload_zoom = StringField(max_length=40)
    reload = StringField(max_length=40)
    replaces = StringField(max_length=200)
    size = StringField(max_length=200)
    source = StringField(max_length=200)
    spawnceiling = StringField(max_length=200)
    spawnoffsets = StringField(max_length=200)
    specialeffects = StringField(max_length=200)
    standardgfxincluded = StringField(max_length=200)
    summon = StringField(max_length=40)
    summong = StringField(max_length=40)
    surround = StringField(max_length=40)
    thingclass = StringField(max_length=40)
    type = StringField(max_length=40)
    typebrightmapsfordoomheretichexenandstrife = StringField(max_length=200) # <- crappy HTML? looks like a name/value pair... https://www.realm667.com/en/repository-18489/sfx-shoppe-mainmenu-139-58855/other-66854/1077-iwad-brightmaps#info
    usetype = StringField(max_length=200)
    variants = StringField(max_length=200)
    varients = StringField(max_length=200)
    zscript = StringField(max_length=40)

class R667Info(EmbeddedDocument):
    entries = EmbeddedDocumentField(R667InfoEntries)
    title = StringField(max_length=40)

# R667 CREDITS
class R667CreditsEntries(EmbeddedDocument):
    acs = StringField(max_length=40)
    additionalcredits = StringField(max_length=200)
    author = StringField(max_length=200)
    baseidea = StringField(max_length=200)
    brightmaps = StringField(max_length=40)
    brightmapsedit = StringField(max_length=40)
    code = StringField(max_length=40)
    conversion = StringField(max_length=200)
    decaldef = StringField(max_length=40)
    decorate = StringField(max_length=40)
    decoratecreatedby = StringField(max_length=40)
    edits = StringField(max_length=200)
    gldefs = StringField(max_length=40)
    glddefs = StringField(max_length=40)
    ideabase = StringField(max_length=200)
    idea = StringField(max_length=200)
    ideaby = StringField(max_length=200)
    models = StringField(max_length=200)
    nameassuggestedby = StringField(max_length=200)
    namesuggestedby = StringField(max_length=200)
    note = StringField(max_length=200)
    originalfont = StringField(max_length=200)
    palette = StringField(max_length=40)
    rippedby = StringField(max_length=200)
    seeindividualwadsforcredits = StringField(max_length=200)
    sounds = StringField(max_length=40)
    sfx = StringField(max_length=200)
    sndinfo = StringField(max_length=200)
    soundedit = StringField(max_length=200)
    soundedits = StringField(max_length=200)
    source = StringField(max_length=200)
    sprideedit = StringField(max_length=40)
    specialthanks = StringField(max_length=200)
    sprite = StringField(max_length=200)
    sprites = StringField(max_length=200)
    spriteedit = StringField(max_length=40)
    spriteedits = StringField(max_length=40)
    spritesedit = StringField(max_length=40)
    spriteedit = StringField(max_length=40)
    spiteedit = StringField(max_length=40)
    submitted = StringField(max_length=40)
    submittedbravo = StringField(max_length=40)
    submittedby = StringField(max_length=40)
    submittedceeb = StringField(max_length=200)
    submittedthedoomedarchvile = StringField(max_length=200)
    textures = StringField(max_length=200)
    textures_materials = StringField(max_length=200)
    updated = StringField(max_length=40)
    zscript = StringField(max_length=40)

class R667Credits(EmbeddedDocument):
    title = StringField(max_length=40)
    entries = EmbeddedDocumentField(R667CreditsEntries)

# first cut
class MetaData(EmbeddedDocument):
    # doomwadstation, tspg, wad-archive, camoy,doomshack
    # _id = StringField(max_length=40)
    href = StringField(max_length=200)
    filename = StringField(max_length=200)
    dir = StringField(max_length=200)

    #doomworld
    id = IntField()
    title = StringField(max_length=40)
    size = IntField()
    age = IntField()
    date = StringField(max_length=10)
    author = StringField(max_length=40)
    email = StringField(max_length=100)
    description = StringField(max_length=4000)
    rating = FloatField(max_value=5)
    votes = IntField()
    url = StringField(max_length=200)
    idgamesurl = StringField(max_length=200)

    #R667
    state = StringField(max_length=20)
    imagefile = StringField(max_length=100)
    # this gets silly...
    info = EmbeddedDocumentField(document_type=R667Info)
    credits = EmbeddedDocumentField(document_type=R667Credits)
    section = StringField(max_length=20)
    topic = StringField(max_length=20)



# see https://stackoverflow.com/questions/25466966/mongoengine-link-to-existing-collection
class WADDownload(Document):
    meta = {'collection':'downloads'}   # specify the collection to use
    _id = StringField(max_length=200, required=True, primary_key=True)
    url = StringField(max_length=200, required=True)
    state = EnumField(DownloadState,default=DownloadState.NOTFETCHED)
    source = StringField(max_length=20, required=True)
    metadata = EmbeddedDocumentField(document_type=MetaData)

    def set_state(self, new_state:DownloadState):
        self.state = new_state
