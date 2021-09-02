import numpy as np
import xarray as xr
from phenopy import _getPheno0
from phenoxr.pheno import _getLSPmetrics2

def _getPheno2D(dstack, doy, interpolType, nan_replace, rollWindow, nGS, xnew=None):
    # dstack.doy
    ans = np.apply_along_axis(_getPheno0, 0, dstack, doy, interpolType, nan_replace, rollWindow, nGS)
    
    # TODO: ¿_getPheno0 cambia el orden del arreglo? si es así, debo corregir - DONE?
    # TODO: retornar día del año modificado, eliminar time/year, usar xnew (nuevo doy) - DONE!
    # Esto se llama PhenoShape
    
    if xnew is None:
        xnew = range(1, nGS + 1)
        
    return _assemble(ans, dstack, xnew, True)
    

def _parseLSP(dstack, xnew, nGS, num, phentype):
    # num=len(bandNames) = 16
    ans = np.apply_along_axis(_getLSPmetrics2, 0, dstack, xnew, nGS, num, phentype)
    
    return _assemble(ans, dstack, range(1, num+1), True)


def _assemble(computed_data, original_stack, z_values, asDataArray=True):
    coords_ = {'time': z_values,
              'y': original_stack['y'],
              'x': original_stack['x']}
    
    if asDataArray:
        out = xr.DataArray(computed_data, 
                           coords=coords_, 
                           dims=original_stack.dims)
    else:
        pass
    
    return out