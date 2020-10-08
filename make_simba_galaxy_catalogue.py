import caesar
import numpy as np

lssfr_cut = -10.5

# functiosn which return SNR/resolution element at R=1000
# in the different redshift bins for passive and star-forming galaxies
def snr_vs_hmag_z1p5_passive(hmag):

    lsnr_h = -0.4 * hmag + 10.11
    lsnr_yj = -0.38 * hmag + 9.64
    lsnr_ri = -0.41 * hmag + 10.12

    return (10**lsnr_h, 10**lsnr_yj, 10**lsnr_ri)


def snr_vs_hmag_z1p5_starforming(hmag):

    lsnr_h = -0.4 * hmag + 9.82
    lsnr_yj = -0.37 * hmag + 9.37
    lsnr_ri = -0.38 * hmag + 9.36

    return (10**lsnr_h, 10**lsnr_yj, 10**lsnr_ri)


# function to make the catalogue:
def make_catalogue(output_file, sanpshot_files):

    ofile = open(output_file, 'w')
    ofile.write('# idx lmass_stellar lmass_tot lsfr lssfr lzstar ')
    ofile.write('u_cfht b_subaru v_subaru g_subaru r_subaru i_subaru z_subaru ')
    ofile.write('y_vista j_vista h_vista k_vista irac_1 irac_2 snr_h snr_yj snr_ri\n')

    for hdf in sanpshot_files:

        obj = caesar.load(hdf)
        redshift = obj.simulation.redshift
        print("Loded simba snapshot at z={:.2f}".format(redshift))

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

                if gal.appmag[filt] >= 100:
                    ofile.write('{:15.2f}'.format(-999.))
                else:
                    ofile.write('{:15.2f}'.format(gal.appmag[filt]))

            # add the snr per resolution element in the three MOONS gratings
            if (sfr <= 0) | (gal.appmag['vista_h'] >= 100.):
                snr_h = -999.
                snr_yj = -999.
                snr_ri = -999.
            else:
                if (redshift > 1.15) & (redshift < 1.75):
                    if lssfr <= lssfr_cut:
                        snr_h, snr_yj, snr_ri = snr_vs_hmag_z1p5_passive(hmag=gal.appmag['vista_h'])
                    else:
                        snr_h, snr_yj, snr_ri = snr_vs_hmag_z1p5_starforming(hmag=gal.appmag['vista_h'])
                else: # don't have data for other redshifts yet
                    snr_h = -999.
                    snr_yj = -999.
                    snr_ri = -999.

            ofile.write('{:15.1f}'.format(snr_h))
            ofile.write('{:15.1f}'.format(snr_yj))
            ofile.write('{:15.1f}'.format(snr_ri))

            ofile.write('\n')

    ofile.close()

if __name__ == "__main__":

    make_catalogue(output_file='moons_simba_z1p5_galaxies.cat', 
        sanpshot_files=['./simba_snapshots/m100n1024_085.hdf5',
                        './simba_snapshots/m100n1024_087.hdf5', 
                        './simba_snapshots/m100n1024_090.hdf5',
                        './simba_snapshots/m100n1024_095.hdf5',
                        './simba_snapshots/m100n1024_098.hdf5'])

