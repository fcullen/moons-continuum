import caesar
import numpy as np

def make_catalogue(output_file, sanpshot_files):

    ofile = open(output_file, 'w')
    ofile.write('# idx lmass_stellar lmass_tot lsfr lssfr lzstar ')
    ofile.write('u_cfht b_subaru v_subaru g_subaru r_subaru i_subaru z_subaru ')
    ofile.write('y_vista j_vista h_vista k_vista irac_1 irac_2\n')

    for hdf in sanpshot_files:

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
            ofile.write('{:15.3f}'.format(lzstar))

            # add photometry in the COSMOS filters (narrowbands not available)
            filter_names = ['megacam_u', 'suprimecam_b', 'suprimecam_v', 'suprimecam_g', 
                'suprimecam_r', 'suprimecam_i', 'suprimecam_z', 'vista_y', 'vista_j',
                'vista_h', 'vista_k', 'irac_1', 'irac_2']

            for filt in filter_names:

                ofile.write('{:15.2f}'.format(gal.appmag[filt]))

            ofile.write('\n')

    ofile.close()

if __name__ == "__main__":

    make_catalogue(output_file='moons_simba_z1p5_galaxies.cat', 
        sanpshot_files=['./simba_snapshots/m100n1024_085.hdf5', 
                        './simba_snapshots/m100n1024_090.hdf5', 
                        './simba_snapshots/m100n1024_098.hdf5'])

