
/****************************************************************************
 *
 * MODULE:       r3.retile
 *   	    	
 * AUTHOR(S):    Original author 
 *               Soeren Gebbert soerengebbert <at> googlemail <dot> co
 * 
 * PURPOSE:      Retiles an existing G3D map with user defined x, y and z tile size
 *
 * COPYRIGHT:    (C) 2011 by the GRASS Development Team
 *
 *               This program is free software under the GNU General Public
 *   	    	License (>=v2). Read the file COPYING that comes with GRASS
 *   	    	for details.
 *
 *****************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <grass/gis.h>
#include <grass/raster.h>
#include <grass/G3d.h>
#include <grass/glocale.h>

/*- Parameters and global variables -----------------------------------------*/
typedef struct {
    struct Option *input, *output, *tiling;
    struct Flag *cache;
} paramType;

paramType param; /*Parameters */

/*- prototypes --------------------------------------------------------------*/
void fatal_error(void *map, int *fd, int depths, char *errorMsg); /*Simple Error message */
void set_params(); /*Fill the paramType structure */
void g3d_to_raster(void *map, G3D_Region region, int *fd); /*Write the raster */
int open_output_map(const char *name, int res_type); /*opens the outputmap */
void close_output_map(int fd); /*close the map */



/* ************************************************************************* */
/* Error handling ********************************************************** */

/* ************************************************************************* */
void fatal_error(void *map, int *fd, int depths, char *errorMsg)
{
    int i;

    /* Close files and exit */
    if (map != NULL) {
        if (!G3d_closeCell(map))
            G3d_fatalError(_("Unable to close the 3d raster map"));
    }

    if (fd != NULL) {
        for (i = 0; i < depths; i++)
            Rast_unopen(fd[i]);
    }

    G3d_fatalError(errorMsg);
    exit(EXIT_FAILURE);

}

/* ************************************************************************* */
/* Set up the arguments we are expecting ********************************** */

/* ************************************************************************* */
void set_params()
{
    param.input = G_define_standard_option(G_OPT_R3_INPUT);

    param.output = G_define_standard_option(G_OPT_R3_OUTPUT);
    param.output->description = _("Name of the retiled 3D raster map");
    
    param.tiling = G_define_standard_option(G_OPT_R3_TILE_DIMENSION);
    
    param.cache = G_define_flag();
    param.cache->key = 'c';
    param.cache->description = "Disable tile caching";
}


/* ************************************************************************* */
/* Main function, open the G3D map and create the raster maps ************** */

/* ************************************************************************* */
int main(int argc, char *argv[])
{
    struct GModule *module;
    G3D_Map *map = NULL;
    int tileX, tileY, tileZ;
    char *mapset;

    /* Initialize GRASS */
    G_gisinit(argv[0]);

    module = G_define_module();
    G_add_keyword(_("raster3d"));
    G_add_keyword(_("retile"));
    G_add_keyword(_("voxel"));
    module->description = _("Retiles an existing G3D map with user defined x, y and z tile size");

    /* Get parameters from user */
    set_params();

    /* Have GRASS get inputs */
    if (G_parser(argc, argv))
        exit(EXIT_FAILURE);

    G_debug(3, _("Open 3d raster map <%s>"), param.input->answer);

    mapset = G_find_grid3(param.input->answer, "");
    
    if (mapset == NULL)
        G3d_fatalError(_("3d raster map <%s> not found"),
                       param.input->answer);

    /*Set the defaults */
    G3d_initDefaults();
    
    if(!param.cache->answer)
        map = G3d_openCellOld(param.input->answer, mapset, G3D_DEFAULT_WINDOW, 
                          G3D_TILE_SAME_AS_FILE, G3D_USE_CACHE_DEFAULT);
    else
        map = G3d_openCellOld(param.input->answer, mapset, G3D_DEFAULT_WINDOW, 
                          G3D_TILE_SAME_AS_FILE, G3D_NO_CACHE);

    if (map == NULL)
        G3d_fatalError(_("Unable to open 3d raster map <%s>"),
                       param.input->answer);

    /* Get the tile dimension */
    G3d_getTileDimension(&tileX, &tileY, &tileZ);    
    if (strcmp(param.tiling->answer, "default") != 0) {
	if (sscanf(param.tiling->answer, "%dx%dx%d",
		   &tileX, &tileY, &tileZ) != 3) {
	    G3d_fatalError(_("G3d_getStandard3dParams: tile dimension value invalid"));
	}
    }
    
    if(!param.cache->answer)
        G_message("Retile map with tile cache enabled");
    else
        G_message("Retile map without tile caching");
    
    G3d_retile(map, param.output->answer, tileX, tileY, tileZ);

    /* Close files and exit */
    if (!G3d_closeCell(map))
        fatal_error(map, NULL, 0, _("Error closing 3d raster map"));

    map = NULL;

    return (EXIT_SUCCESS);
}
