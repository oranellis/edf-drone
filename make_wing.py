import math

span=1.3
root_chord=0.2
min_chord_ratio=0.2
section_count=16
x_panel_count=50
y_panel_size=(span/2)*(1/24)
twist=0
file_name="Main_Wing.xml"
foil_name="EPPLER 67 AIRFOIL"

# section_count=14
# x_panel_count=40
# y_panel_count=2
# span=0.4
# root_chord=0.12
# twist=0
# file_name="Elevator.xml"
# foil_name="NACA 0012 AIRFOILS"

# Finds the spanwise location on an elliptical wing for a normalised chord length
#
# @param c Normalised chord length, between 0 and 1
#
# @returns y Normalised spanwise location, between 0 (wing root) and 1 (wing tip)
def SpanLocationFromChord(c):
    y = math.sqrt(1-math.pow(c,2))
    return y

# Finds the offset from the wing leading edge for the aerofoil to produce an elliptical wing
#
# @param chord The chord length
def GetXOffset(chord):
    offset=(root_chord-chord) / 2
    return offset

# Returns the actual spanwise location from the non-dimentional y
#
# @param y Between the root of the wing 0 and the tip of the wing 1
def GetDimentionalisedYLocation(y):
    y_actual=y*span/2
    return y_actual

# Returns the twist at a location y on the wing
#
# @param y Between the root of the wing 0 and the tip of the wing 1
def GetTwist(_):
    return twist

# Returns the twist at a location y on the wing
#
# @param y Between the root of the wing 0 and the tip of the wing 1
def GetDihedral(_):
    return 0

# Computes the normalised span locations along an elliptical wing with equal chord length spacing
# down from c_root to c_root*min_root_chord and adds them to sections
sections = []
chords = []
for i in range(section_count, -1, -1):
    if min_chord_ratio != 0 or i != 0:
        nd_chord=(i/section_count)*(1-min_chord_ratio) + min_chord_ratio
        chord=nd_chord*root_chord
        numerator = SpanLocationFromChord(nd_chord)
        denominator = SpanLocationFromChord(min_chord_ratio)
        sections.append(
            numerator/denominator
            )
        chords.append(chord)

wing_string = "\t\t<Sections>\n"
for index, y in enumerate(sections):
    y_panel_count = 1
    if index < (len(sections)-1):
        y_panel_count = math.floor((sections[index+1]-sections[index]) / y_panel_size)

    wing_string += \
    "\t\t\t<Section>\n" + \
    f"\t\t\t\t<y_position> {GetDimentionalisedYLocation(y):.3f}</y_position>\n" + \
    f"\t\t\t\t<chord> {chords[index]:.3f}</chord>\n" + \
    f"\t\t\t\t<xOffset> {GetXOffset(chords[index]):.3f}</xOffset>\n" + \
    f"\t\t\t\t<Dihedral> {GetDihedral(y):.3f}</Dihedral>\n" + \
    f"\t\t\t\t<Twist> {GetTwist(y):.3f}</Twist>\n" + \
    f"\t\t\t\t<x_number_of_panels> {x_panel_count:d}</x_number_of_panels>\n" + \
    "\t\t\t\t<x_panel_distribution>COSINE</x_panel_distribution>\n" + \
    f"\t\t\t\t<y_number_of_panels> {y_panel_count:d}</y_number_of_panels>\n" + \
    "\t\t\t\t<y_panel_distribution>UNIFORM</y_panel_distribution>\n" + \
    "\t\t\t\t<Left_Side_FoilName>" + foil_name + "</Left_Side_FoilName>\n" + \
    "\t\t\t\t<Right_Side_FoilName>" + foil_name + "</Right_Side_FoilName>\n" + \
    "\t\t\t</Section>\n"
wing_string += "\t\t</Sections>\n"

with open(file_name, "r") as f:
    lines = f.readlines()
flipbit = False
with open(file_name, "w") as f:
    for line in lines:
        if not flipbit:
            if "<Sections>" in line:
                flipbit = True
            else:
                f.write(line)
        elif "</Sections>" in line:
            flipbit = False
            f.write(wing_string)
