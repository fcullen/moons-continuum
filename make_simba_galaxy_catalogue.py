import caesar
import numpy as np

ofile = open('moons_simba_galinfo.dat', 'w')
ofile.write('# idx lmass_stellar lmass_tot lsfr lssfr lzstar\n')

# load the snapshot:
hdf_files = ['m100n1024_090.hdf5', 'm100n1024_104.hdf5']

for hdf in hdf_files:

    obj = caesar.load(hdf)
    print("Loded simba snapshot at z={:.2f}".format(obj.simulation.redshift))

    # select the galaxies:
    galaxies = obj.galaxies

    # loop though galaxies and extract information:
    for i, gal in enumerate(galaxies[:]):

        ofile.write('{:^15d}'.format(i))

        # stellar mass
        lmass_stellar = np.log10(gal.masses['stellar'])
        ofile.write('{:15.3f}'.format(lmass_stellar))

        # total mass:
        lmass_tot = np.log10(gal.masses['total'])   
        ofile.write('{:15.3f}'.format(lmass_tot))

        # sfr and ssfr:
        sfr = gal.sfr.value
        if sfr <= 0:
            lsfr = -999.
            lssfr = -999.
        else:
            lsfr = np.log10(sfr)
            lssfr = np.log10(sfr / gal.masses['stellar'].value)
        
        ofile.write('{:15.3f}'.format(lsfr))
        ofile.write('{:15.3f}'.format(lssfr))

        # metallicity:
        lzstar = np.log10(gal.metallicities['stellar'])
        ofile.write('{:15.3f}\n'.format(lzstar))

ofile.close()