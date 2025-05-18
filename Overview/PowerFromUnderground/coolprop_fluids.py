from CoolProp.CoolProp import PropsSI
coolprop_fluids = [
    ("1-Butene", "1-Butene"),
    ("Acetone", "Acetone"),
    ("Air", "Air"),
    ("Ammonia", "Ammonia"),
    ("Argon", "Argon"),
    ("Benzene", "Benzene"),
    ("CarbonDioxide", "Carbon Dioxide (CO₂)"),
    ("CarbonMonoxide", "Carbon Monoxide (CO)"),
    ("CarbonylSulfide", "Carbonyl Sulfide"),
    ("CycloHexane", "Cyclohexane"),
    ("Cyclopentane", "Cyclopentane"),
    ("CycloPropane", "Cyclopropane"),
    ("D4", "D4"),
    ("D5", "D5"),
    ("D6", "D6"),
    ("Deuterium", "Deuterium"),
    ("Dichloroethane", "Dichloroethane"),
    ("DiethylEther", "Diethyl Ether"),
    ("DimethylCarbonate", "Dimethyl Carbonate"),
    ("DimethylEther", "Dimethyl Ether"),
    ("Ethane", "Ethane"),
    ("Ethanol", "Ethanol"),
    ("EthylBenzene", "Ethylbenzene"),
    ("Ethylene", "Ethylene"),
    ("EthyleneOxide", "Ethylene Oxide"),
    ("Fluorine", "Fluorine"),
    ("HFE143m", "HFE-143m"),
    ("HeavyWater", "Heavy Water (D₂O)"),
    ("Helium", "Helium"),
    ("Hydrogen", "Hydrogen"),
    ("HydrogenChloride", "Hydrogen Chloride"),
    ("HydrogenSulfide", "Hydrogen Sulfide"),
    ("IsoButane", "Isobutane (R-600a)"),
    ("IsoButene", "Isobutene"),
    ("Isohexane", "Isohexane"),
    ("Isopentane", "Isopentane"),
    ("Krypton", "Krypton"),
    ("MD2M", "MD2M"),
    ("MD3M", "MD3M"),
    ("MD4M", "MD4M"),
    ("MDM", "MDM"),
    ("MM", "MM"),
    ("Methane", "Methane"),
    ("Methanol", "Methanol"),
    ("MethylLinoleate", "Methyl Linoleate"),
    ("MethylLinolenate", "Methyl Linolenate"),
    ("MethylOleate", "Methyl Oleate"),
    ("MethylPalmitate", "Methyl Palmitate"),
    ("MethylStearate", "Methyl Stearate"),
    ("Neon", "Neon"),
    ("Neopentane", "Neopentane"),
    ("Nitrogen", "Nitrogen"),
    ("NitrousOxide", "Nitrous Oxide (N₂O)"),
    ("Novec649", "Novec 649"),
    ("Oxygen", "Oxygen"),
    ("Propylene", "Propylene"),
    ("Propyne", "Propyne"),
    ("R11", "R-11"),
    ("R113", "R-113"),
    ("R114", "R-114"),
    ("R115", "R-115"),
    ("R116", "R-116"),
    ("R12", "R-12"),
    ("R123", "R-123"),
    ("R1233zd(E)", "R-1233zd(E)"),
    ("R1234yf", "R-1234yf"),
    ("R1234ze(E)", "R-1234ze(E)"),
    ("R1234ze(Z)", "R-1234ze(Z)"),
    ("R124", "R-124"),
    ("R1243zf", "R-1243zf"),
    ("R125", "R-125"),
    ("R13", "R-13"),
    ("R1336MZZE", "R-1336mzz(E)"),
    ("R134a", "R-134a"),
    ("R13I1", "R-13I1"),
    ("R14", "R-14"),
    ("R141b", "R-141b"),
    ("R142b", "R-142b"),
    ("R143a", "R-143a"),
    ("R152A", "R-152a"),
    ("R161", "R-161"),
    ("R21", "R-21"),
    ("R218", "R-218"),
    ("R22", "R-22"),
    ("R227EA", "R-227ea"),
    ("R23", "R-23"),
    ("R236EA", "R-236ea"),
    ("R236FA", "R-236fa"),
    ("R245ca", "R-245ca"),
    ("R245fa", "R-245fa"),
    ("R32", "R-32"),
    ("R365MFC", "R-365mfc"),
    ("R404A", "R-404A"),
    ("R407C", "R-407C"),
    ("R41", "R-41"),
    ("R410A", "R-410A"),
    ("R507A", "R-507A"),
    ("RC318", "RC-318"),
    ("SES36", "SES36"),
    ("SulfurDioxide", "Sulfur Dioxide (SO₂)"),
    ("SulfurHexafluoride", "Sulfur Hexafluoride (SF₆)"),
    ("Toluene", "Toluene"),
    ("Water", "Water (H₂O)"),
    ("Xenon", "Xenon"),
    ("cis-2-Butene", "cis-2-Butene"),
    ("m-Xylene", "m-Xylene"),
    ("n-Butane", "n-Butane (R-600)"),
    ("n-Decane", "n-Decane"),
    ("n-Dodecane", "n-Dodecane"),
    ("n-Heptane", "n-Heptane"),
    ("n-Hexane", "n-Hexane"),
    ("n-Nonane", "n-Nonane"),
    ("n-Octane", "n-Octane"),
    ("n-Pentane", "n-Pentane"),
    ("n-Propane", "n-Propane (R-290)"),
    ("n-Undecane", "n-Undecane"),
    ("o-Xylene", "o-Xylene"),
    ("p-Xylene", "p-Xylene"),
    ("trans-2-Butene", "trans-2-Butene")
]


def property_generator(selected_fluids , PropsSI):
    # This function is used to generate the properties of the fluids
    temperature = 25 + 273.15
    pressure = 101325
    
    for fluid in selected_fluids:
        try:
                h_liquid = PropsSI('H', 'T', temperature, 'Q', 0, fluid)
                h_vapor = PropsSI('H', 'T', temperature, 'Q', 1, fluid)
                latent_heat_vaporisation = h_vapor - h_liquid
                specific_heat_capacity = PropsSI('C', 'T', temperature, 'P', pressure, fluid)
                Density_L= PropsSI('D', 'T', temperature, 'Q', 0, fluid)
                Density_G= PropsSI('D', 'T', temperature, 'Q', 1, fluid)
                Evaporation_temp = PropsSI('T', 'P', pressure, 'Q', 0, fluid)
                yield [latent_heat_vaporisation, specific_heat_capacity, Density_L, Density_G, Evaporation_temp]
        except Exception as error:
            print(f"Error retrieving properties for {fluid}: {error}")
            yield [None, None, None, None, None]

if __name__ == "__main__":
    # Example usage
    
    selected_fluids = ["WATER", "R600"]
    for properties in property_generator(selected_fluids, PropsSI):
        print(properties)